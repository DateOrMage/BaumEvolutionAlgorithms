from typing import List, Union
from .multi_fitness import MultiFitness


class VEGAHyperbolaFitness(MultiFitness):
    """
    A class for calculating fitness values for multiobjective optimization using the hyperbola approach.
    Inherits from MultiFitness.
    """

    def get_fitness_score(self, individ: dict, penalty_value: Union[int, float] = 0) ->\
            List[Union[int, float]]:
        """
        Method for calculating fitness score of individual.

        :param individ: data of an individual.
        :param penalty_value: list of fitness values (with respect to optimization values) of an individual.
        :return: list of fitness scores of the individual.
        """

        if self.obj_value is not None:
            score = [1.0 / (1 + abs(self.obj_value[i] - individ['obj_score'][i]) + penalty_value)
                     for i in range(len(individ['obj_score']))]
        else:
            score = [-(score + penalty_value) for score in individ['obj_score']]

        return score
