from enum import Enum


class TokenSourceType(Enum):
    rss         = 1
    twitter     = 2


class TokenSource:

    def __init__(self, official:bool):
        self.official = official

    def get_token_blob() -> str:
        # Override in subclass
        pass
