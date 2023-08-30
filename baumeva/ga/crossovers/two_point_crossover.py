from random import sample
from .base_crossover import BaseCrossover
from baumeva.ga import GaData


class TwoPointCrossover(BaseCrossover):
    """
    A class for implementing two-point crossover in a genetic algorithm.
    Inherits from BaseCrossover.
    """
    def __init__(self) -> None:
        """
        Initialize the TwoPointCrossover instance.

        :return: None
        """
        super().__init__()
        self.len_individ = None

    def crossover(self, parent_1: list, parent_2: list, child_1: dict, child_2: dict) -> tuple:
        idx_segment = sample(range(1, self.len_individ), 2)
        idx_segment.sort()
        child_1['genotype'] = parent_1[:idx_segment[0]] + parent_2[idx_segment[0]:idx_segment[1]] + parent_1[
                                                                                                    idx_segment[1]:]
        child_2['genotype'] = parent_2[:idx_segment[0]] + parent_1[idx_segment[0]:idx_segment[1]] + parent_2[
                                                                                                    idx_segment[1]:]
        return child_1, child_2

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the two-point crossover operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        self.len_individ = len(ga_data.population[0]['genotype'])
        super().execute(ga_data)
