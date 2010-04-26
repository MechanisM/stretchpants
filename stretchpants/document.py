from base import TopLevelSearchIndex, BaseSearchDocument
from fields import StringField


class SearchDocument(BaseSearchDocument):
    __metaclass__ = TopLevelSearchIndex

    def get_queryset(self):
        raise NotImplementedError("Please override this method to return your "
                                  "document's queryset.")
