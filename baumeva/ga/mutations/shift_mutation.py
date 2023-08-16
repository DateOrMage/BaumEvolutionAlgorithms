from random import sample
from .base_combinatory_mutation import BaseCombinatoryMutation


class ShiftMutation(BaseCombinatoryMutation):

    def get_mutation(self, child: dict) -> dict:
        # fill realization
        return child
