from os import system
from weakref import WeakKeyDictionary

# 🍇 richard's grape

class immutableVar(object):
    """ensures that certain settings/ descriptors are never changed after setting them"""
    def __init__(self, default, required=False, doc=""):
        self.default = default
        self._is_set = False
        self.required = required
        self.doc = doc
        self.values = WeakKeyDictionary()
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.values.get(instance, self.default)
    
    def __set__(self, instance, new_value):
        if self._is_set:
            raise ValueError("Already set!")
        else:
            self.values[instance] = new_value
            self._is_set = True



class varString(immutableVar):
    """makes sure that the variable is a string when it needs to be"""

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("expecting a string value but instead receieved a {}".format(type(value)))
        super().__set__(instance, value)







# PLACEHOLDER #
class varFindings(immutableVar):
    """makes sure that the variable is a string when it needs to be"""

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("expecting a string value but instead receieved a {}".format(type(value)))
        super.__set__(instance, value)


# PLACEHOLDER #
class varStrings(immutableVar):
    """makes sure that the variable is a string when it needs to be"""

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("expecting a string value but instead receieved a {}".format(type(value)))
        super.__set__(instance, value)
