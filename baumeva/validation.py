# import matplotlib.pyplot as plt
# import numpy as np
# from pymoo.config import Config
# from baumeva.ga import BasePopulation
#
# Config.warnings['not_compiled'] = False
#
# def get_phenotypes(population: BasePopulation) -> list:
#     """
#     Creates a list of phenotypes of all individuals in the population.
#
#     :param population: population data.
#     :return: list of phenotypes of all individuals.
#     """
#     return [individ['phenotype'] for individ in population]
#
#
# def visualize(obj_function, ga_data, axis=1) -> None:
#     """
#     Visualizes a scatter plot containing current population characteristics. Plot is 2-dimensional.
#
#     :param obj_function: objective functions data.
#     :param ga_data: GaData instance containing population and related data.
#     :param axis: 0 if the result should be presented in the variables space, 1 - if in the objective space.
#     :return: None.
#     """
#
#     values = get_phenotypes(ga_data.population)
#
#     if axis == 1:
#         values = list(map(obj_function, values))
#     values = np.array(values)
#
#     plt.scatter(values[:, 0], values[:, 1], facecolors='none', edgecolors='b')
#
#     if ga_data.parents is not None:
#         values = get_phenotypes(ga_data.parents)
#         if axis == 1:
#             values = np.array(list(map(obj_function, values)))
#         values = np.array(values)
#
#         plt.scatter(values[:, 0], values[:, 1], facecolors='none', edgecolors='g')
#
#     values = []
#     for individ in ga_data.population:
#         if individ['rank'] == 1:
#             if axis == 0:
#                 values.append(individ['phenotype'])
#             else:
#                 values.append(obj_function(individ['phenotype']))
#     values = np.array(values)
#     plt.scatter(values[:, 0], values[:, 1], facecolors='none', edgecolors='r')
#
#     if axis == 0:
#         plt.xlabel('x1')
#         plt.ylabel('x2')
#     else:
#         plt.xlabel('f1')
#         plt.ylabel('f2')
#
#     plt.title('Generation ' + str(ga_data.idx_generation))
#     plt.show()
#
# pareto_front = np.array(ga_data.historical_best[-1])
#
# plt.scatter(pareto_front[:, 0], pareto_front[:, 1], facecolors='none', edgecolors='r')
# plt.xlabel('f1')
# plt.ylabel('f2')
# plt.show()
#
# # validation
# # ref_point = np.array([100,100,3])
# #
# # ind = HV(ref_point=ref_point)
# #
# # for step in ga_data.historical_best:
# #     print("HV", ind(np.array(step)), step)
# #
# # print(ind(ref_point))