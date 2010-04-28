class BaseSearchField(object): 
    
    def __init__(self, stored=True, indexed=True, provided=False,
                 id_field=False):
        self.stored = stored
        self.indexed = indexed
        self.provided = provided
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
        
    def get_queryset(self):
        """Override to customize QuerySet.
        """
        return self._meta.get("document_type").objects()
