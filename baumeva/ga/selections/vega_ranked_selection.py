from .vega_balanced_selection import VEGABalancedSelection
from baumeva.ga import MultiGaData


class VEGARankedSelection(VEGABalancedSelection):
    """
    Class for implementing ranked selection for multiobjective optimization with the VEGA algorithm.
    Inherits from VEGABalancedSelection.
    """

    score_type = 'rank'

    def __init__(self, num_objectives: int):
        """
        Initializes the VEGARankedSelection instance.

        :return: None
        """
        super().__init__(num_objectives)

    def add_probabilities(self, ga_data: MultiGaData):
        """
        Calculates ranks and selection probabilities based on individuals' scores.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        prev_score = -1
        count = 1
        for idx in range(len(ga_data.population)):
            rank = idx + 1
            ga_data.population[idx]['rank'][self.idx] = rank
            if ga_data.population[idx]['score'][self.idx] == prev_score:
                count += 1
                if rank == len(ga_data.population):
                    for _idx in range(rank - count, rank):
                        ga_data.population[_idx]['rank'][self.idx] = (sum(range(rank - count, rank)) + count) / count
            elif count > 1:
                for _idx in range(idx - count, idx):
                    ga_data.population[_idx]['rank'][self.idx] = (sum(range(idx - count, idx)) + count) / count
                count = 1
            prev_score = ga_data.population[idx]['score'][self.idx]
        super().add_probabilities(ga_data)

    def execute(self, ga_data: MultiGaData) -> None:
        """
        Executes the selection operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        for ind in ga_data.population:
            ind['rank'] = [0]*self.num_objectives

        super().execute(ga_data)
