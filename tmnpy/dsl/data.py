from enum import Enum

from .element import Element


class Lifetime(Enum):

    """
    needs documentation
    """

    # not applicable
    NONE = "NONE"
    # unknown lifetime
    UNKNOWN = "UNKNOWN"
    # relatively short expiration date (time to live)
    SHORT = "SHORT_LIVED"
    # long or no expiration date
    LONG = "LONG_LIVED"
    # no expiration date but revoked/invalidated automatically in some conditions
    AUTO = "AUTO_REVOKABLE"
    # no expiration date but can be invalidated manually
    MANUAL = "MANUALLY_REVOKABLE"
    # cannot be invalidated at all
    HARDCODED = "HARDCODED"


class Data(Element):

    """
    needs documentation
    """

    def __init__(
        self,
        name: str,
        is_pii: bool = False,
        is_phi: bool = False,
        format: str = "N/A",
        is_credentials: bool = False,
        lifetime: Lifetime | str = Lifetime.NONE,
        **kwargs
    ):
        if not isinstance(is_pii, bool):
            raise ValueError("Is PII must be a boolean")
        self.is_pii = is_pii

        if not isinstance(is_phi, bool):
            raise ValueError("Is PHI must be a boolean")
        self.is_phi = is_phi

        if not isinstance(format, str):
            raise ValueError("Format must be a string")
        self.format = format

        if not isinstance(is_credentials, bool):
            raise ValueError("Is Credentials must be a boolean")
        self.is_credentials = is_credentials

        if isinstance(lifetime, str):
            lifetime = Lifetime[lifetime]

        if not isinstance(lifetime, Lifetime):
            raise ValueError("Lifetime bust be a Lifetime object")
        self.lifetime = lifetime

        super().__init__(name, **kwargs)
