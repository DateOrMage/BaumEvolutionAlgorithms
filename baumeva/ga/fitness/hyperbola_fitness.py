from typing import List, Union
from .base_fitness import BaseFitness


class HyperbolaFitness(BaseFitness):

    def get_scores(self, genotype: List[Union[int, float]], idx_generation:  int) -> tuple:

        if self.input_data:
            obj_score = self.obj_function(self.input_data, genotype)
        else:
            obj_score = self.obj_function(genotype)

        if self.obj_value is not None:
            score = 1.0 / (1 + abs(self.obj_value - (obj_score + self.get_penalty_value(genotype, idx_generation))))
        else:
            score = -(obj_score + self.get_penalty_value(genotype, idx_generation))

        return obj_score, score
