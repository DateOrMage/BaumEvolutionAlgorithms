from .populations import BasePopulation


class GaData:
    idx_generation: int = 0
    num_generation_no_improve: int = 0
    population: BasePopulation = None
    parents: BasePopulation = None
    children: BasePopulation = None
    historical_best: list = []
    historical_mediocre: list = []
    historical_worst: list = []
    best_solution: dict = None

    def __init__(self, num_generations: int, children_percent: float = 0.9, transfer_parents: str = 'best',
                 early_stop: int = 10) -> None:
        self.num_generations = num_generations
        self.early_stop = early_stop
        self.children_percent = children_percent
        self.transfer_parents = transfer_parents

    def get_avg_score(self) -> float:
        avg = 0
        for individ in self.population:
            avg += individ['score']
        avg /= len(self.population)
        return avg

    def update(self) -> None:
        if not self.population.is_sorted:
            self.population.sort_by_dict()

        self.historical_best.append(self.population[-1]['score'])
        self.historical_mediocre.append(self.get_avg_score())
        self.historical_worst.append(self.population[0]['score'])

        if self.best_solution is None:
            self.best_solution = self.population[-1]
            self.best_solution['idx_generation'] = self.idx_generation

        elif self.best_solution['score'] < self.population[-1]['score']:
            self.best_solution = self.population[-1]
            self.best_solution['idx_generation'] = self.idx_generation
            self.num_generation_no_improve = 0
        else:
            self.num_generation_no_improve += 1

        self.idx_generation += 1

