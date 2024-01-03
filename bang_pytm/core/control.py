from .element import Element

class Requirement(Element):
    """
    Based on ASVS
    """
    def __init__(self,name: str, desc: str = None, applicability: dict = None, related_cwe:list =None, related_nist: list=None)-> None:
        super().__init__(name, desc)
        self.applicability = applicability
        self.related_cwe = related_cwe
        self.related_nist = related_nist


class Control:

    def __init__(self):
        # TO DO
        pass
