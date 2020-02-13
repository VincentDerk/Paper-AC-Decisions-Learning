"""
By Vincent Derkinderen (DTAI lab KU Leuven, 2019)

A script to evaluate and create a mean squared sampled error (MSSE) plot for each epoch in the learning process.
The mean squared sampled error is obtained by sampling from the correct model and comparing the utility of the sample
with the utility according to the found_utilities in the epoch.

Input
    Learned models: ./data/results/{drop_prob}_0.5_150/{file}.pl based on presence of {file}_weights.p
    Correct model: ./data/processed/{drop_prob}_0.5_150/{file}.pl

Output
    Plot pdf: ./data/results/{drop_prob}_0.5_150/{file}_msse.pdf
    Plot coordinates: ./data/results/{drop_prob}_0.5_150/{file}_msselatex.txt
"""
import os
import sys
import random
import matplotlib.pyplot as plt

from problog.logic import Not
from problog.engine import DefaultEngine, Term
from problog.program import PrologFile
from problog.tasks.sample import sample

from script_plot import _read_python_plot_info


def main(argv):
    """
    Evaluate each learned ProbLog model based on the mean squared sampled error (MSSE) and report the results using a
    plot of the MSE, MSE_Test, MSSE over each epoch. The mean squared sampled error is obtained by sampling from the
    correct model and comparing the utility of the sample with the utility obtained from the found utilities in that
    epoch.

    Input
    All the ProbLog models to evaluate are obtained from ./data/results/{drop_prob}_0.5_150/{file}_weights.p where
    {file} contains {name}. Where the correct model is assumed to be in ./data/processed/{drop_prob}_0.5_150/{file}.pl

    Output
    A pdf of the plot is saved to ./data/results/{drop_prob}_0.5_150/{file}_msse.pdf
    The coordinates to make a similar plot in latex: ./data/results/{drop_prob}_0.5_150/{file}_msselatex.txt
    """
    args = _argparser().parse_args(argv[1:])
    seed = args.seed
    random.seed(a=seed)
    name = args.name
    drop_prob = args.drop
    nb_of_examples = args.nb_of_examples
    nb_of_samples = args.nb_of_samples
    filepoint = "./data/results/{}_0.5_{}/".format(drop_prob, nb_of_examples)
    filepoint_actual = "./data/processed/{}_0.5_{}/".format(drop_prob, nb_of_examples)

    # Get tasks
    task_list = list()
    for file in os.listdir(filepoint):
        if file.endswith("_weights.p") and name in file:
            task_list.append(file)

    # Create random seeds
    random_seeds = list()
    for i in range(0, len(task_list)):
        random_seeds.append(random.randint(0, 2147000000))

    for task, seed in zip(task_list, random_seeds):
        random.seed(a=seed)

        # Retrieve data (input)
        filename = "{}_0.5_{}/".format(drop_prob, nb_of_examples) + task.replace("_weights.p", ".pl")
        modelpath = filepoint_actual + task.replace("_weights.p", ".pl")
        mse, mse_test, _, found_weights = _read_python_plot_info(filename)
        datapoints = process_file(modelpath, found_weights, nb_of_samples)

        # Report results (output)
        plot_filename = filepoint + task.replace('_weights.p', '_msse.pdf')
        latex_filename = filepoint + task.replace("_weights.p", "_msselatex.txt")
        _save_latex_plot_source(latex_filename, mse, mse_test, datapoints)
        create_python_sampled_error_plot(mse, mse_test, datapoints)
        plt.savefig(plot_filename, bbox_inches='tight')
        # plt.show()
        plt.clf()
        print("Finished %s" % task)


