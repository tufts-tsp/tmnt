from typing import Dict, Set

from .element import Element


class Data(Element):

    def __init__(
        self,
        name,
        is_pii: bool = False,
        is_phi: bool = False,
        format: str = None,
        is_credentials: bool = False,
        lifetime: str = None,
        **kwargs
    ):
        """
        Note to @mrtoaf: add recommended values for lifetime (not requirement)
        """
        self.is_pii = is_pii
        self.is_phi = is_phi
        self.format = format
        self.is_credentials = is_credentials
        self.lifetime = lifetime
        if is_phi == True:
            self.is_phi = True
        super().__init__(name, **kwargs)
        # TO DO