from abc import ABC, abstractmethod


class BaseReportBuilder(ABC):
    @abstractmethod
    def build(self, *args, **kwargs) -> None:
        """Print report in console"""
        pass
