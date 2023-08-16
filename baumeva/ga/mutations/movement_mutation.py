from random import sample
from .base_combinatory_mutation import BaseCombinatoryMutation


class MovementMutation(BaseCombinatoryMutation):

    def get_mutation(self, child: dict) -> dict:
        idx_move = sample(range(0, len(child['genotype'])), 2)
        z = child['genotype'].pop(idx_move[0])
        child['genotype'].insert(idx_move[1], z)
        return child
