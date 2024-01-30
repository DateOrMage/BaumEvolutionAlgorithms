from random import sample
from copy import deepcopy
from .base_selection import BaseSelection
from baumeva.ga import GaData


class TournamentSelection(BaseSelection):
    """
    Class for implementing tournament selection in a genetic algorithm.
    Inherits from BaseSelection.
    """

    def __init__(self, tournament_size: int = 3):
        """
        Initialize the TournamentSelection instance.

        :param tournament_size: The size of each tournament (default: 3).
        :return: None
        """
        self.tournament_size = tournament_size

    def check_tournament_size(self, num_individ: int) -> None:
        """
        Check if the tournament size is valid, it should be more than 2 and less than number of individuals.

        :param num_individ: The number of individuals in the population.
        :return: None
        """
        if self.tournament_size < 2 or self.tournament_size >= num_individ:
            raise Exception(f'Size of tournament must be >= 2 and <= number of individuals: '
                            f'{num_individ}, but was given: {self.tournament_size}')

    @staticmethod
    def get_best(tournament: list, ga_data: GaData):
        """
        Get the best individual from a tournament.

        :param tournament: List of indices representing the tournament participants.
        :param ga_data: GaData instance containing population and related data.
        :return: The best individual from the tournament.
        """
        best = ga_data.population[tournament[0]]
        for idx in tournament[1:]:
            if ga_data.population[idx]['score'] > best['score']:
                best = ga_data.population[idx]
        return best

    def tournament(self, ga_data: GaData) -> None:
        """
        Perform the tournament selection process. At the end n (ga_data.children_percent *
            * ga_data.population.num_individ for now) parents selected.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        idx_total = list(range(len(ga_data.population)))
        total_num_parents = int(ga_data.children_percent*ga_data.population.num_individ)
        for i in range(total_num_parents):
            parents_pair = []
            while len(parents_pair) < 2:
                tournament = sample(idx_total, self.tournament_size)
                best = self.get_best(tournament, ga_data)
                if len(parents_pair) == 0 or best['idx_individ'] != parents_pair[0]['idx_individ']:
                    parents_pair.append(best)

            ga_data.parents.extend(deepcopy(parent) for parent in parents_pair)

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the tournament selection operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        self.check_tournament_size(num_individ=ga_data.population.num_individ)
        super().execute(ga_data)
        self.tournament(ga_data)
