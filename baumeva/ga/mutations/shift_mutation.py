from random import randint, choice
from .base_combinatory_mutation import BaseCombinatoryMutation


class ShiftMutation(BaseCombinatoryMutation):

    def get_mutation(self, child: dict) -> dict:
        chain_length = randint(1, len(child['genotype']) - 2)
        s_idx = randint(0, len(child['genotype']) - chain_length)
        e_idx = s_idx + chain_length

        chain = child['genotype'][s_idx:e_idx]
        del child['genotype'][s_idx:e_idx]

        i_idx = choice([idx for idx in range(len(child['genotype']) + 1) if idx != s_idx])
        child['genotype'][i_idx:i_idx] = chain

        return child
