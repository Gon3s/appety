from typing import Dict, Type
from .base_parser import BaseParser
from .appety_parser import AppetyParser
from .brasserie_parser import BrasserieParser

PARSERS: Dict[str, Type[BaseParser]] = {
    "appety": AppetyParser,
    "brasserie": BrasserieParser,
}


def get_parser(name: str) -> BaseParser:
    if name not in PARSERS:
        raise ValueError(
            f"Parser '{name}' not found. Available parsers: {list(PARSERS.keys())}"
        )
    return PARSERS[name]()
