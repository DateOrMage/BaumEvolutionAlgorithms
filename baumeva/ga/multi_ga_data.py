from copy import deepcopy
from .populations import BasePopulation
from typing import Union
from itertools import cycle
from .ga_data import GaData


class MultiGaData(GaData):
    """
    Class for holding and managing data related to a genetic algorithm run in multiple objective optimization case.
    """

    def __init__(self, num_obj_functions: int, num_generations: int, children_percent: float = 0.95, early_stop: int = 10, obj_function = None) -> None:
        """
        Initialize the MultiGaData instance.

        :param num_obj_functions: number of objectives.
        :param num_generations: number of generations the genetic algorithm will run.
        :param children_percent: percentage of children to be created as part of new offsprings.
        :param early_stop: number of consecutive generations with no improvement to trigger early stopping.
        :return: None
        """
        self.num_obj_functions = num_obj_functions
        super().__init__(num_generations, children_percent, early_stop)
        self.obj_function = obj_function

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

    def inferior(self, x: dict, y: dict) -> Union[dict, None]:
        """
        Computes the inferior of 2 individuals

        :param x: dict, first individual data.
        :param y: dict, second individual data.
        :return: dict, containing the inferior of x and y if there is one, None if there are no inferior individuals
        """
        x_score = list(self.obj_function(x['phenotype']))
        y_score = list(self.obj_function(y['phenotype']))

        if x_score == y_score:
            return None

        max_score = x_score.copy()
        for i in range(len(y_score)):
            if max_score[i] < y_score[i]:
                max_score[i] = y_score[i]

        if max_score == x_score:
            return x
        elif max_score == y_score:
            return y
        else:
            return None

    def assign_ranks(self) -> None:
        """
        Assigns a rank to every individual in population equal to 1 + number of individuals dominating it

        :return: None
        """
        for individ in self.population:
            individ['rank'] = 1

        for i in range(len(self.population)):
            for j in range(i+1, len(self.population)):
                inf = self.inferior(self.population[i], self.population[j])
                if inf is not None:
                    inf['rank'] += 1

    def update(self) -> None:
        """
        Update the MultiGaData instance with information about the current generation.

        :return: None
        """

        self.assign_ranks()

        if not self.population.is_sorted:
            self.population.sort_by_dict('rank')

        best_pareto = []
        phenotypes = []
        for individ in self.population:
            if individ['rank'] == 1:
                # best_pareto.append(str(spec['phenotype']) + ': ' + str(self.obj_function(spec['phenotype'])[:self.num_obj_functions]))
                best_pareto.append(self.obj_function(individ['phenotype'])[:self.num_obj_functions])
                phenotypes.append(individ['phenotype'])
            else:
                break

        self.historical_best.append(best_pareto)
        self.historical_mediocre.append(phenotypes)

        # if self.best_solution is None:
        #     self.best_solution = deepcopy(self.population[-1])
        #     self.best_solution['idx_generation'] = self.idx_generation
        #
        # elif self.best_solution['score'] < self.population[-1]['score']:
        #     self.best_solution = deepcopy(self.population[-1])
        #     self.best_solution['idx_generation'] = self.idx_generation
        #     self.num_generation_no_improve = 0
        # else:
        #     self.num_generation_no_improve += 1
        #
        self.idx_generation += 1

    def print_best_solution(self) -> None:
        """
        Method for print params of the best individ.
        :return: None
        """
        print('|' + '=' * 85 + '|')
        print(f'Index generation: {self.idx_generation - 1}')
        for i, elem in enumerate(self.historical_mediocre):
            print(str(i)+': '+str(elem))
        #print(self.historical_best)
        # print('Best solution:')
        # print(f'\tindex generation: {self.best_solution["idx_generation"]}')
        # print(f'\tgenotype: {self.best_solution["genotype"]}')
        # if 'phenotype' in self.best_solution.keys():
        #     print(f'\tphenotype: {self.best_solution["phenotype"]}')
        # print(f'\tfitness score: {self.best_solution["score"]}')
        # print(f'\tobjective score: {self.best_solution["obj_score"]}')
        # print(f'\tfeasible region: {self.best_solution["feasible"]}')