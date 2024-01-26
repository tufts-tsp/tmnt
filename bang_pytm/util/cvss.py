### TO BE DONE
### SHOULD IMPLEMENT ALL VERSIONS
### CAN USE https://github.com/RedHatProductSecurity/cvss as starting point

from decimal import Decimal
from typing import Self

class CVSS(object):
    def __init__(self) -> None:
        pass

    def severity(self, level: str = "overall") -> str:
        pass

    def exploitability(self, level: str = "overall") -> Decimal:
        pass

    def impact(self, level: str = "overall") -> Decimal:
        pass

    def vector_string(self, level: str = "overall") -> str:
        pass

    def convert(self, version: str) -> Self:
        pass
