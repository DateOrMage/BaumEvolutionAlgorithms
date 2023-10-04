from random import sample
from .ga_data import GaData


class NewGeneration:
    """
    Class for creating a new generation of individuals in a genetic algorithm.
    """

    def __init__(self, transfer_parents: str = 'best') -> None:
        """
        Initialize the NewGeneration instance.

        :param transfer_parents: strategy for transferring parents to the next generation.
        :return: None
        """
        self.transfer_parents = transfer_parents
        self.check_transfer_parent()

    def check_transfer_parent(self) -> None:
        """
        Check if the selected strategy for transferring parents is valid.


        :return: None
        """
        if self.transfer_parents not in ['best', 'random']:
            raise Exception(f'transfer_parents must be equal "best" or "random", not {self.transfer_parents}')

    def add_parents(self, ga_data: GaData, num_elites: int) -> None:
        """
        Add parent individuals to the offspring based on the selected strategy.

        :param ga_data: GaData instance containing population and related data.
        :param num_elites: number of parent individuals to add.
        :return: None
        """
        if self.transfer_parents == 'best':
            elites = ga_data.population[-num_elites - 1:]
            if ga_data.population.is_duplicate(elites):
                loop_counter = 0
                z_counter = 0
                while ga_data.population.is_duplicate(elites):
                    break_out_loop = False
                    for i in range(1, len(elites)):
                        for j in range(1, len(elites) - (i-1)):
                            if elites[-i]['genotype'] == elites[-i-j]['genotype']:
                                del elites[-i-j]
                                break_out_loop = True
                                break
                        if break_out_loop:
                            break

                    z_counter += 1
                    if -num_elites-1-z_counter < 0:
                        elites[0:0] = sample(ga_data.population, num_elites + 1 - len(elites))
                        break
                    elites.insert(0, ga_data.population[-num_elites-1-z_counter])
                    loop_counter += 1
                    if loop_counter >= len(ga_data.children):
                        break
        else:
            elites = sample(ga_data.population[:-1], num_elites)
            loop_counter = 0
            while ga_data.population.is_duplicate(elites):
                elites = sample(ga_data.population[:-1], num_elites)
                loop_counter += 1
                if loop_counter >= len(ga_data.children):
                    break
            elites.append(ga_data.population[-1])

        ga_data.children.extend(elites)

    def execute(self, ga_data: GaData) -> None:
        """
        Execute the new generation creation process.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        ga_data.children.__dict__ = ga_data.population.__dict__
        if not ga_data.population.is_sorted:
            ga_data.population.sort_by_dict()

        num_elites = ga_data.population.num_individ - len(ga_data.children)
        if num_elites > 0:
            self.add_parents(ga_data, num_elites=num_elites)
        else:
            ga_data.children.append(ga_data.population[-1])

        ga_data.population = ga_data.children
        ga_data.population.is_sorted = False
