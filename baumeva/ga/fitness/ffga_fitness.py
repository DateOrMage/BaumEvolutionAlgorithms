from typing import Union
from .multi_fitness import MultiFitness
from baumeva.ga.multi_ga_data import MultiGaData


class FFGAFitness(MultiFitness):
    """
    A class for calculating fitness values for multiobjective optimization using the FFGA algorithm.
    Inherits from MultiFitness.
    """

    def get_fitness_score(self, individ: dict, penalty_value: Union[int, float] = 0) -> Union[int, float]:
        """
        Method for calculating fitness score of individual.

        :param individ: data of an individual.
        :param penalty_value: list of fitness values (with respect to optimization values) of an individual.
        :return: list of fitness scores of the individual.
        """

        score = 1.0 / (1 + individ['rank'])

        # if self.obj_value is not None:
        #     score = [1.0 / (1 + abs(self.obj_value[i] - obj_score[i]) + penalty_value) for i in range(len(obj_score))]
        # else:
        #     score = [-(score + penalty_value) for score in obj_score]

        return score

    def execute(self, ga_data: MultiGaData) -> None:
        """
        Calculate and assign fitness scores to individuals in the population.

        :param ga_data: MultiGaData instance containing population and related data.
        :return: None
        """

        super().execute(ga_data)
