from .balanced_selection import BalancedSelection
from baumeva.ga import MultiGaData


class VEGABalancedSelection(BalancedSelection):
    """
    Class for implementing balanced selection for multiobjective optimization with the VEGA algorithm.
    Inherits from BalancedSelection.
    """

    idx: int = 0

    def __init__(self, num_objectives: int):
        """
        Initialize the VEGABalancedSelection instance.

        :param num_objectives: The number of objectives.
        :return: None
        """
        self.num_objectives = num_objectives
        super().__init__()

    def get_total_num_parents(self, ga_data: MultiGaData) -> int:
        """
        Method for calculation the total number of parents to select.

        :param ga_data: MultiGaData instance containing population and related data.
        :return: total number of parents.
        """
        return int(ga_data.children_percent * ga_data.population.num_individ / self.num_objectives)

    def add_probabilities(self, ga_data: MultiGaData):
        """
        Calculate and store selection probabilities based on individuals' scores.

        :param ga_data: MultiGaData instance containing population and related data.
        :return: None
        """
        self.selection_scores = [0]
        sum_scores = sum(ind[self.score_type][self.idx] for ind in ga_data.population)
        proportional = 0

        for ind in ga_data.population:
            proportional += ind[self.score_type][self.idx] / sum_scores
            self.selection_scores.append(proportional)

    def execute(self, ga_data: MultiGaData) -> None:
        """
        Execute the balanced selection operation.

        :param ga_data: MultiGaData instance containing population and related data.
        :return: None
        """
        for self.idx in range(self.num_objectives):
            super().execute(ga_data)
