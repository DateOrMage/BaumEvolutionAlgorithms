from abc import ABC, abstractmethod
from baumeva.ga import GaData


class BaseCrossover(ABC):
    """
    Abstract class for implementing crossover operations in a genetic algorithm.
    """
    def __init__(self) -> None:
        """
        Initialize the BaseCrossover instance.
        :return: None
        """
        self.num_offsprings: int = 1

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the crossover operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        ga_data.children = ga_data.population.get_empty_copy()
