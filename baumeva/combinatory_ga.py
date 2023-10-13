from typing import List, Callable, Union, Any
from .ga import GaData, OrderCatPopulation, HyperbolaFitness, BasePenalty, TournamentSelection, OrderCrossover,\
                MovementMutation, NewGeneration


class CombinatoryGA:
    """
    Class for perform combinatory genetic algorithm (categorical order combinations without repetitions).
    """
    def __init__(self, num_generations: int, num_individ: int, gens: tuple, obj_function: Callable,
                 obj_value: Union[int, float] = None, input_data: Any = None, penalty: BasePenalty = None,
                 conditions: list = None, children_percent: float = 0.95, early_stop: Union[int, None] = 10,
                 input_population: List[list] = None, tournament_size: int = 3,
                 mutation_lvl: Union[str, float] = 'normal', transfer_parents: str = 'best',
                 is_print: bool = True) -> None:
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
        :param penalty: BasePenalty, default: None. Subclass of BasePenalty(), initialization before
                        initialization subclass of BaseFitness(), used for conditional optimization.
                        Example: DynamicPenalty();
        :param conditions: list of strings (optimizer and conditionals) 3 value can be use: 'optimize', '<=', '!='.
                           Default: None.
                           Example: There is objective function: my_obj_func(x1, x2):
                                                                    return x1**2 + x2**2, 1-x1+x2, x1+x2
                                    my_obj_func returns 3 values, first value to optimize, second value must be <= 0,
                                    third value != 0, so have conditions = ['optimize', '<=', '!=']
        :param children_percent: float, default: 0.9. Percent of children who will be in new generation;
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
        self.conditions = conditions
        self.children_percent = children_percent
        self.early_stop = early_stop if early_stop is not None else num_generations
        self.input_population = input_population
        self.tournament_size = tournament_size
        self.mutation_lvl = mutation_lvl
        self.transfer_parents = transfer_parents
        self.is_print = is_print

    def optimize(self) -> GaData:
        """
        Main method of CombinatoryGA().
        :return: GaData
        """
        # init GaData & Population
        ga_data = GaData(num_generations=self.num_generations, children_percent=self.children_percent,
                         early_stop=self.early_stop)
        population = OrderCatPopulation()
        population.set_params(num_individ=self.num_individ, gens=self.gens, input_population=self.input_population)
        # init fitness func, selection, crossover, mutation, new generation
        fitness_func = HyperbolaFitness(obj_function=self.obj_function, obj_value=self.obj_value,
                                        input_data=self.input_data, penalty=self.penalty, conditions=self.conditions)
        selection = TournamentSelection(tournament_size=self.tournament_size)
        cross = OrderCrossover()
        mutation = MovementMutation(mutation_lvl=self.mutation_lvl)
        new_generation = NewGeneration(transfer_parents=self.transfer_parents)
        # creating first generation
        population.fill()
        ga_data.population = population
        fitness_func.execute(ga_data=ga_data)
        ga_data.update()
        # main loop for GA perform
        for i in range(1, ga_data.num_generations):

            selection.execute(ga_data)
            cross.execute(ga_data)
            mutation.execute(ga_data)
            new_generation.execute(ga_data)
            fitness_func.execute(ga_data)
            ga_data.update()

            if ga_data.num_generation_no_improve > ga_data.early_stop:
                break

        if self.is_print:
            ga_data.print_best_solution()
        return ga_data
