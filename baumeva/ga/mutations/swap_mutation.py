from random import sample
from .base_combinatory_mutation import BaseCombinatoryMutation


class SwapMutation(BaseCombinatoryMutation):
    """
    A class for implementing swap mutation in a genetic algorithm.
    Inherits from BaseCombinatoryMutation.
    """

    def get_mutation(self, child: dict) -> dict:
        """
        Perform swap mutation on a child individual.

        :param child: A dictionary representing the child individual.
        :return: The mutated child individual.
        """

        idx_swap = sample(range(0, len(child['genotype'])), 2)
        child['genotype'][idx_swap[0]], child['genotype'][idx_swap[1]] =\
            child['genotype'][idx_swap[1]], child['genotype'][idx_swap[0]]

        return child
