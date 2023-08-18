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
    selection_scores = [0]

    def __init__(self):
        """
        Initialize the BalancedSelection instance.

        :return: None
        """
        pass

    def add_probabilities(self, ga_data: GaData):
        """
        Calculate and store selection probabilities based on individuals' scores.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        self.selection_scores = [0]
        sum_scores = sum(ind[self.score_type] for ind in ga_data.population)
        proportional = 0

        for ind in ga_data.population:
            proportional += ind[self.score_type] / sum_scores
            self.selection_scores.append(proportional)

    def get_index(self):
        """
        Get the index of a selected individual using proportional selection.

        :return: The index of the selected individual.
        """
        rand_value = random()
        idx = min(range(len(self.selection_scores)), key=lambda i: abs(self.selection_scores[i] - rand_value))
        return idx if rand_value >= self.selection_scores[idx] else idx - 1

    def balanced_selection(self, ga_data: GaData):
        """
        Perform balanced selection to choose parents for crossover.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        total_num_parents = int(ga_data.children_percent * ga_data.population.num_individ)

        for _ in range(total_num_parents):
            idxs = []
            while len(idxs) < 2:
                idx = self.get_index()
                if len(idxs) == 0 or idx != idxs[-1]:
                    idxs.append(idx)

            ga_data.parents.extend(deepcopy(ga_data.population[idx]) for idx in idxs)

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the balanced selection operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        super().execute(ga_data)
        self.add_probabilities(ga_data)
        self.balanced_selection(ga_data)
