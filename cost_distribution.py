from typing import List

import matplotlib.pyplot as plt
import numpy as np

from gantry_grid import Gantry


def cost_plot(costs: List[int], x_min, x_max) -> None:
    """
    Plots a histogram of the distribution of the costs for an order given a
    list of the cost for the order.

    Args:
        costs: The list of the build costs for the order.
        x_min (int): Where to start the plot on the x-axis.
        x_max (int): Where to end the plot on the x-axis.
    """
    min = np.min(costs)
    mean = np.round(np.mean(costs), 3)
    median = np.median(costs)
    max = np.max(costs)
    std = np.round(np.std(costs), 3)

    bins = [i + .25 * j for i in range(x_min, x_max) for j in [-1, 1]]

    fig = plt.figure()
    ax = fig.add_subplot(111)
    plt.hist(costs, bins=bins, color='navy')
    plt.ylabel("Frequency")
    plt.xlabel("Build Pallet Cost")
    plt.text(.89, .95,
             "Min: " + str(min) + '\n' +
             "Mean: " + str(mean) + '\n' +
             "Median: " + str(median) + '\n' +
             "Max: " + str(max) + '\n' +
             "SD: " + str(std),
             horizontalalignment='left',
             verticalalignment='top',
             transform=ax.transAxes)

    plt.show()


costs = []
build_index_num = 0

for x in range(100):
    gantry = Gantry()
    gantry.set_base_case()
    gantry.set_order(50)
    gantry.fill_by_product()

    for pallet_num in range(len(gantry.order.order_list)):
        build_cost = gantry.build_spot_cost(pallet_num,
                                            gantry.build_indices[build_index_num])
        costs.append(build_cost)

        # switch to the other build location in the base case
        build_index_num = 1 - build_index_num

cost_plot(costs, 10, 55)
