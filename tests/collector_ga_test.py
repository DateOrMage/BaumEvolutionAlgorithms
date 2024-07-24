from baumeva import CollectorGA
from baumeva.ga import (GaData, MultiGaData, BinaryPopulation, HyperbolaFitness, FFGAFitness, VEGAHyperbolaFitness,
                        TournamentSelection, VEGATournamentSelection, VEGABalancedSelection, OnePointCrossover,
                        BinStringMutation, DynamicPenalty, NewGeneration)


def generate_gens_params(one_gen: list, num_gens: int) -> list:
    gens_params = []
    for _ in range(num_gens):
        gens_params.append(one_gen)
    return gens_params


def one_max(gens: list) -> float:
    return sum(gens) / len(gens)


# my_ga = CollectorGA(fitness=HyperbolaFitness(obj_function=one_max, obj_value=1),
#                     selection=TournamentSelection(5),
#                     crossover=OnePointCrossover(),
#                     mutation=BinStringMutation(0.15),
#                     new_generation=NewGeneration('best'))
#
# my_ga.set_population(population=BinaryPopulation,
#                      num_individ=100,
#                      num_generations=100,
#                      gens=generate_gens_params([0, 1, 1], 30),
#                      early_stop=35)
#
# my_ga.optimize()

# ---------------------------------- multi-objective optimization ----------------------------------------------------


def zdt1(x: list) -> tuple:
    """
    conditions=['optimize']*2
    gens=((0, 1, 0.01),)*30
    """
    f1 = x[0]
    g = 1 + 9 / (len(x) - 1) * sum(x[1:])
    h = 1 - (f1/g) ** 0.5
    f2 = g * h

    return f1, f2


def multilinear_conditions(x: list) -> tuple:
    """
    conditions=['optimize']*9 + ['<=']*5
    gens=((0, 100, 0.01), (0, 100, 0.01))
    """
    return -4*x[0]-2*x[1], -2*x[0]-4*x[1], -3*x[0]-9*x[1], -8*x[0]-2*x[1], -4*x[0]+x[1], -3*x[0]+2*x[1], 2*x[0] - 4*x[1], \
        3*x[0] - x[1], 4*x[0] + 3*x[1], 2*x[0]+3*x[1], -x[0]+3*x[1], 2*x[0]-x[1], -x[0], -x[1]


moga = CollectorGA(fitness=VEGAHyperbolaFitness(obj_function=multilinear_conditions, obj_value=[0,]*9,
                                                conditions=['optimize']*9 + ['<=']*5, penalty=DynamicPenalty()),
                   selection=VEGABalancedSelection(9),
                   crossover=OnePointCrossover(),
                   mutation=BinStringMutation(0.05),
                   new_generation=NewGeneration('best'),
                   storage=MultiGaData)

moga.set_population(population=BinaryPopulation,
                    num_individ=100,
                    num_generations=1000,
                    gens=((0, 100, 0.01), (0, 100, 0.01)))

moga.optimize()
