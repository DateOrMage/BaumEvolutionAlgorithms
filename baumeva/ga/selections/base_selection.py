from abc import ABC, abstractmethod
from baumeva.ga import GaData


class BaseSelection(ABC):

    def execute(self, ga_data: GaData) -> None:
        ga_data.population.reset_idx_individ()
        ga_data.parents = ga_data.population.get_empty_copy()
