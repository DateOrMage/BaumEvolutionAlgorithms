from typing import List, Union
from .base_fitness import BaseFitness


class HyperbolaFitness(BaseFitness):
    """
    A class for calculating fitness value using the hyperbola approach.
    Inherits from BaseFitness.
    """

    def get_fitness_score(self, obj_score: Union[int, float], penalty_value: Union[int, float] = 0) ->\
            Union[int, float]:
        """
        Method for calculating fitness score of individual.

        :param obj_score: object value of an individual.
        :param penalty_value: fitness value of an individual.
        :return: fitness score of the individual.
        """

        if self.obj_value is not None:
            score = 1.0 / (1 + abs(self.obj_value - (obj_score + penalty_value)))
        else:
            score = -(obj_score + penalty_value)

        return score
