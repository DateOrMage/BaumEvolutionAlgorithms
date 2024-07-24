from .multi_ga_data import MultiGaData
from .new_generation import NewGeneration


class MultiNewGeneration(NewGeneration):
    """
    Class for creating a new generation of individuals in a genetic algorithm in case of multiobjective optimization.
    """

    def add_best(self, ga_data: MultiGaData, num_elites):
        """
        Add best parent individuals to the offspring (elitism strategy).

        :param ga_data: MultiGaData instance containing population and related data.
        :param num_elites: number of parent individuals to add.
        :return: list of elites to add to the population.
        """
        elites = []

        for individ in ga_data.population:
            if individ['rank'] == 1:
                elites.append(individ)
            else:
                break

        return elites

    def execute(self, ga_data: MultiGaData) -> None:
        """
        Execute the new generation creation process.

        :param ga_data: MultiGaData instance containing population and related data.
        :return: None
        """
        ga_data.children.__dict__ = ga_data.population.__dict__
        if ga_data.population.is_phenotype:
            ga_data.population.get_phenotype()
        # ga_data.assign_ranks()
        # if not ga_data.population.is_sorted:
        #     ga_data.population.sort_by_dict('rank')

        self.add_parents(ga_data, num_elites=10)

        ga_data.population = ga_data.children
        ga_data.population.is_sorted = False
