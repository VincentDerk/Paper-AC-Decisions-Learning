"""
By Vincent Derkinderen (DTAI lab KU Leuven, 2019)

Small code example that was used to interactively extract information from previous learning experiments.
"""
import sys
import statistics
from script_learning import _construct_rel_error_list, _read_python_plot_info,_create_python_plot
import matplotlib.pyplot as plt


def main(args):

    results = list()
    datapoints = dict()
    for drop_prob in [0.0, 0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9]:
        folder = '{}_0.5_150/'.format(drop_prob)
        filepath = "./data/results/" + folder

        import os
        for file in os.listdir(filepath):
            if file.endswith("_mse.p") and ('False' in file) and 'survey' in file:
                filename = file.replace('_mse.p', '') + ".pl"
                mse, mse_test, correct_weights, weights = _read_python_plot_info(folder + filename)
                mre = [statistics.mean(_construct_rel_error_list(correct_weights, c_weights)) for c_weights in weights]
                id = file.split("_")[2]
                if datapoints.get(id) is None:
                    datapoints[id] = [(drop_prob, [mse[-1], mse_test, mre[-1]])]
                else:
                    datapoints.get(id).append((drop_prob, [mse[-1], mse_test, mre[-1]]))

        #error = [0] * 81
        #for file, [mse, mse_test, mre] in datapoints.items():
        #    for i in range(0, 81):
        #        error[i] += mre[i]
        #for i in range(0,81):
        #    error[i] /= len(datapoints)
        #results.append(error)
    for file, results in datapoints.items():
        coordinates = ["({},{})".format(drop_prob, mre) for drop_prob, [mse, mse_test, mre] in results]
        print("")


if __name__ == '__main__':
    main(sys.argv)
