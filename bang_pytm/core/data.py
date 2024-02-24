from typing import Dict, Set

from .element import Element
from .asset import Asset
from .flow import Flow


class Data(Element):

    __flows: Set[Flow] = set()
    __assets: Dict[Asset, dict] = {}

    def __init__(
        self,
        name,
        assets: Dict[Asset, dict] = {},
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
        for k, v in assets:
            self.add_asset(k, v["location"], v["encrypted"])
        super().__init__(name, **kwargs)
        # TO DO

    @property
    def assets(self) -> dict:
        # For each asset, specify the location (processed, stored, sent,
        # received) and encryption (true, false)
        # example - {Asset1: {'location': ..., 'encrypted':True/False}}
        return self.__assets

    def add_asset(
        self, asset: Asset, loc: str = None, encrypted: bool = False
    ) -> None:
        self.__assets[asset] = {"location": loc, "encypted": encrypted}

    @property
    def flows(self) -> set:
        # listing the flows
        return self.__flows
