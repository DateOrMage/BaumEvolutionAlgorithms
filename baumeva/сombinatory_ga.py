from typing import List, Callable, Union, Any
from .ga import GaData, OrderCatPopulation, HyperbolaFitness, PenaltyFunction, TournamentSelection, OrderCrossover,\
                InversionMutation, NewGeneration


class CombinatoryGA:
    def __init__(self, num_generations: int, num_individ: int, gens: tuple, obj_function: Callable,
                 obj_value: Union[int, float] = None, input_data: Any = None, penalty: PenaltyFunction = None,
                 children_percent: float = 0.9, early_stop: int = 10, input_population: List[list] = None,
                 tournament_size: int = 3, mutation_lvl: Union[str, float] = 'normal', transfer_parents: str = 'best')\
                 -> None:
        self.num_generations = num_generations
        self.num_individ = num_individ
        self.gens = gens
        self.obj_function = obj_function
        self.obj_value = obj_value
        self.input_data = input_data
        self.penalty = penalty
        self.children_percent = children_percent
        self.early_stop = early_stop
        self.input_population = input_population
        self.tournament_size = tournament_size
        self.mutation_lvl = mutation_lvl
        self.transfer_parents = transfer_parents

    def optimize(self) -> GaData:
        ga_data = GaData(num_generations=self.num_generations, children_percent=self.children_percent,
                         early_stop=self.early_stop)
        population = OrderCatPopulation()
        population.set_params(num_individ=self.num_individ, gens=self.gens, input_population=self.input_population)

        fitness_func = HyperbolaFitness(obj_function=self.obj_function, obj_value=self.obj_value,
                                        input_data=self.input_data, penalty=self.penalty)
        selection = TournamentSelection(tournament_size=self.tournament_size)
        cross = OrderCrossover()
        mutation = InversionMutation(mutation_lvl=self.mutation_lvl)
        new_generation = NewGeneration(transfer_parents=self.transfer_parents)

        population.fill()
        ga_data.population = population
        fitness_func.execute(data=ga_data)
        ga_data.update()

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