def process_file(modelpath, found_utilities_per_epoch, nb_of_samples=100):
    """
    Get the mean squared sampled error (MSSE) of each utility, for each epoch, by sampling from the actual model and
    comparing the difference in actual and found utility (nb_of_samples samples).
    :param modelpath: The filepath to the correct model to sample from.
    :type modelpath: str
    :param found_utilities_per_epoch: For each epoch, the learned utility for each term.
    :type found_utilities_per_epoch: list[dict[Term, float]]
    :param nb_of_samples: The number of samples to use to compute the MSSE.
    :type nb_of_samples: int
    :return: For each epoch, the mean squared sampled error (MSSE), obtained by sampling 100 times from the actual model
    and comparing the actual utility of the sample with the utility according to the found_utilities in that epoch.
    :rtype: list[float]
    """
    program = PrologFile(modelpath)
    engine = DefaultEngine(label_all=True, keep_order=True)
    db = engine.prepare(program)

    def convert(t):
        if isinstance(t, Not) or str(t.functor) == 'not' or str(t.functor) == '\\+':
            return str(t.args[0]), False
        else:
            return str(t), True
    term_to_correct_utility = {convert(q[0]): q[1].compute_value() for q in engine.query(db, Term('utility', None, None))}

    datapoints = list()
    for found_utilities in found_utilities_per_epoch:
        term_to_found_utility = term_to_correct_utility.copy()
        term_to_found_utility.update({convert(term): utility for term, utility in found_utilities.items()})

        # Evaluate epoch
        error = 0
        for observations in sample(program, n=nb_of_samples, format='dict'):
            # Calculate actual and found value
            correct_value = 0
            found_value = 0
            for term, truth in observations.items():
                observation = (str(term), truth)
                correct_utility_obs = term_to_correct_utility.get(observation, 0)
                found_utility_obs = term_to_found_utility.get(observation, 0)
                correct_value += correct_utility_obs
                found_value += found_utility_obs
            # Store difference of actual and found
            error += (correct_value - found_value)**2
        error = error / nb_of_samples
        datapoints.append(error)
    return datapoints


def create_python_sampled_error_plot(mse, mse_test, errors):
    """
    Create a python plot of the mean squared error (MSE, or MSE_Train and MSE_Test if mse_test is not None) and the
    mean squared sampled error (MSSE) vs epoch using the given information. Afterwards,
    the figure is available via plt, e.g.
            plt.savefig(plot_filename, bbox_inches='tight')
            plt.show()
            plt.clf()

    :param mse: A list containing the mean square error (MSE) for each epoch.
    :type mse: list[float]
    :param mse_test: A list containing the mean square error of the test set (MSE_test) for each epoch.
    :type mse_test: list[float] | None
    :param errors: A list containing the mean squared sampled error (MSSE) for each epoch.
    :type errors: list[float]
    """
    epochs = list(range(0, len(mse)))
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('epoch')

    ax1.set_ylabel('MSE')
    line = ax1.plot(epochs, mse, 'b-')[0]
    ax1.set_yscale('log')

    if mse_test is not None and len(mse_test) > 0:
        line.set_label('MSE_Train')
        line = ax1.plot(epochs, mse_test, 'g^-')[0]
        line.set_label('MSE_Test')
    else:
        line.set_label('MSE')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    ax2.set_ylabel('MSSE', color='tab:red')
    line = ax2.plot(epochs, errors, 'r--')[0]
    ax2.set_yscale('log')
    line.set_label('MSSE')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    # plt.show()


def _save_latex_plot_source(filepath, mse, mse_test, errors):
    """
    Save the coordinates required for the latex (MSE, MSE_test, MSSE vs epoch) plot in format:
    % MSE
    (epoch,mse[epoch])
    ...

    % MSE_test
    (epoch, mse_test[epoch])
    ...

    % MSSE
    (epoch, errors[epoch])
    ...

    :param filepath: The file where to write the coordinates to.
    :type filepath: str
    :param mse: A list containing the mean square error (MSE) for each epoch.
    :type mse: list[float]
    :param mse_test: A list containing the mean square error of the test set (MSE_test) for each epoch.
    :type mse_test: list[float] | None
    :param errors: A list containing the mean squared sampler error (MSSE) for each epoch.
    :type errors: list[float]
    """
    with open(filepath, 'w') as f:
        f.write("% MSE\n")
        for i in range(0, len(mse)):
            f.write("({},{})".format(i, mse[i]))
            f.write("\n\n")

        if mse_test is not None:
            f.write("% MSE_test\n")
            for i in range(0, len(mse_test)):
                f.write("({},{})".format(i, mse_test[i]))
            f.write("\n\n")

        f.write("% MSSE\n")
        for i in range(0, len(errors)):
            f.write("({},{})".format(i, errors[i]))
        f.write("\n")


def _argparser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help="The name of each file that should be processed in "
                                     "./data/results/{drop_prob}_0.5_{nb_of_examples}/filename.")
    parser.add_argument('--drop', '-d', type=float, default=0.5,
                        help='The probability that a term is dropped from the observations.')
    parser.add_argument('--seed', '-s', type=int, default=5,
                        help='The seed to use by the random module.')
    parser.add_argument('--nb_of_examples', '-n', type=int, default=150,
                        help='The number of partial interpretations that make up the dataset of examples.')
    parser.add_argument('--nb_of_samples', '-ns', type=int, default=100,
                        help='The number of samples to take to compute the mean squared sample error.')
    return parser


if __name__ == '__main__':
    main(sys.argv)
