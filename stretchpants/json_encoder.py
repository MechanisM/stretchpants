from datetime import datetime, date
import json
from time import mktime
        
from pymongo.cursor import Cursor
from pymongo.dbref import DBRef
from pymongo.objectid import ObjectId

from mongoengine.connection import _get_db
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.queryset import QuerySet

from settings import DEFAULT_DATE_FORMAT, DEFAULT_DATETIME_FORMAT
from utils.fields import LazyReference


class JsonEncoder(json.JSONEncoder):
    def default(self, value):
        """Convert niche data types, and ``Document`` subclasses.
        
        Conversion notes:

        - ``datetime.date`` and ``datetime.datetime`` objects are
          converted into UNIX timestamps.
        - ``pymongo.objectid.ObjectId`` objects are converted into
          ``unicode`` strings.
        - ``mongoengine.document.Document`` instances are converted
          into ``dict`` representations via instance._data.
        - ``DBRef`` objects are automagically dereferenced.
        """

        if isinstance(value, datetime):
            return mktime(value.timetuple())
        elif isinstance(value, date):
            dt = datetime(value.year, value.month, value.day, 0, 0, 0)
            return mktime(dt.timetuple())
        elif isinstance(value, ObjectId):
            return unicode(value)
        elif isinstance(value, (Cursor, QuerySet)):
            return list(value)
        elif issubclass(value.__class__, (Document, EmbeddedDocument)):
            present_keys = dict(filter(lambda k: k[0] in value._present_fields, 
                                value.__dict__['_data'].iteritems()))
            return present_keys
        elif isinstance(value, DBRef):
            # dereference
            obj = _get_db().dereference(value)
            if obj:
                del obj['_types']
                return obj
        elif isinstance(value, LazyReference):
            return value.dereference()
        else:
            # use no special encoding and hope for the best
            return value
