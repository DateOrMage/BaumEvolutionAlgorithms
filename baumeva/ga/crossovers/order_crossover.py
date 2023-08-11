from .base_crossover import BaseCrossover
from baumeva.ga import GaData


class OrderCrossover(BaseCrossover):
    def get_children(self, *parents_data: dict, ga_data: GaData):
        # get empty dict of individ
        # fill two child
        # return 1 or 2 child
        pass

    def execute(self, ga_data: GaData) -> None:
        super().execute(ga_data)
        for i in range(int(len(ga_data.parents)/2)):
            first_p = ga_data.parents[i]
            second_p = ga_data.parents[-i-1]

