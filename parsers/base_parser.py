from abc import ABC, abstractmethod
from typing import Optional, Dict


class BaseParser(ABC):
    """Base class for all menu parsers."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for the parser"""
        pass

    @abstractmethod
    def get_latest_menu(self) -> Optional[Dict[str, str]]:
        """Get the latest menu from the source."""
        pass
