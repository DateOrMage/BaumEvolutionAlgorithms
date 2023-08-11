from random import sample
from copy import deepcopy
from .base_selection import BaseSelection
from baumeva.ga import GaData


class TournamentSelection(BaseSelection):
    def __init__(self, tournament_size: int = 3):
        self.tournament_size = tournament_size

    def check_tournament_size(self, num_individ: int) -> None:
        if self.tournament_size < 2 or self.tournament_size > num_individ:
            raise Exception(f'Size of tournament must be >= 2 and <= number of individuals: '
                            f'{num_individ}, but was given: {self.tournament_size}')

    @staticmethod
    def get_best(tournament: list, ga_data: GaData):
        best = ga_data.population[tournament[0]]
        for idx in tournament[1:]:
            if ga_data.population[idx]['score'] > best['score']:
                best = deepcopy(ga_data.population[idx])
        return best

    def tournament(self, ga_data: GaData) -> BaseSelection:
        idx_total = list(range(ga_data.population.num_individ))
        selected_parents = ga_data.population.get_empty_copy()
        total_num_parents = int(ga_data.children_percent*ga_data.population.num_individ)
        for i in range(total_num_parents):
            if len(idx_total) >= self.tournament_size:
                tournament = sample(idx_total, self.tournament_size)
            else:
                tournament = idx_total
            best = self.get_best(tournament, ga_data)
            idx_total.remove(best['idx_individ'])
            selected_parents.append(best)

        return selected_parents

    def execute(self, ga_data: GaData) -> None:

        self.check_tournament_size(num_individ=ga_data.population.num_individ)
        ga_data.population.reset_idx_individ()
        ga_data.parents = self.tournament(ga_data)

