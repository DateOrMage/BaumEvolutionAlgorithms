from copy import deepcopy
from .populations import BasePopulation


class GaData:
    """
    Class for holding and managing data related to a genetic algorithm run.

    Attributes:
        idx_generation (int): Index of the current generation.
        num_generation_no_improve (int): Number of consecutive generations with no improvement.
        population (BasePopulation): Current population of individuals.
        parents (BasePopulation): Selected parent individuals for crossover.
        children (BasePopulation): Offspring individuals produced by crossover.
        historical_best (list): List of historical best scores for each generation.
        historical_mediocre (list): List of historical average scores for each generation.
        historical_worst (list): List of historical worst scores for each generation.
        best_solution (dict): Dictionary representing the best individual solution found so far.

    Methods:
        get_avg_score()
        update()
    """
    idx_generation: int = 0
    num_generation_no_improve: int = 0
    population: BasePopulation = None
    parents: BasePopulation = None
    children: BasePopulation = None
    historical_best: list = None
    historical_mediocre: list = None
    historical_worst: list = None
    best_solution: dict = None

    def __init__(self, num_generations: int, children_percent: float = 0.95, early_stop: int = 10) -> None:
        """
        Initialize the GaData instance.

        :param num_generations: number of generations the genetic algorithm will run.
        :param children_percent: percentage of children to be created as part of new offsprings.
        :param early_stop: number of consecutive generations with no improvement to trigger early stopping.
        :return: None
        """
        self.num_generations = num_generations
        self.early_stop = early_stop
        self.children_percent = children_percent
        self.historical_best = []
        self.historical_mediocre = []
        self.historical_worst = []

    def get_avg_score(self) -> float:
        """
        Calculate and return the average score of the current population.

        :return: аverage score of the population.
        """
        avg = 0
        for individ in self.population:
            avg += individ['score']
        avg /= len(self.population)
        return avg

    def update(self) -> None:
        """
        Update the GaData instance with information about the current generation.

        :return: None
        """
        if not self.population.is_sorted:
            self.population.sort_by_dict()

        self.historical_best.append(self.population[-1]['score'])
        self.historical_mediocre.append(self.population[int(len(self.population)/2)]['score'])
        self.historical_worst.append(self.population[0]['score'])

        if self.best_solution is None:
            self.best_solution = deepcopy(self.population[-1])
            self.best_solution['idx_generation'] = self.idx_generation

        elif self.best_solution['score'] < self.population[-1]['score']:
            self.best_solution = deepcopy(self.population[-1])
            self.best_solution['idx_generation'] = self.idx_generation
            self.num_generation_no_improve = 0
        else:
            self.num_generation_no_improve += 1

        self.idx_generation += 1

    def print_best_solution(self) -> None:
        """
        Method for print params of the best individ.
        :return: None
        """
        print('|' + '=' * 85 + '|')
        print(f'Index generation: {self.idx_generation-1}')
        print('Best solution:')
        print(f'\tindex generation: {self.best_solution["idx_generation"]}')
        print(f'\tgenotype: {self.best_solution["genotype"]}')
        if 'phenotype' in self.best_solution.keys():
            print(f'\tphenotype: {self.best_solution["phenotype"]}')
        print(f'\tfitness score: {self.best_solution["score"]}')
        print(f'\tobjective score: {self.best_solution["obj_score"]}')
        print(f'\tfeasible region: {self.best_solution["feasible"]}')
