from .populations import BasePopulation


class GaData:
    idx_generation: int = 0
    population: BasePopulation = None
    children: BasePopulation = None
    historical_best: list = []
    historical_mediocre: list = []
    historical_worst: list = []
    best_solution: dict = {}

    def update(self):
        if not self.population.is_sorted:
            self.population.sort_by_dict()
        self.historical_best.append(self.population[-1]['score'])
        self.historical_worst.append(self.population[0]['score'])

