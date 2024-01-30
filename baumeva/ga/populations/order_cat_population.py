from random import sample
from typing import List
from .cat_population import CatPopulation


class OrderCatPopulation(CatPopulation):
    """
    Class for representing ordered categorical population in a genetic algorithm.
    Inherits from OrderBasePopulation.
    """

    def get_generated_individ(self) -> List[int]:
        """
        Method for generating ordinal categorical individuals from gen.
        self.gens: tuple[int_1, int_2, int_3], where int_1 - start point, int_2 - end point,
                   int_3 - length of track <= then (int_2 - int_1).
                   Example: (0, 30, 10) - 30 total points , but track contains only 10.
        :return: genotype: List[int]
        """
        genotype = sample(range(self.gens[0], self.gens[1]+1), self.gens[2])
        return genotype

    @staticmethod
    def get_empty_copy():
        """
        Get an empty instance of OrderCatPopulation.

        :return: An empty instance of OrderCatPopulation.
        """
        return OrderCatPopulation()
