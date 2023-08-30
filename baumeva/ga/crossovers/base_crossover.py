from random import randint
from abc import ABC, abstractmethod
from baumeva.ga import GaData


class BaseCrossover(ABC):
    """
    Abstract class for implementing crossover operations in a genetic algorithm.
    """
    def __init__(self) -> None:
        """
        Initialize the BaseCrossover instance.
        :return: None
        """
        self.num_offsprings: int = 1

    @abstractmethod
    def crossover(self, parent_1: list, parent_2: list, child_1: dict, child_2: dict) -> tuple:
        """
        Perform crossover of parent_1 and parent_2.
        :param parent_1: genotype of first parent
        :param parent_2: genotype of second parent
        :param child_1: first offspring
        :param child_2: second offspring
        :return: child_1 and child_2
        """
        pass

    def get_children(self, parent_1: list, parent_2: list, ga_data: GaData) -> tuple:
        """
        Generate offspring using crossover.

        :param parent_1: list containing genotypes of parent individuals.
        :param parent_2: list containing genotypes of parent individuals.
        :param ga_data: GaData instance containing population and related data.
        :return: A tuple containing generated offspring individuals.
        """

        child_1 = ga_data.population.get_empty_individ()
        child_2 = ga_data.population.get_empty_individ()

        child_1, child_2 = self.crossover(parent_1, parent_2, child_1, child_2)

        if self.num_offsprings == 1:
            coin = randint(1, 2)
            if coin == 1:
                return (child_1, )
            else:
                return (child_2, )
        else:
            return child_1, child_2

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the crossover operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        ga_data.children = ga_data.population.get_empty_copy()
        for i in range(0, int(len(ga_data.parents)), 2):
            parent_1 = ga_data.parents[i]['genotype']
            parent_2 = ga_data.parents[i+1]['genotype']
            pair_children = self.get_children(parent_1, parent_2, ga_data=ga_data)
            for child in pair_children:
                ga_data.children.append(child)
