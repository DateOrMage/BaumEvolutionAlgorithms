from typing import List
from random import randrange
from .base_population import BasePopulation


class CatPopulation(BasePopulation):
    """
    Class for representing a categorical population in a genetic algorithm.
    Inherits from BasePopulation.
    """

    def set_params(self, num_individ: int, gens: tuple, input_population: List[list] = None) -> None:
        """
         Initialization of categorical population.

         :param num_individ: the number of individuals in the population.
         :param gens: tuple specifying the range of categorical values for each gene.
                      Each element in the tuple should be a tuple with (start, end, step) values.
         :param input_population: optional input population to be used for initialization.
         :return: None
         """
        if input_population:
            if len(input_population) > num_individ:
                raise Exception(f'Size of input population: {len(input_population)} more then number of individuals:'
                                f' {num_individ}')
        self.num_individ = num_individ
        self.gens = gens
        self.input_population = input_population

    def get_generated_individ(self):
        """
        Generate a random individual based on the defined gene ranges.

        :return: list representing the genotype of the generated individual.
        """
        genotype = []
        for gen in self.gens:
            genotype.append(randrange(gen[0], gen[1]+1, gen[2]))
        return genotype

    def fill(self) -> None:
        """
        Fill the categorical population with individuals according to the specified parameters.

        :return: None
        """
        if self.input_population:
            for individ in self.input_population:
                self.add_dict(genotype=list(individ), score=None, obj_score=None)
            num_empty_individ = self.num_individ - len(self.input_population)
        else:
            num_empty_individ = self.num_individ

        for i in range(num_empty_individ):
            self.add_dict(genotype=self.get_generated_individ(), score=None, obj_score=None)

        self.reset_idx_individ()

    @staticmethod
    def get_empty_copy():
        """
        Get an empty instance of CatPopulation.

        :return: An empty instance of CatPopulation.
        """
        return CatPopulation()
