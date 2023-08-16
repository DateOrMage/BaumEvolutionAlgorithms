from random import sample
from .base_combinatory_mutation import BaseCombinatoryMutation


class InversionMutation(BaseCombinatoryMutation):

    def get_mutation(self, child: dict) -> dict:

        idx_segment = sample(range(0, len(child['genotype'])), 2)
        idx_segment.sort()

        segment = child['genotype'][idx_segment[0]:idx_segment[1]+1]
        segment.reverse()
        left_side = child['genotype'][:idx_segment[0]]
        right_side = child['genotype'][idx_segment[1]+1:]

        child['genotype'] = left_side + segment + right_side
        return child



