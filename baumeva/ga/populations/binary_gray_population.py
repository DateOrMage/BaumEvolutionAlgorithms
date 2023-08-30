from .binary_population import BinaryPopulation


class BinaryGrayPopulation(BinaryPopulation):
    @staticmethod
    def get_gray_value(value: int) -> int:
        """
        Function for coding integer value into graycode
        :param value: input integer value
        :return: graycode in integer type
        """
        return value ^ (value >> 1)

    @staticmethod
    def get_index_from_gray(gray_value: int) -> int:
        """
        Get index of point from gray value.
        :param gray_value: integer
        :return: index of point
        """
        real_value = 0
        while gray_value > 0:
            real_value = real_value ^ gray_value
            gray_value = gray_value >> 1
        return real_value

    def index_to_binary(self, value: int, num_bits: int) -> str:
        """
        Function for coding integer value to binary with definition number of bits.
        Return binary string.
        """
        value = self.get_gray_value(value)

        return super().index_to_binary(value=value, num_bits=num_bits)

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
            index_point = self.get_index_from_gray(index_point)
            point = self.gens[gen_idx][0] + index_point * self.real_step[gen_idx]
            phenotype.append(point)
        return phenotype

    @staticmethod
    def get_empty_copy():
        """
        Get an empty instance of BinaryGrayPopulation.

        :return: An empty instance of BinaryGrayPopulation.
        """
        return BinaryGrayPopulation()
