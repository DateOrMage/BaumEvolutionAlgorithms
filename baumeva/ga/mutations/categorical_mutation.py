from typing import Union
from random import randint, choice, randrange
from .base_mutation import BaseMutation
from baumeva.ga import GaData

class CategoricalMutation(BaseMutation):

    def __init__(self, mutation_lvl: Union[str, float] = 'normal') -> None:
        """
        Initialize the CategoricalMutation instance.

        :param mutation_lvl: Mutation level, can be string ('weak', 'normal', 'strong') or a float from 0 to 1.
        :return: None
        """
        super().__init__(mutation_lvl=mutation_lvl)
        self.check_mutation()

    def check_mutation(self) -> None:
        """
        Check the validity of the mutation level parameter.

        :return: None
        """
        if type(self.mutation_lvl) is str:
            if self.mutation_lvl in self.mutation_map.keys():
                self.mutation_lvl = self.mutation_map[self.mutation_lvl]
            else:
                raise Exception(f'{self.mutation_lvl} is not expected, please use one of this:'
                                f' ("normal", "weak", "strong") or float value from 0 to 1')
        elif type(self.mutation_lvl) is float:
            if self.mutation_lvl < 0 or self.mutation_lvl > 1:
                raise Exception(f'{self.mutation_lvl} is not expected, please use one of this:'
                                f' ("normal", "weak", "strong") or float value from 0 to 1')
        else:
            raise Exception(f'{self.mutation_lvl} is not expected, please use one of this:'
                            f' ("normal", "weak", "strong") or float value from 0 to 1')

    # {0.3, 1, 3} might not be the optimal set coefficients for categorical mutation
    def update_mutation_lvl(self, len_bin_str: int) -> None:
        """
        Method for mapping string value mutation to float.
        :param len_bin_str: length of binary string;
        :return: None.
        """
        if type(self.mutation_lvl) is str:
            if self.mutation_lvl == 'weak':
                self.mutation_lvl = 0.3 / len_bin_str
            elif self.mutation_lvl == 'normal':
                self.mutation_lvl = 1 / len_bin_str
            else:
                self.mutation_lvl = 3 / len_bin_str

    def determines_mutation(self) -> bool:
        """
        Determine if mutation should be performed.

        :return: True if mutation should be performed, False otherwise.
        """
        if randint(0, self.rnd_samples - 1) <= self.mutation_lvl * self.rnd_samples:
            return True
        else:
            return False

    def get_mutation(self, child: dict, gen_pool: tuple) -> None:
        """
        Perform categorical mutation on a child individual.

        :param child: A dictionary representing the child individual.
        :param gen_pool: A tuple, gens attribute from population class
        :return: None.
        """
        for i_gen, gen in enumerate(child['genotype']):
            is_mutation = self.determines_mutation()
            if is_mutation:
                if isinstance(gen_pool[i_gen], list):
                    if len(gen_pool[i_gen]) > 1:
                        child['genotype'][i_gen] = choice([x for x in gen_pool[i_gen] if x != child['genotype'][i_gen]])
                    else:
                        continue
                else:
                    if len(range(gen_pool[i_gen][0], gen_pool[i_gen][1]+1, gen_pool[i_gen][2])) > 1:
                        child['genotype'][i_gen] = \
                            choice([x for x in range(gen_pool[i_gen][0], gen_pool[i_gen][1]+1, gen_pool[i_gen][2]) if x != child['genotype'][i_gen]])
                    else:
                        continue

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the mutation operation.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        for child in ga_data.children:
            self.get_mutation(child, ga_data.population.gens)