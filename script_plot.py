"""
By Vincent Derkinderen (DTAI lab KU Leuven, 2019)

A script to create a plot for each previously executed learning experiment that resulted in a _mse.p file in the
specified folder.

The results are read from ./data/results/{folder}{file}_mse.p, _mse_test.p, _correct_results.p and weights.p.
The plot (coordinates) is saved in ./data/results/{folder}[file}.pdf (plot_latex.txt)
"""
import sys
import matplotlib.pyplot as plt
from script_learning import _read_python_plot_info, _create_python_plot, _save_latex_plot_source


def main(argv):
    """
    For each file {file}_mse.p in ./data/results/{folder}, retrieves the mse, mse_test and found weights and uses it to
    create a plot in ./data/results/{folder}{file}.pdf and save the coordinates to be used in latex for the plot, in:
    ./data/results/{folder}{file}plot_latex.txt
    """
    args = _argparser().parse_args(argv[1:])
    folder = args.folder  # '0.0_0.5_150/'
    filepath = "./data/results/" + folder

    import os
    for file in os.listdir(filepath):
        if file.endswith("_mse.p") and ("True" in file or "False" in file):
            filename = file.replace("_mse.p", ".pl")
            mse, mse_test, correct_weights, weights = _read_python_plot_info(folder + filename)
            _create_python_plot(mse, mse_test, weights, correct_weights, log_scale=True)
            plot_filename = "./data/results/" + folder + filename.replace('.pl', '.pdf')
            plt.savefig(plot_filename, bbox_inches='tight')
            # plt.show()
            plt.clf()
            latex_filename = "./data/results/" + folder + filename.replace(".pl", "plot_latex.txt")
            _save_latex_plot_source(latex_filename, mse, mse_test, weights, correct_weights)


def _argparser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('folder', help="The name of the folder in ./data/results/ to search in, e.g. '0.0_0.5_150/'")
    return parser


if __name__ == '__main__':
    main(sys.argv)
