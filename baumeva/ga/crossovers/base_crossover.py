from abc import ABC, abstractmethod
from baumeva.ga import GaData


class BaseCrossover(ABC):
    def __init__(self, num_offsprings: int = 2) -> None:
        self.num_offsprings = num_offsprings

    def execute(self, ga_data: GaData) -> None:
        ga_data.children = ga_data.population.get_empty_copy()
