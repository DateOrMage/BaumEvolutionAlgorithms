from abc import ABC, abstractmethod
from baumeva.ga import GaData


class BaseSelection(ABC):

    @abstractmethod
    def execute(self, ga_data: GaData) -> None:
        pass
