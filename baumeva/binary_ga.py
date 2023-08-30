from typing import List, Callable, Union, Any
from .ga import GaData, BinaryPopulation, BinaryGrayPopulation, HyperbolaFitness, PenaltyFunction, TournamentSelection,\
                OnePointCrossover, BinStringMutation, NewGeneration


class BinaryGA:
    """
    Class for perform binary genetic algorithm.
    """
    def __init__(self, num_generations: int, num_individ: int, gens: tuple, obj_function: Callable,
                 obj_value: Union[int, float] = None, input_data: Any = None, penalty: PenaltyFunction = None,
                 is_gray: bool = False, children_percent: float = 0.95, early_stop: int = 10,
                 input_population: List[list] = None, tournament_size: int = 3,
                 mutation_lvl: Union[str, float] = 'normal', transfer_parents: str = 'best') -> None:
        """
        Initialization CombinatoryGA with next parameters:
        :param num_generations: int, number of generations;
        :param num_individ: int, number of individuals in generation (size of population);
        :param gens: tuple, tuple of 3 integer value, example: (0, 9, 10), 0 - first categorical value,
                     9 - last categorical value, step between categorical is 1 (const), 10 - number of categorical
                     values in every individ, u can use value in range 9-0+1 = 10;
        :param obj_function: Callable, object function with 1 or 2 arguments, my_func(gens: list) or
                             my_func(input_data: Any, gens: list);
        :param obj_value: int | float, default: None. If object value exists, GA will optimize to the value,
                          else GA will optimize to min;
        :param input_data: Any, default: None. Argument for object function;
        :param penalty: PenaltyFunction, default: None. Subclass of PenaltyFunction(), initialization before
                        initialization class CombinatoryGA(), used for conditional optimization.
                        Example: Dynamic([(my_conditional_func_1, 'inequal'), (my_conditional_func_2, 'equal)]);
        :param is_gray: bool, default: False. Ability to use gray code instead of binary representation;
        :param children_percent: float, default: 0.95. Percent of children who will be in new generation;
        :param early_stop: int, default: 10. Early stopping criteria, number of generation without improve;
        :param input_population: list[list], default: None. First generation from user;
        :param tournament_size: int, default: 3. Size of tournament, use only with selection_type="tournament";
        :param mutation_lvl: str | float, default: 'normal'. Mutations gens with different parameters:
                             float value: 0.00,...,1.00;
                             str value: 'weak', 'normal', 'strong';
        :param transfer_parents: str, default: "best". Type of transfer parents: "best", "random"
        :return None
        """
        self.num_generations = num_generations
        self.num_individ = num_individ
        self.gens = gens
        self.obj_function = obj_function
        self.obj_value = obj_value
        self.input_data = input_data
        self.penalty = penalty
        self.is_gray = is_gray
        self.children_percent = children_percent
        self.early_stop = early_stop
        self.input_population = input_population
        self.tournament_size = tournament_size
        self.mutation_lvl = mutation_lvl
        self.transfer_parents = transfer_parents

    def optimize(self) -> GaData:
        """
        Main method of CombinatoryGA().
        :return: GaData
        """
        # init GaData & Population
        ga_data = GaData(num_generations=self.num_generations, children_percent=self.children_percent,
                         early_stop=self.early_stop)
        if self.is_gray:
            population = BinaryGrayPopulation()
        else:
            population = BinaryPopulation()

        population.set_params(num_individ=self.num_individ, gens=self.gens, input_population=self.input_population)
        # init fitness func, selection, crossover, mutation, new generation
        fitness_func = HyperbolaFitness(obj_function=self.obj_function, obj_value=self.obj_value,
                                        input_data=self.input_data, penalty=self.penalty)
        selection = TournamentSelection(tournament_size=self.tournament_size)
        cross = OnePointCrossover()
        mutation = BinStringMutation(mutation_lvl=self.mutation_lvl)
        new_generation = NewGeneration(transfer_parents=self.transfer_parents)
        # creating first generation
        population.fill()
        ga_data.population = population
        fitness_func.execute(ga_data=ga_data)
        ga_data.update()
        # main loop for GA perform
        for i in range(ga_data.num_generations):

            selection.execute(ga_data)
            cross.execute(ga_data)
            mutation.execute(ga_data)
            new_generation.execute(ga_data)
            fitness_func.execute(ga_data)
            ga_data.update()

            if ga_data.num_generation_no_improve >= ga_data.early_stop:
                print('|=============================================================================================|')
                print(f'Early stopping: {i}')
                print('Best solution:')
                print(f'\tgenotype: {ga_data.best_solution["genotype"]}')
                print(f'\tfitness score: {ga_data.best_solution["score"]}')
                print(f'\tobjective score: {ga_data.best_solution["obj_score"]}')
                break
        return ga_data
