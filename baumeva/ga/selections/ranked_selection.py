from .balanced_selection import BalancedSelection
from baumeva.ga import GaData


class RankedSelection(BalancedSelection):
    """
    Class for implementing ranked selection in a genetic algorithm.
    Inherits from BalancedSelection.
    """

    score_type = 'rank'

    def __init__(self):
        """
        Initialize the RankedSelection instance.

        :return: None
        """
        super().__init__()

    def add_probabilities(self, ga_data: GaData):
        """
        Calculate ranks and selection probabilities based on individuals' scores.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        prev_score = -1
        count = 1
        for idx in range(len(ga_data.population)):
            rank = idx + 1
            ga_data.population[idx]['rank'] = rank
            if ga_data.population[idx]['score'] == prev_score:
                count += 1
                if rank == len(ga_data.population):
                    for _idx in range(rank - count, rank):
                        ga_data.population[_idx]['rank'] = (sum(range(rank - count, rank)) + count) / count
            elif count > 1:
                for _idx in range(idx - count, idx):
                    ga_data.population[_idx]['rank'] = (sum(range(idx - count, idx)) + count) / count
                count = 1
            prev_score = ga_data.population[idx]['score']
        super().add_probabilities(ga_data)

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the selection operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        super().execute(ga_data)
