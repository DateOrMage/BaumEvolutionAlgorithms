from random import random
from copy import deepcopy
from .base_selection import BaseSelection
from baumeva.ga import GaData


class BalancedSelection(BaseSelection):
    """
    Class for implementing balanced selection in a genetic algorithm.
    Inherits from BaseSelection.
    """
    score_type = 'score'

    def __init__(self):
        """
        Initialize the BalancedSelection instance.

        :return: None
        """
        pass

    def add_probabilities(self, ga_data: GaData):
        sum_scores = 0
        for ind in ga_data.population:
            sum_scores += ind[self.score_type]
        for ind in ga_data.population:
            ind['selection_score'] = ind[self.score_type] / sum_scores

    @staticmethod
    def balanced_selection(ga_data: GaData):
        total_num_parents = int(ga_data.children_percent * ga_data.population.num_individ)
        avg_step = 1 / (ga_data.population.num_individ - 1)
        for _ in range(total_num_parents):
            rand_value = random()
            idx = int(rand_value / avg_step)
            while True:
                if rand_value >= ga_data.population[idx]['selection_score']:
                    if rand_value <= ga_data.population[idx + 1]['selection_score'] and \
                                        ga_data.population[idx] not in ga_data.parents:
                        ga_data.parents.append(deepcopy(ga_data.population[idx]))
                        break
                    else:
                        idx += 1
                else:
                    idx -= 1


    def execute(self, ga_data: GaData) -> None:
        super().execute(ga_data)
        self.add_probabilities(ga_data)
        self.balanced_selection(ga_data)
