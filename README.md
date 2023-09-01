# BaumEvA - Bauman Evolution Algorithm

BaumEvA is an advanced genetic algorithm crafted in Python. It's designed to work with both binary and combinatorial data types, providing a comprehensive suite of tools for optimization and search tasks. Baumeva offers a variety of selection, crossover, mutation, and parent selection mechanisms.

## Installation

To install the BaumEvA, run the following command:

```bash
pip install baumeva
```

## Usage

### Basic Usage

BaumEvA is designed for straightforward integration and usage. The library features two classes: `BinaryGA` and `CombinatoryGA`. These classes come equipped with predefined methods, allowing users to effortlessly engage with both binary and combinatorial genetic algorithms.

```python
from baumeva import BinaryGA

# function to be optimized
def func_grivanka(value_list):
    res_sum = 0
    res_mpl = 1
    for i, value in enumerate(value_list):
        res_sum += (value*value) / 4000
        res_mpl *= math.cos(value/math.sqrt(i+1))
    return res_sum - res_mpl + 1

# simple method for use GA
binary_ga = BinaryGA(num_generations=100,
                     num_individ=100,
                     gens=((-16, 16, 0.01), (-16, 16, 0.01)),
                     obj_function=func_grivanka,
                     obj_value=0)
data = binary_ga.optimize()
```

The `num_generations` specifies the total number of generations the genetic algorithm should run for. In the example given `num_generations=100` means the algorithm will iterate through 100 generations.

The `num_individ` dictates the total number of individuals in a population. In the example given num_individ=100 implies there are 100 individuals in a single generation.

The `gens` defines the range and precision for each gene in the binary representation. Each inner tuple comprises: minimum value for the gene, maximum value for the gene, precision for the gene's value (the step). In the example given gens=((-16, 16, 0.01), (-16, 16, 0.01)) signifies two genes, both ranging from -16 to 16 with a precision of 0.01.

The `obj_function` describes the objective function that evaluates the object score of each individual. In the example given `obj_function=func_grivanka` indicates the func_grivanka function will be used to determine the object score and subsequently fitness score of the individuals.

The `obj_value` defines the target or optimal value the algorithm aims to achieve or get as close as possible to, using the obj_function. In the example given `obj_value=0` means the genetic algorithm will aim to find an individual whose object function value is as close to 0 as possible.

### Advanced Usage

Additionally, Baumeva offers a modular approach for those who desire more granularity. Beyond the convenience of the `BinaryGA` and `CombinatoryGA` classes, users have the flexibility to assemble a genetic algorithm tailored to their needs. By directly declaring specific classes, you can handpick from a diverse range of mutation, selection and crossover methods, crafting a customized genetic algorithm.

```python
import random
from baumeva import GaData
from baumeva.ga.populations import OrderCatPopulation
from baumeva.ga.fitness import HyperbolaFitness
from baumeva.ga.selections import TournamentSelection
from baumeva.ga.crossovers import OrderCrossover
from baumeva.ga.mutations import InversionMutation
from baumeva import NewGeneration

def word_distance(word):
    return sum(c1 != c2 for c1, c2 in zip('algorithm', word))

def string_generator():
    chars = list('algorithm')
    while True:
        random.shuffle(chars)
        yield ''.join(chars)

generated_population = [next(string_generator()) for _ in range(50)]

ga_data = GaData(num_generations=100, early_stop=15)
ocp = OrderCatPopulation()
ocp.set_params(num_individ=50, gens=(0, 8, 9), input_population=generated_population)
ocp.fill()
ga_data.population = ocp
fitness_func = HyperbolaFitness(obj_function=word_distance, obj_value=0)
fitness_func.execute(ga_data=ga_data)
ga_data.update()

for i in range(ga_data.num_generations):
    selection = TournamentSelection(tournament_size=5)
    selection.execute(ga_data)

    order_cross = OrderCrossover()
    order_cross.execute(ga_data)

    bcm = InversionMutation(0.15)
    bcm.execute(ga_data)

    NewGeneration('best').execute(ga_data)

    fitness_func.execute(ga_data=ga_data)
    ga_data.update()

    if ga_data.num_generation_no_improve >= ga_data.early_stop:
        print(f'Early stopping: {i}')
        break

print(f"Result: {ga_data.best_solution} ")
```

This example demonstrates the use of the BaumEvA library to search for the word "algorithm" using a categorical genetic algorithm.

### Components Used:

1. **GaData**: Configures the genetic algorithm's data parameters like the number of generations and an early stopping criterion.
2. **OrderCatPopulation**: Represents the population structure for this task. In this case we set the first population manually using `generated_population` - a list consisting of words anagrams to 'algorithm'.
3. **HyperbolaFitness**: Fitness function, where the objective is the word distance between the evolved string and the target string 'algorithm'.
4. **TournamentSelection**: Selection method used, which operates on tournament-based selection logic.
5. **OrderCrossover**: The crossover mechanism used in the genetic algorithm.
6. **InversionMutation**: Mutation method, introducing randomness in the population.
7. **NewGeneration**: Utility for generating new population members based on chosen criteria.

### How it works:

1. The genetic algorithm data parameters are initialized, and the initial population is set and filled.
2. The fitness of each individual in the population is calculated based on its distance from the target word 'algorithm'.
3. In each generation:
   - The tournament-based selection method is applied.
   - Pairs of individuals undergo crossover using the order-based crossover mechanism.
   - Mutation is applied with a probability to introduce variability.
   - A new generation is created based on the best individuals.
   - Fitness is recalculated for the new generation.
4. The genetic algorithm either runs for a predefined number of generations or stops early if there hasn't been an improvement in the population fitness for a specified number of generations.
5. The result is the closest approximation found to the word 'algorithm'.

## License

The BaumEvA library is distributed under the MIT License. See the [LICENSE](https://github.com/DateOrMage/BaumEvolutionAlgorithms/blob/master/LICENSE.txt) file for more information.

## Contribution

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/DateOrMage/BaumEvolutionAlgorithms).

## Contact

For any inquiries or questions, you can reach out to the author via email at [vatutu@gmail.com](mailto:vatutu@gmail.com).
