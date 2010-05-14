import json

from base import TopLevelSearchIndex, BaseSearchDocument
from fields import StringField
from json_encoder import JsonEncoder


class SearchDocument(BaseSearchDocument):
    __metaclass__ = TopLevelSearchIndex
    
    @property
    def _document_type(self):
        return self._meta.get("document_type")._class_name.split(".")[-1]

    def count(self):
        if not hasattr(self, "_doc_count"):
            setattr(self, "_doc_count", self.get_queryset().count())
        return self._doc_count

    def prepare(self, document):
        """Prepare a document for indexing.
        """
        data = {}
        for field in self._fields:
            if not self._fields[field].provided:
                # handle document field
                value = getattr(document, field, None)
                if value is not None:
                    data[field] = self._fields[field].prepare(value)
            else:
                # handle "dynamic"/callable field:
                # pass the document instance to the field's data provider
                provider = getattr(self, "provide_" + field)
                if not callable(provider):
                    raise Exception("Provider for %s must be callable" % field)
                data[field] = provider(document)
        return data

    def __iter__(self):
        """Iterate over given QuerySet and yield storable version.
        """
        from math import ceil
        
        qs_fields = [field 
                     for field 
                     in self._fields.keys() 
                     if not self._fields[field].provided]
        necessary_fields = self._meta.get("extra_fields")
        if necessary_fields:
            qs_fields += necessary_fields
        qs = self.get_queryset().only(*qs_fields)
        
        # lets do this in chunks of 1000, eh?
        limit = 1000
        iterations = int(ceil(qs.count() / float(limit)))
        
        for offset in xrange(0, iterations):
            start = offset * 1000
            
            qs_chunk = qs[start:start+limit]
            for document in qs_chunk:
                data = self.prepare(document)
                index_data = {'index': self._meta.get("index"),
                              'document_type': self._document_type,
                              'document_id': document[self._id_field],
                              'document': data}
                yield IndexableDocument(**index_data)


class IndexableDocument(object):
    
    def __init__(self, index, document_type, document_id, document):
        self.index = index
        self.document_type = document_type
        self.document_id = document_id
        self.document = document

    @property
    def object_path(self):
        "This object's index/type/key path. E.g., entities/Artist/12345"
        return "%s/%s/%s" % (self.index, self.document_type, self.document_id)

    def encode(self):
        return json.dumps(self.document, cls=JsonEncoder)
