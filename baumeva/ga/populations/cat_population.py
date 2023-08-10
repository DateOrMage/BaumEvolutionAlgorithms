from typing import List
from random import randrange
from .base_population import BasePopulation


class CatPopulation(BasePopulation):
    """
    A class for representing a categorical population in a genetic algorithm.
    Inherits from BasePopulation.
    """
    num_individ: int = None
    gens: tuple = None
    input_population: List[list] = None

    def set_params(self, num_individ: int, gens: tuple, input_population: List[list] = None) -> None:
        """
         Initialization of categorical population.

         :param num_individ: the number of individuals in the population.
         :param gens: tuple specifying the range of categorical values for each gene.
                      Each element in the tuple should be a tuple with (start, end, step) values.
         :param input_population: optional input population to be used for initialization.
         """
        if input_population:
            if len(input_population) > num_individ:
                raise Exception(f'Size of input population: {len(input_population)} more then number of individuals:'
                                f' {num_individ}')
        self.num_individ = num_individ
        self.gens = gens
        self.input_population = input_population

    def get_generated_individ(self):
        genotype = []
        for gen in self.gens:
            genotype.append(randrange(gen[0], gen[1]+1, gen[2]))
        return genotype

    def fill(self) -> None:
        if self.input_population:
            for individ in self.input_population:
                self.add_dict(genotype=list(individ), score=None, obj_score=None)
            num_empty_individ = self.num_individ - len(self.input_population)
        else:
            num_empty_individ = self.num_individ

        for i in range(num_empty_individ):
            self.add_dict(genotype=self.get_generated_individ(), score=None, obj_score=None)


if __name__ == '__main__':
    population = CatPopulation()
    population.set_params(num_individ=10, gens=((0, 10, 1), (-10, 0, 1)), input_population=[[2, 0], [3, -1]])
    population.fill()
    for individual in population:
        print(individual)
