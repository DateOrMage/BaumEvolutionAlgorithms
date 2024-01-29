from typing import List, Tuple
from random import randint, seed
from .base_population import BasePopulation


class BinaryPopulation(BasePopulation):
    """
    Class for representing a binary population in a genetic algorithm.
    Inherits from BasePopulation.
    """
    num_bits: List[int] = []
    real_num_points: List[int] = []
    real_step: List[float] = []
    idx_bits: List[int] = [0]

    def set_params(self, num_individ: int, gens: tuple, input_population: List[list] = None) -> None:
        """
        Initialization of binary population.

        :param num_individ: the number of individuals in the population.
        :param gens: tuple specifying the range of int|float values for each gene.
                     Each element in the tuple should be a tuple with (start, end, step) values.
        :param input_population: optional input population to be used for initialization.
        :return: None
        """
        if input_population:
            if len(input_population) > num_individ:
                raise Exception(f'Size of input population: {len(input_population)} more then number of individuals:'
                                f' {num_individ}')
        self.num_individ = num_individ
        self.gens = gens
        self.input_population = input_population
        self.is_phenotype = True

    @staticmethod
    def get_real_number_of_points(num_points: int) -> Tuple[int, int]:
        """
        Function for search n: 2**n - 1 >= num_points, where n is number of bits.
        Returns n and real_num_points = 2**n - 1.
        """
        n = 0
        while (2 ** n - 1) < num_points:
            n += 1

        return n, 2 ** n - 1

    def get_gens_params(self) -> None:
        """
        Method for getting binary parameters of gens
        :return: None
        """
        for gen in self.gens:
            gen_range = abs(gen[1] - gen[0])
            num_points = int(gen_range / gen[2])
            num_bits, real_num_points = self.get_real_number_of_points(num_points)
            self.real_step.append(gen_range / (2 ** num_bits - 1))
            self.num_bits.append(num_bits)
            self.real_num_points.append(real_num_points)
            self.idx_bits.append(self.idx_bits[-1] + num_bits)

    @staticmethod
    def index_to_binary(value: int, num_bits: int) -> str:
        """
        Function for coding integer value to binary with definition number of bits.
        Return binary string.
        """
        bin_string = bin(value)[2:]
        if len(bin_string) > num_bits:
            raise Exception(f'Cannot convert {value} to binary string with current number of bits: {num_bits}')
        elif len(bin_string) < num_bits:
            bin_string = '0' * (num_bits - len(bin_string)) + bin_string
        return bin_string

    def get_generated_individ(self) -> list:
        """
        Method for generation genotype of individ.
        :return: list of '0' and '1'.
        """
        genotype = ''
        if self.rnd_seed is not None:
            seed(self.rnd_seed)
            self.rnd_seed += 1
        for i in range(len(self.gens)):
            genotype += self.index_to_binary(value=randint(0, self.real_num_points[i]), num_bits=self.num_bits[i])

        return list(genotype)

    def float_individ_to_binary(self, float_gens: list) -> list:
        """
        Method for coding input individ to binary
        :param float_gens: input genotype;
        :return: list of '0' and '1'
        """
        if len(float_gens) != len(self.gens):
            raise Exception(f'Incorrect len of input individ: {float_gens}')
        genotype = ''
        for gen_idx, gen_value in enumerate(float_gens):
            if gen_value < self.gens[gen_idx][0] or gen_value > self.gens[gen_idx][1]:
                raise Exception(f'Gen: {gen_value} is out of range:'
                                f' ({self.gens[gen_idx][0]}, {self.gens[gen_idx][1]})')
            step_idx = round((gen_value - self.gens[gen_idx][0]) / self.real_step[gen_idx])
            genotype += self.index_to_binary(value=step_idx, num_bits=self.num_bits[gen_idx])

        return list(genotype)

    def binary_individ_to_float(self, genotype: list) -> list:
        """
        Method for decoding binary individ to float
        :param genotype: binary genotype;
        :return: list of real gens.
        """
        phenotype = []
        genotype_str = ''.join(genotype)
        for gen_idx, gen_item in enumerate(self.gens):
            index_point = int(genotype_str[self.idx_bits[gen_idx]:self.idx_bits[gen_idx + 1]], 2)
            point = self.gens[gen_idx][0] + index_point * self.real_step[gen_idx]
            phenotype.append(point)
        return phenotype

    def get_phenotype(self):
        """
        Method for adding phenotype to individ.
        :return: None.
        """
        for individ in self:
            if individ['phenotype'] is None:
                individ['phenotype'] = self.binary_individ_to_float(individ['genotype'])

    def fill(self) -> None:
        """
        Fill the binary population with individuals according to the specified parameters.

        :return: None
        """
        self.get_gens_params()

        if self.input_population:
            for individ in self.input_population:
                self.add_dict(genotype=self.float_individ_to_binary(individ), phenotype=None, score=None,
                              obj_score=None)
            num_empty_individ = self.num_individ - len(self.input_population)
        else:
            num_empty_individ = self.num_individ

        for i in range(num_empty_individ):
            self.add_dict(genotype=self.get_generated_individ(), phenotype=None, score=None, obj_score=None)

        self.get_phenotype()
        self.reset_idx_individ()

    def swap(self) -> None:
        """
        Method for swap genotype and phenotype.
        :return: None.
        """
        for individ in self:
            individ['genotype'], individ['phenotype'] = individ['phenotype'], individ['genotype']

    @staticmethod
    def get_empty_copy():
        """
        Get an empty instance of BinaryPopulation.

        :return: An empty instance of BinaryPopulation.
        """
        return BinaryPopulation()
