from random import randint
from .base_crossover import BaseCrossover
from baumeva.ga import GaData


class OnePointCrossover(BaseCrossover):
    """
    A class for implementing one-point crossover in a genetic algorithm.
    Inherits from BaseCrossover.
    """
    def __init__(self) -> None:
        """
        Initialize the OnePointCrossover instance.

        :return: None
        """
        super().__init__()
        self.len_individ = None

    def crossover(self, parent_1: list, parent_2: list, child_1: dict, child_2: dict) -> tuple:
        idx_point = randint(1, self.len_individ - 1)
        child_1['genotype'] = parent_1[:idx_point] + parent_2[idx_point:]
        child_2['genotype'] = parent_2[:idx_point] + parent_1[idx_point:]
        return child_1, child_2

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the one-point crossover operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        self.len_individ = len(ga_data.population[0]['genotype'])
        super().execute(ga_data)
