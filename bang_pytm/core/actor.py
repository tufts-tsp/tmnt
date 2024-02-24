from bang_pytm.core.descriptors import varString
from bang_pytm.core.tm import TM
from .element import Element

class Actor(Element):
    """a person or organization that is represented in the threat model"""

    def __init__(self, name, actor_type: str = None, physical_access: bool = False, **kwargs):
        """
        Actor

        actor_type : str
            Options: Individual, Organization ... User can specify
        associated_assets : List[Asset]
            In the case of external orgs/individuals these would be External Entity
        admin_assets : List[Asset]
            Should be a subset of associated_assets, i.e. if you are adding 
            admin asset that is not present in associated it should be added to
            it as well
        """
        self.physical_access = physical_access
        super().__init__(name, **kwargs)
        
