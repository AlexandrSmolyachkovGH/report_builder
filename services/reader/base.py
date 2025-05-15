from abc import ABC, abstractmethod
from typing import List, Dict


class BaseCSVDataReader(ABC):

    @abstractmethod
    def read(self, *args, **kwargs) -> Dict[str, List[Dict[str, str]]]:
        """Read file in parts and extract all parts into result"""
        pass
