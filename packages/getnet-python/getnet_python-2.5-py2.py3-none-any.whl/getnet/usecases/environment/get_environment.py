"""This module implement API environment enum"""
from enum import Enum, unique

API_URLS = {
    0: "https://api-sandbox.getnet.com.br",
    1: "https://api-homologacao.getnet.com.br",
    2: "https://api.getnet.com.br",
}


@unique
class Environment(Enum):
    """Environment represents the API envinments specs
    args:
        Enum (Enum): Enum class
    """

    SANDBOX = 0
    HOMOLOG = 1
    PRODUCTION = 2

    def base_url(self) -> str:
        """base_url returns the base url for the environment
        returns:
            str: base url
        """
        return API_URLS[self.value]
