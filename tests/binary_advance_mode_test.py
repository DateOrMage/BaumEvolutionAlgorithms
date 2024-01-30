import math
from random import seed
import baumeva
from baumeva.ga import GaData, BinaryPopulation, HyperbolaFitness, TournamentSelection, OnePointCrossover,\
    BinStringMutation, NewGeneration, BinaryGrayPopulation, CatPopulation, OrderCatPopulation, BalancedSelection,\
    RankedSelection, TwoPointCrossover, UniformCrossover


def func_grivanka(value_list):
    res_sum = 0
    res_mpl = 1
    for i, value in enumerate(value_list):
        res_sum += (value*value) / 4000
        res_mpl *= math.cos(value/math.sqrt(i+1))
    return res_sum - res_mpl + 1


def print_result(data: dict) -> None:
    print("Best result: ")
    for key in data.keys():
        print(f"{key}: {data[key]}")


baumeva.generator.rnd_seed = 11
ga_data = GaData(num_generations=100, early_stop=60)
bp = BinaryGrayPopulation()
bp.set_params(num_individ=100, gens=((-16, 16, 0.01), (-16, 16, 0.01)), input_population=None)
bp.fill()
ga_data.population = bp
for d in ga_data.population:
    print('-'*35)
    for k in d.keys():
        print(f"{k}: {d[k]}")
fitness_func = HyperbolaFitness(obj_function=func_grivanka, obj_value=0)
fitness_func.execute(ga_data)
ga_data.update()

selection = TournamentSelection(tournament_size=3)
crossover = OnePointCrossover()
mutation = BinStringMutation(0.35)
new_generation = NewGeneration('best')

for i in range(1, ga_data.num_generations):

    selection.execute(ga_data)
    crossover.execute(ga_data)
    mutation.execute(ga_data)
    new_generation.execute(ga_data)
    fitness_func.execute(ga_data)
    ga_data.update()

    if ga_data.num_generation_no_improve >= ga_data.early_stop:
        print(f'Early stopping: {i} generation')
        break
    if ga_data.best_solution['obj_score'] == 0:
        print(f'Goal achieved: {i} generation')
        break

ga_data.print_best_solution()
