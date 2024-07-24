from copy import deepcopy
from typing import List, Union
from .ga_data import GaData


class MultiGaData(GaData):
    """
    Class for holding and managing data related to a genetic algorithm run in multiple objective optimization case.
    """

    def __init__(self, num_generations: int, children_percent: float = 0.95, early_stop: int = 10) -> None:
        """
        Initialize the MultiGaData instance.

        :param num_generations: number of generations the genetic algorithm will run.
        :param children_percent: percentage of children to be created as part of new offsprings.
        :param early_stop: number of consecutive generations with no improvement to trigger early stopping.
        :return: None
        """
        super().__init__(num_generations, children_percent, early_stop)

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
        Update the MultiGaData instance with information about the current generation.

        :return: None
        """

        if not self.population.is_sorted:
            self.population.sort_by_dict('rank')

        pareto_set = []
        for individ in self.population:
            if individ['rank'] == 1:
                pareto_set.append(individ)
            else:
                break

        self.historical_best.append(pareto_set)

        if self.best_solution is None:
            self.best_solution = {'pareto_set':[]}

        if self.best_solution['pareto_set'] != pareto_set:
            self.best_solution['pareto_set'] = deepcopy(pareto_set)
            self.best_solution['idx_generation'] = self.idx_generation
            self.num_generation_no_improve = 0
        else:
            self.num_generation_no_improve += 1

        self.idx_generation += 1

    @staticmethod
    def print_list(head, lst, label) -> None:
        print(f'\t{head}:')
        for elem in lst:
            print(f'\t\t{elem[label]}')

    def print_best_solution(self) -> None:
        """
        Method for print params of the best individ.
        :return: None
        """
        print('|' + '=' * 85 + '|')
        print(f'Index generation: {self.idx_generation - 1}')
        print('Best solution:')
        print(f'\tindex generation: {self.best_solution["idx_generation"]}')
        # print(f'\tgenotypes: {self.best_solution["genotype"]}')
        # if 'phenotype' in self.best_solution.keys():
        self.print_list('phenotypes', self.best_solution["pareto_set"], 'phenotype')
        # print(f'\tfitness score: {self.best_solution["score"]}')
        self.print_list('objective scores', self.best_solution["pareto_set"], 'obj_score')
        # print(f'\tfeasible region: {self.best_solution["feasible"]}')
