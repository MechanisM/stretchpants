"""

TopLevelSearchIndex             metaclass, inherits from ``type``

BaseSearchDocument              base for indexed documents. inherits from ``object``.

BaseField                       base for a field of an indexed document

    Methods:
        def validate            validate that the value is "correct"
        def prepare             convert values into a type usable by ElasticSearch

    Properties:
        stored                  boolean. determines if ES should "store" the value.
        indexed                 boolean. determines if ES should "index" the value.
        name                    string. name to use when storing in the index.

SearchDocument                  base for indexed documents

    Methods:
        def save
        def delete
    
    Properties
        collection_name         name of the index, eg "entities"
        class_name              document's type, eg "Artist"
        document_id             document's id. can be string version of objectid.
        *fields                 collection of BaseField subclasses

"""

class BaseSearchField(object): 
    
    def __init__(self, stored=True, indexed=True, document_field=True,
                 provider=None, id_field=False):
        self.stored = stored
        self.indexed = indexed
        self.document_field = document_field
        self._provider = provider
        self._id_field = id_field

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance._data.get(self.name)
    
    def __set__(self, instance, value):
        instance._data[self.name] = value

    def prepare(self, value):
        return value


class TopLevelSearchIndex(type):
    
    def __new__(cls, name, bases, attrs):
        metaclass = attrs.get('__metaclass__')
        super_new = super(TopLevelSearchIndex, cls).__new__
        if metaclass and issubclass(metaclass, TopLevelSearchIndex):
            return super_new(cls, name, bases, attrs)
        
        doc_fields = {}
        superclasses = {}
        id_field = None
        
        for base in bases:
            # Include all fields present in superclasses
            if hasattr(base, '_fields'):
                doc_fields.update(base._fields)
                class_name.append(base._class_name)
                # Get superclasses from superclass
                superclasses[base._class_name] = base
                superclasses.update(base._superclasses)

        # Check for meta properties
        meta = attrs.get('_meta', attrs.get('meta', {}))
        attrs['_meta'] = meta

        # Add the document's fields to the _fields attribute
        for attr_name, attr_value in attrs.items():
            if hasattr(attr_value, "__class__") and \
               issubclass(attr_value.__class__, BaseSearchField):
                attr_value.name = attr_name
                doc_fields[attr_name] = attr_value
                if attr_value._id_field:
                    id_field = attr_name

        if id_field is None:
            raise Exception("Please define an id field")

        attrs['_fields'] = doc_fields
        attrs['_id_field'] = id_field
        
        new_class = super_new(cls, name, bases, attrs)
        return new_class

        
class BaseSearchDocument(object):

    def __init__(self, **values):
        self._data = {}
        # Assign initial values to instance
        for attr_name, attr_value in self._fields.items():
            if attr_name in values:
                setattr(self, attr_name, values.pop(attr_name))
            else:
                # Use default value if present
                value = getattr(self, attr_name, None)
                setattr(self, attr_name, value)

    def __iter__(self):
        return iter(self._fields)
