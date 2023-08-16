from random import sample
from .base_combinatory_mutation import BaseCombinatoryMutation


class SwapMutation(BaseCombinatoryMutation):

    def get_mutation(self, child: dict) -> dict:
        idx_swap = sample(range(0, len(child['genotype'])), 2)
        child['genotype'][idx_swap[0]], child['genotype'][idx_swap[1]] =\
            child['genotype'][idx_swap[1]], child['genotype'][idx_swap[0]]

        return child
