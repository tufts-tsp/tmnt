from os import system

# 🍇 richard's grape

class immutableVar(object):
    """ensures that certain settings/ descriptors are never changed after setting them"""
    def __init__(self, required=False,doc=""):
        self._value = None
        self._is_set = False
        self.required = required
        self.doc = doc
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        if self._is_set:
            raise ValueError("Already set!")
        else:
            self._value = new_value
            self._is_set = True



class varString(immutableVar):
    """makes sure that the variable is a string when it needs to be"""

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("expecting a string value but instead receieved a {}".format(type(value)))
        super.__set__(instance, value)

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
