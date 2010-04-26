from base import BaseSearchField


__all__ = ["IntField", "FloatField", "StringField", "DictField", 
           "BooleanField"]


class ValidationError(Exception):
    pass


class IntField(BaseSearchField):
    
    def validate(self, value):
        """Ensure that the given value is or could be an integer. 
        """
        if not isinstance(value, int):
            try:
                value = int(value)
            except:
                raise ValidationError("%s could not be converted to int" % \
                                      value)


class FloatField(BaseSearchField):
    
    def validate(self, value):
        """Ensure that the given value is or could be a float.
        """
        if not isinstance(value, float):
            try:
                value = float(value)
            except:
                raise ValidationError("%s could not be converted to float" % \
                                      value)


class StringField(BaseSearchField):

    def validate(self, value):
        """Ensure that the given value is a string. 
        """
        if not isinstance(value, dict):
            raise ValidationError("%s must be a string" % self.name)
        
        
class DictField(BaseSearchField):
    
    def validate(self, value):
        """Ensure that the given value is a dict. 
        """
        if not isinstance(value, dict):
            raise ValidationError("%s must be a dictionary" % self.name)


class BooleanField(BaseSearchField):
    
    def validate(self, value):
        """Ensure that the given value is a boolean.
        """
        if not isinstance(value, bool):
            raise ValidationError("%s must be a boolean" % self.name)
