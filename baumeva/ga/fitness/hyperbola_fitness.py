from typing import List, Union
from .base_fitness import BaseFitness


class HyperbolaFitness(BaseFitness):
    """
    A class for calculating fitness value using the hyperbola approach.
    Inherits from BaseFitness.
    """

    def get_fitness_score(self, individ: dict, penalty_value: Union[int, float] = 0) ->\
            Union[int, float]:
        """
        Method for calculating fitness score of individual.

        :param individ: data of an individual.
        :param penalty_value: fitness value of an individual.
        :return: fitness score of the individual.
        """

        if self.obj_value is not None:
            score = 1.0 / (1 + abs(self.obj_value - individ['obj_score']) + penalty_value)
        else:
            score = -(individ['obj_score'] + penalty_value)

        return score
