from .tournament_selection import TournamentSelection
from baumeva.ga import MultiGaData


class VEGATournamentSelection(TournamentSelection):
    """
    Class for implementing tournament selection in a genetic algorithm (for multiobjective optimization
    with the VEGA algorithm).
    Inherits from TournamentSelection.
    """

    idx: int = 0

    def __init__(self, num_obj_functions: int, tournament_size: int = 3):
        """
        Initialize the TournamentSelection instance.

        :param num_obj_functions: The number of objectives.
        :param tournament_size: The size of each tournament (default: 3).
        :return: None
        """
        self.num_obj_functions = num_obj_functions
        super().__init__(tournament_size=tournament_size)

    def get_best(self, tournament: list, ga_data: MultiGaData):
        """
        Get the best individual from a tournament.

        :param tournament: List of indices representing the tournament participants.
        :param ga_data: MultiGaData instance containing population and related data.
        :return: The best individual from the tournament.
        """
        best = ga_data.population[tournament[0]]
        for idx in tournament[1:]:
            if ga_data.population[idx]['score'][self.idx] > best['score'][self.idx]:
                best = ga_data.population[idx]
        return best

    def get_total_num_parents(self, ga_data: MultiGaData) -> int:
        """
        Method for calculation the total number of parents to select.

        :param ga_data: MultiGaData instance containing population and related data.
        :return: total number of parents.
        """
        return int(ga_data.children_percent*ga_data.population.num_individ/self.num_obj_functions)

    def tournament(self, ga_data: MultiGaData) -> None:
        """
        Perform the tournament selection process. At the end n (ga_data.children_percent *
            * ga_data.population.num_individ / num_obj_functions for now) parents selected.

        :param ga_data: GaData instance containing population and related data.
        :return: None
        """
        for self.idx in range(self.num_obj_functions):

            super().tournament(ga_data)

    def execute(self, ga_data: MultiGaData) -> None:
        """
        Execute the tournament selection operation.

        :param ga_data: MultiGaData instance containing population and related data.
        :return: None
        """
        super().execute(ga_data)
