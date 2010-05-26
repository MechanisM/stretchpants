from mongoengine import Document


class RegistrationError(Exception):
    pass


class SearchSite(object):

    def __init__(self):
        self._registry = {}
        self._field_mapping = None
        
    def __iter__(self):
        return self._registry.iteritems()
        
    def register(self, document, index_class):
        """Register a ``Document``.
        
        :param document: Document class, *not* an instance.
        :param index_class: SearchDocument used for indexing.
        """
        
        if not issubclass(document, Document):
            raise Exception("'document' arg must be a mongoengine Document")
    
        if document in self._registry:
            raise RegistrationError("Document %s already registered" % \
                                    document().__class__)

        # index_class._document_type = document
        idx_cls = index_class()
        idx_cls._meta['document_type'] = document

        self._registry[document] = idx_cls
            
    def unregister(self, document):
        """Remove a ``Document`` from the registry.
        
        :param document: Document class, *not* an instance.
        """
        if document in self._registry:
            del self._registry[document]
    
    def get_index(self, document):
        if not document in self._registry:
            raise RegistrationError("%s is not registered" % \
                                    document().__class__)
        return self._registry[document]

    
site = SearchSite()
