from typing import List, Type
from .ga import (GaData, MultiGaData, BasePopulation, BaseFitness, BaseSelection, BaseCrossover, BaseMutation,
                 NewGeneration)


class CollectorGA:
    """
    Class for collection unique GA.
    ga_data: Class for holding and managing data related to a genetic algorithm run.
    """
    ga_data: GaData = None

    def __init__(self,
                 fitness: BaseFitness,
                 selection: BaseSelection,
                 crossover: BaseCrossover,
                 mutation: BaseMutation,
                 new_generation: NewGeneration,
                 storage: Type[GaData] = GaData) -> None:
        """
        Initialization CollectorGA with next parameters:
        :param fitness: initialized subclass of BaseFitness;
        :param selection: initialized subclass of BaseSelection;
        :param crossover: initialized subclass of BaseCrossover;
        :param mutation: initialized subclass of BaseMutation;
        :param new_generation: initialized class NewGeneration;
        :param storage: subclass of GaData;
        """
        self.fitness = fitness
        self.selection = selection
        self.crossover = crossover
        self.mutation = mutation
        self.new_generation = new_generation
        self.storage = storage

    def set_population(self,
                       population: Type[BasePopulation],
                       num_individ: int,
                       num_generations: int,
                       gens: tuple,
                       input_population: List[list] = None,
                       children_percent: float = 0.95,
                       early_stop: int = 10) -> None:
        """
        Method for definition population.
        :param population: subclass of BasePopulation;
        :param num_individ: int, number of individuals in generation (size of population);
        :param num_generations: int, number of generations;
        :param gens: tuple or list, depends on population type;
        :param input_population: list[list], default: None. First generation from user;
        :param children_percent: float, default: 0.95. Percent of children who will be in new generation;
        :param early_stop: int, default: 10. Early stopping criteria, number of generation without improve;
        :return: None.
        """
        self.ga_data = self.storage(num_generations=num_generations, children_percent=children_percent,
                                    early_stop=early_stop)
        ppl = population()
        ppl.set_params(num_individ=num_individ, gens=gens, input_population=input_population)
        ppl.fill()
        self.ga_data.population = ppl

    def optimize(self) -> None:
        """
        Main method of CollectorGA().
        :return: None.
        """
        self.fitness.execute(self.ga_data)
        self.ga_data.update()

        for i in range(1, self.ga_data.num_generations):

            self.selection.execute(self.ga_data)
            self.crossover.execute(self.ga_data)
            self.mutation.execute(self.ga_data)
            self.new_generation.execute(self.ga_data)
            self.fitness.execute(self.ga_data)
            self.ga_data.update()

            if self.ga_data.num_generation_no_improve > self.ga_data.early_stop:
                break
        self.ga_data.print_best_solution()
