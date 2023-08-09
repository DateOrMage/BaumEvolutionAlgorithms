from .populations import BasePopulation


class GaData:
    idx_generation: int = 0
    population: BasePopulation = None
    children: BasePopulation = None

