from random import sample, randint
from .base_crossover import BaseCrossover
from baumeva.ga import GaData


class OrderCrossover(BaseCrossover):
    """
    A class for implementing order crossover in a genetic algorithm.
    Inherits from BaseCrossover.
    """
    def __init__(self) -> None:
        """
        Initialize the OrderCrossover instance.

        :return: None
        """
        super().__init__()
        self.len_individ = None

    def get_idx_segment(self) -> list:
        """
        Get the indices for the crossover segment to change.

        :return: A list containing the indices of the crossover segment.
        """
        idx_segment = sample(range(1, self.len_individ), 2)
        idx_segment.sort()
        return idx_segment

    def get_children(self, *parents_data: tuple, ga_data: GaData) -> tuple:
        """
        Generate offspring using order crossover.

        :param parents_data: tuple containing genotypes of parent individuals.
        :param ga_data: GaData instance containing population and related data.
        :return: A tuple containing generated offspring individuals.
        """

        child_1 = ga_data.population.get_empty_individ()
        child_2 = ga_data.population.get_empty_individ()

        idx_segment = self.get_idx_segment()
        right_side = self.len_individ - idx_segment[1]
        left_side = idx_segment[0]

        segment = parents_data[0][idx_segment[0]:idx_segment[1]]
        new_gens = [x for x in parents_data[1] if x not in segment]
        child_1['genotype'] = new_gens[right_side:right_side+left_side] + segment + new_gens[:right_side]

        segment = parents_data[1][idx_segment[0]:idx_segment[1]]
        new_gens = [x for x in parents_data[0] if x not in segment]
        child_2['genotype'] = new_gens[right_side:right_side + left_side] + segment + new_gens[:right_side]

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
        Execute the order crossover operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        super().execute(ga_data)
        self.len_individ = len(ga_data.population[0]['genotype'])
        for i in range(0, int(len(ga_data.parents)), 2):
            parent_1 = ga_data.parents[i]['genotype']
            parent_2 = ga_data.parents[i+1]['genotype']
            pair_children = self.get_children(parent_1, parent_2, ga_data=ga_data)
            for child in pair_children:
                ga_data.children.append(child)
