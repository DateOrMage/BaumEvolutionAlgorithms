from baumeva import CollectorGA
from baumeva.ga import BinaryPopulation, HyperbolaFitness, TournamentSelection, OnePointCrossover,\
    BinStringMutation, NewGeneration


def generate_gens_params(one_gen: list, num_gens: int) -> list:
    gens_params = []
    for _ in range(num_gens):
        gens_params.append(one_gen)
    return gens_params


def one_max(gens: list) -> float:
    return sum(gens) / len(gens)


my_ga = CollectorGA(fitness=HyperbolaFitness(obj_function=one_max, obj_value=1),
                    selection=TournamentSelection(5),
                    crossover=OnePointCrossover(),
                    mutation=BinStringMutation(0.15),
                    new_generation=NewGeneration('best'))

my_ga.set_population(population=BinaryPopulation,
                     num_individ=100,
                     num_generations=100,
                     gens=generate_gens_params([0, 1, 1], 30),
                     early_stop=35)

my_ga.optimize()
