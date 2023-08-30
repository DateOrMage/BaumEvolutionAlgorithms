from random import randint
from .base_crossover import BaseCrossover
from baumeva.ga import GaData


class UniformCrossover(BaseCrossover):
    """
    A class for implementing uniform crossover in a genetic algorithm.
    Inherits from BaseCrossover.
    """
    def __init__(self) -> None:
        """
        Initialize the UniformCrossover instance.

        :return: None
        """
        super().__init__()
        self.len_individ = None

    def crossover(self, parent_1: list, parent_2: list, child_1: dict, child_2: dict) -> tuple:

        new_gens = []
        for i in range(self.len_individ):
            coin = randint(1, 2)
            if coin == 1:
                new_gens.append(parent_1[i])
            else:
                new_gens.append(parent_2[i])
        child_1['genotype'] = new_gens
        child_2['genotype'] = new_gens

        return child_1, child_2

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the uniform crossover operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        self.len_individ = len(ga_data.population[0]['genotype'])
        super().execute(ga_data)
