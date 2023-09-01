import random
from typing import List, Union, Callable, Optional, Any
from baumeva.ga.support_funcs.support_functions import get_real_number_of_points, index_to_binary,\
     get_odd_num_children, get_result_mutation, sort_list_with_index, get_balanced_selection, get_index_from_gray
from baumeva.ga import Dynamic


class GA:

    def __init__(self,
                 opt_function: Union[Callable[[any, List[Union[int, float]]], Union[int, float]], Callable[
                               [List[Union[int, float]]], Union[int, float]]],
                 gen_parameters: dict,
                 num_generations: int,
                 num_individuals: int,
                 input_data: Any = None,
                 input_generation: Optional[List[List[Union[str, float]]]] = None,
                 input_generation_type: str = 'float',
                 penalty_method: any = None,
                 opt_function_value: Optional[Union[int, float]] = None,
                 is_binary_string: bool = True,
                 is_gray_code: bool = False,
                 percent_child: float = 0.9,
                 transfer_parents_type: str = 'best',
                 selection_type: str = 'tournament',
                 tournament_size: int = 3,
                 crossover_type: str = 'single_point',
                 mutation_value: Union[str, float] = 'normal',
                 early_stop: int = 10,
                 is_print=True
                 # random_seed=None - not implemented in current release
                 ):
        """
        Initialization class GA for generation parameters of genetics algorithm.
        :param opt_function: function to be solved, not fitness function! First argument is input data: any, second one
                             is gens: list[int|float]. Input data is not required in yours function, but if u have it,
                              u must fill input_data argument in GA.
                             Example with input_data:
                                def my_func(data: tuple, gens: list):
                                    return gens[0]*data[0] + gens[1]*data[1]
                            Example without input_data:
                                def my_func(gens: list):
                                    return gens[0]*2 + gens[1]*3
        :param opt_function_value: desired function value
        :param gen_parameters: dict - definition gens, example: {gen1(int): [min(float), max(float), step(float)],
                                                          gen2(int): ... }
        :param num_generations: int - number of generations
        :param penalty_method: subclass of PenaltyFunction(), initialization before initialization class BaumEva(),
                               used for conditional optimization.
                               Example: Dynamic([(my_conditional_func_1, 'inequal'), (my_conditional_func_2, 'equal)]).
                               Default: None.
        :param num_individuals: number of individuals
        :param input_data: any, input data in opt_function
        :param input_generation: list[list[str|float]] as num_individuals[num_gems['0' or '1']] - first generation from
                                 user
        :param input_generation_type: str - type of input data: 'binary_string', 'float'. Default: 'float'
        :param opt_function_value: int/float or None - desired function value. If it is None opt_function will be
                                   minimized, else opt_function will be pursuit to opt_function_value Default: None
        :param is_binary_string: bool - in current release can not be False, default: True
        :param is_gray_code: bool - default: False
        :param percent_child: float - percent children who will be in new generation, default: 0.9
        :param transfer_parents_type: str - type of transfer parents: "best", "random". Default: "best"
        :param selection_type: str - type of selection: "tournament", "balanced", "ranked". Default: "tournament"
        :param tournament_size: int - size of tournament, use only with selection_type="tournament". Default: 3
        :param crossover_type: str - types of crossover: "single_point", "double_point", "equable".
                               Default: "single_point"
        :param mutation_value: float or str - mutations gens with different parameters: float value: 0.01,...,0.99;
                               str value: 'weak', 'normal', 'strong';
                               default: 'normal'
        :param early_stop: int - early stopping criteria, number of generation without improve. Default: 25
        :param is_print: bool - printed results of genetic algorithm. Default: True.
        """

        self.opt_function = opt_function
        self.gen_parameters = gen_parameters
        self.num_generations = num_generations
        self.num_individuals = num_individuals
        self.input_data = input_data
        self.input_generation = input_generation
        self.input_generation_type = input_generation_type
        self.penalty_method = penalty_method
        self.opt_function_value = opt_function_value
        self.is_binary_string = is_binary_string
        self.is_gray_code = is_gray_code
        self.percent_child = percent_child
        self.transfer_parents_type = None if percent_child >= 1 else transfer_parents_type
        self.selection_type = selection_type
        self.tournament_size = tournament_size
        self.crossover_type = crossover_type
        self.mutation_value = mutation_value
        self.idx_generation = 0
        self.early_stop = early_stop
        self.is_print = is_print
        self.generation_no_up = 0
        # self.random_seed = random_seed
        self.len_bin_str = None
        self.best_solution = {'fitness_score': -2**31,
                              'bin_gens': [],
                              'real_gens': [],
                              'function_result': -2**31,
                              'idx_generation': self.idx_generation}
        self.best_score = []
        self.avg_score = []
        self.worst_score = []

    def get_penalty_value(self, gens_list: List[float]):
        if self.penalty_method is None:
            return 0
        elif isinstance(self.penalty_method, Dynamic):
            return self.penalty_method.calculate(gens_list, iter_generation=self.idx_generation)
        else:
            raise Exception(f'Unexpected penalty_method: {self.penalty_method}')

    def fitness_func(self, gens_list):
        """
        Fitness function witch return value from 0 to 1 or maximum.
        """
        if self.opt_function_value is None:
            if self.input_data:
                return -(self.opt_function(self.input_data, gens_list) + self.get_penalty_value(gens_list))
            else:
                return -(self.opt_function(gens_list) + self.get_penalty_value(gens_list))
        else:
            if self.input_data:
                return 1.0 / (1 + abs(self.opt_function_value - (self.opt_function(self.input_data, gens_list) +
                                                                 self.get_penalty_value(gens_list))))
            else:
                return 1.0 / (1 + abs(self.opt_function_value - (self.opt_function(gens_list)
                                                                 + self.get_penalty_value(gens_list))))

    def get_gen_parameters(self):
        """
        Function for definition parameters for each gen:
        - num_points: number of points
        - real_step
        - num_bits: number of bits
        - real_num_points: real number of points
        """
        idx_bits = [0]
        for gen in self.gen_parameters:
            gen_range = abs(self.gen_parameters[gen][1] - self.gen_parameters[gen][0])
            num_points = int(gen_range / self.gen_parameters[gen][2])
            self.gen_parameters[gen].append(num_points)  # 3 index
            if self.is_binary_string:
                num_bits, real_num_points = get_real_number_of_points(num_points)
                real_step = gen_range / (2 ** num_bits - 1)
                self.gen_parameters[gen].append(real_step)  # 4 index
                self.gen_parameters[gen].append(num_bits)  # 5 index
                self.gen_parameters[gen].append(real_num_points)  # 6 index
                idx_bits.append(idx_bits[-1] + num_bits)
        return idx_bits

    def check_input_generation(self) -> None:
        """
        Function for checking input data.
        :return: Exception or None
        """
        if type(self.input_generation) is list:
            if len(self.input_generation) > self.num_individuals:
                raise Exception(f'Number of individuals in input_generation: {len(self.input_generation)} > number of'
                                f' individuals in num_individuals: {self.num_individuals}')
            for inner_obj in self.input_generation:
                if type(inner_obj) is list:
                    if self.input_generation_type == 'binary_string' and len(inner_obj) != self.len_bin_str:
                        raise Exception(f'Length of binary genotype is not correct')
                    if self.input_generation_type == 'float' and len(inner_obj) != len(self.gen_parameters.keys()):
                        raise Exception(f'Length of genotype is not correct')
                    for gen in inner_obj:
                        if self.input_generation_type == 'binary_string' and type(gen) is not str:
                            raise Exception(f'Type of {gen} is not string')
                        elif self.input_generation_type == 'binary_string' and type(gen) is str:
                            if gen != '0' and gen != '1':
                                raise Exception(f'Gen {gen} is not equal "0" or "1"')
                        elif (self.input_generation_type == 'float') and\
                                ((type(gen) is not float) and (type(gen) is not int)):
                            raise Exception(f'Type of {gen} is not float or int')
            # return True
                else:
                    raise Exception(f'Type of {inner_obj} is not list')
        else:
            raise Exception(f'Type of {self.input_generation} is not list')

    def convert_to_gen_type(self) -> List[List[str]]:
        """
        Transformation input data to gen type
        :return: input_population: List[List[str]]
        """
        if self.input_generation_type == 'float':
            input_population = []
            for individ in self.input_generation:
                input_individ = ''
                for gen_idx, gen_value in enumerate(individ):
                    if gen_value < self.gen_parameters[gen_idx][0] or gen_value > self.gen_parameters[gen_idx][1]:
                        raise Exception(f'Gen: {gen_value} is out of range:'
                                        f' ({self.gen_parameters[gen_idx][0]}, {self.gen_parameters[gen_idx][1]})')
                    step_idx = round((gen_value - self.gen_parameters[gen_idx][0]) / self.gen_parameters[gen_idx][4])
                    input_individ += index_to_binary(value=step_idx, num_bits=self.gen_parameters[gen_idx][5],
                                                     is_graycode=self.is_gray_code)
                input_population.append(list(input_individ))
            return input_population
        else:
            return self.input_generation

    def first_generation(self, population):
        for i in range(self.num_individuals-len(population)):
            individual = ''
            for gen in self.gen_parameters:
                individual += index_to_binary(value=random.randint(0, self.gen_parameters[gen][6]),
                                              num_bits=self.gen_parameters[gen][5], is_graycode=self.is_gray_code)

            population.append(list(individual))
        return population

    def get_first_generation(self) -> List[List[str]]:
        """
        Generation first population.
        Return population: list of list string value (binary string)
        """
        population = []
        if self.input_generation:
            self.check_input_generation()
            population = self.convert_to_gen_type()
        population = self.first_generation(population)
        return population

    def bin_string_decoder(self, individ, idx_bits):
        """
        Decoding gens from binary string to real point.
        Return decoded gens as list.
        """
        gen_str = ''.join(individ)
        individ_decoded = []
        for gen_idx, gen_key in enumerate(self.gen_parameters):
            index_point = int(gen_str[idx_bits[gen_idx]:idx_bits[gen_idx + 1]], 2)
            if self.is_gray_code:
                index_point = get_index_from_gray(index_point)
            point = self.gen_parameters[gen_key][0] + index_point * self.gen_parameters[gen_key][4]
            individ_decoded.append(point)
        return individ_decoded

    def get_scores(self, population, idx_bits):
        """
        Get result fitness function for each individual.
        Return list of scores.
        """
        population_decoded = []
        for individ in population:
            individ_decoded = self.bin_string_decoder(individ=individ, idx_bits=idx_bits)
            population_decoded.append(individ_decoded)
        scores_list = []
        for gens_list in population_decoded:
            score = self.fitness_func(gens_list=gens_list)
            scores_list.append(score)
        return scores_list

    def tracking(self, scores_list, population, idx_bits):
        """
        Tracking best, average, worst solutions and other parameters for each generation
        """
        if max(scores_list) > self.best_solution['fitness_score']:
            self.best_score.append(max(scores_list))
            self.best_solution['fitness_score'] = max(scores_list)
            self.best_solution['bin_gens'] = population[scores_list.index(max(scores_list))]
            self.best_solution['real_gens'] = self.bin_string_decoder(individ=self.best_solution['bin_gens'],
                                                                      idx_bits=idx_bits)
            self.best_solution['function_result'] = self.opt_function(self.input_data, self.best_solution['real_gens'])\
                if self.input_data else self.opt_function(self.best_solution['real_gens'])
            self.best_solution['idx_generation'] = self.idx_generation
            self.generation_no_up = 0
        else:
            self.best_score.append(self.best_score[-1])
            self.generation_no_up += 1

        self.avg_score.append(sum(scores_list) / len(scores_list))
        self.worst_score.append(min(scores_list))

    def selection(self, population, scores_list):
        """
        Types of selection: "tournament", "balanced", "ranked".
        Return list of indexes selected parents by 'selection_type'
        """
        selected_idx_list = []
        num_children = get_odd_num_children(num_population=self.num_individuals,
                                            percent_children=self.percent_child)
        if self.selection_type == 'tournament':
            for j in range(num_children):
                tour_idx_list = random.sample(range(len(population)), self.tournament_size)
                tour_best_idx = tour_idx_list[-1]
                for i in range(self.tournament_size - 1):
                    if scores_list[tour_idx_list[i]] > scores_list[tour_best_idx]:
                        tour_best_idx = tour_idx_list[i]
                selected_idx_list.append(tour_best_idx)
        elif self.selection_type == 'balanced':
            selected_idx_list = get_balanced_selection(scores_list, num_children)
        elif self.selection_type == 'ranked':
            sorted_scores = sort_list_with_index(scores_list, reverse=False)
            equal_scores_total = {}
            equal_scores = []
            prev_score = -1
            for rank, inner_dict in enumerate(sorted_scores):
                inner_dict['rank'] = rank
                if inner_dict['value'] == prev_score:
                    equal_scores.append(rank-1)
                    equal_scores.append(rank)
                elif ((inner_dict['value'] != prev_score) and (len(equal_scores) > 0)) or\
                        ((rank == len(sorted_scores)-1) and (len(equal_scores) > 0)):
                    rank_value = int(sum(equal_scores)/len(equal_scores))
                    equal_scores_total[rank_value] = list(set(equal_scores))
                    equal_scores = []
                prev_score = inner_dict['value']

            for d_key_rank in equal_scores_total.keys():
                for rank in equal_scores_total[d_key_rank]:
                    sorted_scores[rank]['rank'] = d_key_rank

            sorted_scores.sort(key=lambda x: x['id'], reverse=False)
            rank_scores = [d['rank'] for d in sorted_scores]
            selected_idx_list = get_balanced_selection(rank_scores, num_children)
        else:
            raise Exception(f'Unexpected selection type: {self.selection_type},'
                            f' select one from ["tournament", "balanced", "ranked"]')
        return selected_idx_list

    def crossover(self, selected_idx_list, population):
        """
        Crossover selected parents.
        Types of crossover: "single_point", "double_point", "equable".
        Return children: list of binary strings.
        """
        children = []
        if self.crossover_type == 'single_point':
            for i in range(int(len(selected_idx_list) / 2)):
                single_point = random.randint(1, self.len_bin_str - 1)
                child_0 = population[selected_idx_list[-i - 1]][:single_point] + population[selected_idx_list[i]][
                                                                                 single_point:]
                child_1 = population[selected_idx_list[i]][:single_point] + population[selected_idx_list[-i - 1]][
                                                                            single_point:]
                children.append(child_0)
                children.append(child_1)
        elif self.crossover_type == 'double_point':
            for i in range(int(len(selected_idx_list) / 2)):
                point_list = [random.randint(1, self.len_bin_str - 1), random.randint(1, self.len_bin_str - 1)]
                while point_list[0] == point_list[1]:
                    point_list = [random.randint(1, self.len_bin_str - 1), random.randint(1, self.len_bin_str - 1)]
                point_list.sort()
                child_0 = population[selected_idx_list[i]][:point_list[0]] + population[
                          selected_idx_list[-i - 1]][point_list[0]:point_list[1]] + population[
                          selected_idx_list[i]][point_list[1]:]
                child_1 = population[selected_idx_list[-i - 1]][:point_list[0]] + population[
                          selected_idx_list[i]][point_list[0]:point_list[1]] + population[
                          selected_idx_list[-i - 1]][point_list[1]:]
                children.append(child_0)
                children.append(child_1)
        elif self.crossover_type == 'equable':
            for i in range(int(len(selected_idx_list) / 2)):
                child_0 = []
                child_1 = []
                for j in range(self.len_bin_str):
                    if population[selected_idx_list[i]][j] != population[selected_idx_list[-i - 1]][j]:
                        child_0.append(str(random.randint(0, 1)))
                        child_1.append(str(random.randint(0, 1)))
                    else:
                        child_0.append(population[selected_idx_list[i]][j])
                        child_1.append(population[selected_idx_list[i]][j])
                children.append(child_0)
                children.append(child_1)
        else:
            raise Exception(f'Unexpected crossover type: {self.crossover_type},'
                            f' select one from ["single_point", "double_point", "equable"]')
        return children

    def mutation(self, children, n_round=3):
        """
        Mutations gens with different parameters: float value: 0.01,...,0.99, 'weak', 'normal', 'strong'.
        :param children: list of binary strings.
        :param n_round: points of rounding.
        :return: children: list of binary strings with mutation.
        """
        if self.mutation_value == 'weak':
            probability = round(0.3 / self.len_bin_str, n_round)
        elif self.mutation_value == 'normal':
            probability = round(1 / self.len_bin_str, n_round)
        elif self.mutation_value == 'strong':
            probability = round(3 / self.len_bin_str, n_round)
        elif (type(self.mutation_value) is float) and (0 < self.mutation_value < 1):
            probability = round(self.mutation_value, n_round)
        else:
            raise Exception(f'Unused value for mutation: {self.mutation_value}, '
                            f'use please float value from 0 to 1 or "weak"/"normal"/"strong"')
        for child in children:
            for i, gen in enumerate(child):
                is_mutation = get_result_mutation(probability=probability, sample=10 * n_round)
                if is_mutation:
                    if gen == '0':
                        child[i] = '1'
                    else:
                        child[i] = '0'
        return children

    def new_generation(self, children, population, scores_list):
        """
        Function for define new generation.
        Types of transfer parents: "best", "random".
        Return children list with transferred parents
        """
        children.append(self.best_solution['bin_gens'])
        if self.transfer_parents_type is not None:
            free_slots = self.num_individuals - len(children)
            if free_slots > 0 and self.transfer_parents_type == 'best':
                scores_sorted_list = sort_list_with_index(value_list=scores_list)
                i = 0

                non_equal = 0
                for idx in range(len(scores_sorted_list)-1):
                    if scores_sorted_list[idx]['value'] != scores_sorted_list[idx+1]['value']:
                        non_equal += 1

                while len(children) < self.num_individuals:
                    if free_slots <= non_equal:
                        if population[scores_sorted_list[i]['id']] != self.best_solution['bin_gens']:
                            children.append(population[scores_sorted_list[i]['id']])
                    else:
                        children.append(population[scores_sorted_list[i]['id']])
                    i += 1
            if free_slots > 0 and self.transfer_parents_type == 'random':
                while len(children) < self.num_individuals:
                    individual = random.choice(population)
                    if individual != self.best_solution['bin_gens']:
                        children.append(individual)
        return children

    def optimize(self):
        """
        Main function of Genetic Algorithm.
        Returns:
            best_solution -> dict of the best solution overall
            best_score -> list of the best solution every generation
            avg_score -> list of the average solution every generation
            worst -> list of the worst solution every generation
        """
        idx_bits = self.get_gen_parameters()
        self.len_bin_str = idx_bits[-1]
        # print(f'idx_bits: {idx_bits}')
        if not self.is_binary_string:
            raise Exception('Non-binary string is not supported in this version')
        population = self.get_first_generation()
        scores_list = self.get_scores(population, idx_bits)
        self.tracking(scores_list, population, idx_bits)
        for i in range(self.num_generations - 1):

            self.idx_generation += 1
            selected_idx_list = self.selection(population, scores_list)
            children = self.crossover(selected_idx_list, population)
            children = self.mutation(children)
            children = self.new_generation(children, population, scores_list)
            population = children
            scores_list = self.get_scores(population, idx_bits)
            self.tracking(scores_list, population, idx_bits)
            if self.is_print:
                print('-'*65)
                print(f'Generation {i+1}:')
                print(f'Best fitness scores: {self.best_score[-1]}')
            # print('Generation_no_up', self.generation_no_up)
            if self.generation_no_up >= self.early_stop:
                print(f'Early stop: {self.early_stop} rounds without improving, index stopped generation - {i + 1}.')
                break
        print('-'*65)
        if self.is_print:
            self.print_result()

        return self.best_solution, self.best_score, self.avg_score, self.worst_score

    def print_result(self, is_print_all=False):
        """
        Function for show results of GA.
        """
        for key_dict in self.best_solution:
            print(f'{key_dict}: {self.best_solution[key_dict]}')
        if is_print_all:
            print(f'List of the best scores: {self.best_score}')
            print(f'List of average scores: {self.avg_score}')
            print(f'List of the worst scores: {self.worst_score}')
