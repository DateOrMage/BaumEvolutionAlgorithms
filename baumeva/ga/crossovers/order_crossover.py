from random import sample
from .base_crossover import BaseCrossover
from baumeva.ga import GaData


class OrderCrossover(BaseCrossover):
    """
    A class for implementing order crossover in a genetic algorithm.
    Inherits from BaseCrossover.
    """
    def __init__(self) -> None:
        """
        Initialize the OrderCrossover instance.

        :return: None
        """
        super().__init__()
        self.len_individ = None

    def get_idx_segment(self) -> list:
        """
        Get the indices for the crossover segment to change.

        :return: A list containing the indices of the crossover segment.
        """
        idx_segment = sample(range(1, self.len_individ), 2)
        idx_segment.sort()
        return idx_segment

    def crossover(self, parent_1: list, parent_2: list, child_1: dict, child_2: dict) -> tuple:
        idx_segment = self.get_idx_segment()
        right_side = self.len_individ - idx_segment[1]
        left_side = idx_segment[0]

        segment = parent_1[idx_segment[0]:idx_segment[1]]
        new_gens = [x for x in parent_2 if x not in segment]
        child_1['genotype'] = new_gens[right_side:right_side+left_side] + segment + new_gens[:right_side]

        segment = parent_2[idx_segment[0]:idx_segment[1]]
        new_gens = [x for x in parent_1 if x not in segment]
        child_2['genotype'] = new_gens[right_side:right_side + left_side] + segment + new_gens[:right_side]

        return child_1, child_2

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the order crossover operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        self.len_individ = len(ga_data.population[0]['genotype'])
        super().execute(ga_data)
