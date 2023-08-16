from random import sample
from .base_combinatory_mutation import BaseCombinatoryMutation


class MovementMutation(BaseCombinatoryMutation):
    """
    A class for implementing movement mutation in a genetic algorithm.
    Inherits from BaseCombinatoryMutation.
    """

    def get_mutation(self, child: dict) -> dict:
        """
        Perform movement mutation on a child individual.

        :param child: A dictionary representing the child individual.
        :return: The mutated child individual.
        """
        idx_move = sample(range(0, len(child['genotype'])), 2)
        z = child['genotype'].pop(idx_move[0])
        child['genotype'].insert(idx_move[1], z)
        return child
