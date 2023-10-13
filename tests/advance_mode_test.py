from random import shuffle
from baumeva.ga import GaData, OrderCatPopulation, HyperbolaFitness, TournamentSelection, OrderCrossover, SwapMutation, \
    NewGeneration


def func_word(word: list) -> float:
    obj_word = 'ALGORITHM'
    res = 0
    for idx, litter in enumerate(word):
        if litter != obj_word[idx]:
            res += 1
    return res


input_population_size = 100
input_word = list("ALGORITHM")
in_pop = []
for i in range(input_population_size):
    shuffle(input_word)
    in_pop.append(input_word.copy())


def print_result(data: dict) -> None:
    print("Best result: ")
    for key in data.keys():
        print(f"{key}: {data[key]}")


ga_data = GaData(num_generations=100, early_stop=60)
ocp = OrderCatPopulation()
ocp.set_params(num_individ=input_population_size, gens=(0, 8, 9), input_population=in_pop)
ocp.fill()
ga_data.population = ocp
fitness_func = HyperbolaFitness(obj_function=func_word, obj_value=0)
fitness_func.execute(ga_data)
ga_data.update()

selection = TournamentSelection(tournament_size=6)
crossover = OrderCrossover()
mutation = SwapMutation(0.35)
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
