from abc import ABC, abstractmethod
from baumeva.ga import GaData


class BaseCrossover(ABC):
    """
    Abstract class for implementing crossover operations in a genetic algorithm.
    """
    def __init__(self, num_offsprings: int = 2) -> None:
        """
        Initialize the BaseCrossover instance.

        :param num_offsprings: the number of offspring individuals to generate (default: 2).
        :return: None
        """
        self.num_offsprings = num_offsprings

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the crossover operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        ga_data.children = ga_data.population.get_empty_copy()
