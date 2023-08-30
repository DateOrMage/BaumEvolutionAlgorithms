# from .gen_alg import GA
from .ga_data import GaData
from .new_generation import NewGeneration
from .penalties.penalty_methods import PenaltyFunction, Dynamic
from .populations import BasePopulation, CatPopulation, OrderCatPopulation, BinaryPopulation, BinaryGrayPopulation
from .fitness import BaseFitness, HyperbolaFitness
from .selections import BaseSelection, TournamentSelection, BalancedSelection, RankedSelection
from .crossovers import BaseCrossover, OrderCrossover, OnePointCrossover, TwoPointCrossover, UniformCrossover
from .mutations import BaseMutation, BaseCombinatoryMutation, InversionMutation, SwapMutation, MovementMutation,\
                       ShiftMutation, BinStringMutation
