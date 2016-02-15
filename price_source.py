from enum import Enum


class PriceSourceType(Enum):
    scrape      = 1
    api         = 2


class PriceSource:

    def __init__(self, stock: str, sourcetype: SourceType):
        self.stock = stock
        self.sourcetype = sourcetype

    def get_price() -> double:
        # Override in subclass
        pass
