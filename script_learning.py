"""
By Vincent Derkinderen (DTAI lab KU Leuven, 2019)

A script to create a ProbLog dataset (script_dataset.py) and perform a learning experiment on it.

Input files are read from ./data/raw/inputfile.pl and files will be created in ./data/processed/ and ./data/results/
"""
import os
import sys
import ulearner
import experiments_utils as utils
import time
import random
import statistics
import pickle
from script_dataset import create_dataset


def main(argv):
    args = _argparser().parse_args(argv[1:])

    filename = args.inputfile
    max_epoch = args.max_epoch
    drop_prob = args.drop
    left_out = args.left_out
    repeat = args.repeat
    seed = args.seed
    nb_of_examples = args.nb_of_examples
    experiments(filename, max_epoch=max_epoch, drop_prob=drop_prob, left_out=left_out, seed=seed, repeat=repeat,
                nb_of_examples=nb_of_examples)
    #experiments('survey', nb=5, max_epoch=80, drop_prob=0.25, left_out=True)    # 27
    #experiments('survey', nb=5, max_epoch=80, drop_prob=0.25, left_out=False)  # 24
    #experiments('survey', nb=5, max_epoch=80, drop_prob=0.5, left_out=True)    # 25
    #experiments('survey', nb=5, max_epoch=80, drop_prob=0.5, left_out=False)   # 26
    #experiments('survey', nb=5, max_epoch=80, drop_prob=0.75, left_out=True)   # 23
    #experiments('survey', nb=5, max_epoch=80, drop_prob=0.75, left_out=False)  # 26    5       (0.4, True)
    #experiments('asia', nb=5, max_epoch=80, drop_prob=0.5, left_out=True)      # 25    6   D   (0.2, True)
    #experiments('asia', nb=5, max_epoch=80, drop_prob=0.5, left_out=False)     # 24    7   D
    #experiments('survey', nb=5, max_epoch=80, drop_prob=0.0, left_out=True)   # 27     8   (0.1, True)
    #experiments('survey', nb=5, max_epoch=80, drop_prob=0.0, left_out=False)  # 23     9


def temp(argv):
    # TODO Documentation if used.
    import matplotlib.pyplot as plt
    args = _argparser().parse_args(argv[1:])

    filename = args.inputfile
    seed = args.seed
    random.seed(a=seed)

    print("Running filename %s with seed %s" % (filename, seed))
    real_model_filename = "./data/processed/" + filename
    input_model_filename = "./data/processed/" + filename.replace('.pl', '') + "_input.pl"
    examples = "./data/processed/" + filename.replace('.pl', '') + "_examples.pl"

    mse, mse_test, weights, correct_weights, _ = test_learning(real_model_filename, input_model_filename, examples,
                                                               filename, max_epoch=80, adaptive_learning_rate=True,
                                                               left_out=True)
    _create_python_plot(mse, mse_test, weights, correct_weights)
    plt.show()


def experiments(name, repeat=5, max_epoch=80, drop_prob=0.25, left_out=True, seed=None, nb_of_examples=100):
    """
    Create a learning dataset for name and perform the learning process. Do this nb times.
    The following files are created for each run with
    new_filename = {drop_prob}_{prob_of_unknown}_{nb_of_examples}/{name}_{max_epoch}_{used_seed}_{left_out}:
    DATASET
    * The model with utilities and all queries, in ./data/processed/{new_filename}.pl
    * The previous model with some utilities made unknown, in ./data/processed/{new_filename}_input.pl
    * A file of nb_of_examples partially observed examples in ./data/processed/{new_filename}_examples.pl
    LEARNING
    * A plot of MSE, MRE vs epoch: ./data/results/{new_filename}.pdf
    * The LaTeX coordinates to use for the plot: ./data/results/{new_filename}_coords.txt
    * The log file in ./data/results/{new_filename}.txt
    * The found_results (dict of term to utility) in ./data/results/{new_filename}_found_results.p
    * The correct_results (dict of term to utility) in ./data/results/{new_filename}_correct_results.p
    * The mse for each epoch (list of float) in ./data/results/{new_filename}_mse.p
    * The test set mse for each epoch (list of float) in ./data/results/{new_filename}_mse_test.p
    * The weights for each epoch (list of dict[Term,float]) in ./data/results/{new_filename}_weights.p
    * The input model where the unknown utilities are replaced with the found weights, in
        ./data/results/{new_filename}_result.pl
    This dataset creation relies on the ProbLog file ./data/raw/name.pl
    :param name: The name of the file to create a dataset for, ./data/raw/name.pl
    :param repeat: The number of times the experiment should be repeated.
    :param max_epoch: The maximum amount of epochs in the gradient ascent process before it should stop.
    :param drop_prob: The probability that an observation (term) is dropped from an example. Used to create the dataset.
    :param left_out: Whether a third of the data should be left out and used for testing instead of training.
    :param seed: The seed to use. When None, a specific set value is used.
    :param nb_of_examples: The amount of partial interpretations that should make up the examples dataset.
    """
    if seed is None:
        seed = 5
    random.seed(a=seed)
    random_seeds = [random.randint(0, 2147000000) for x in range(0, repeat)]
    prob_of_unknown = 0.5
    create_plots = True

    for seed in random_seeds:
        # Create dataset
        random.seed(a=seed)
        filename = name + '.pl'
        new_filename = "{}_{}_{}/{}_{}_{}_{}.pl".format(drop_prob, prob_of_unknown, nb_of_examples, name, max_epoch, seed, left_out)
        os.makedirs(os.path.dirname('./data/results/{}_{}_{}/'.format(drop_prob, prob_of_unknown, nb_of_examples)),
                    exist_ok=True)
        os.makedirs(os.path.dirname('./data/processed/{}_{}_{}/'.format(drop_prob, prob_of_unknown, nb_of_examples)),
                    exist_ok=True)
        real_model_filename, input_model_filename, examples_filename = create_dataset(filename=filename,
                                                                                      new_filename=new_filename,
                                                                                      n=nb_of_examples,
                                                                                      decisions=False,
                                                                                      learning=True,
                                                                                      drop_prob=drop_prob,
                                                                                      prob_of_unknown=prob_of_unknown,
                                                                                      verbose=False)
        # Perform learning
        mse, mse_test, weights, correct_weights, _ = test_learning(real_model_filename, input_model_filename,
                                                                   examples_filename, new_filename, max_epoch=max_epoch,
                                                                   adaptive_learning_rate=True, left_out=left_out)

        # Create plot epoch vs MSE VS MRE
        if create_plots:
            import matplotlib.pyplot as plt
            _create_python_plot(mse, mse_test, weights, correct_weights)
            plot_filename = "./data/results/" + new_filename.replace('.pl', '.pdf')
            plt.savefig(plot_filename, bbox_inches='tight')
            #plt.show()
            plt.clf()

        # Save 'coordinates' for LaTeX doc
        latex_coords_filename = "./data/results/" + new_filename.replace('.pl', '') + "_coords.txt"
        _save_latex_plot_source(latex_coords_filename, mse, mse_test, weights, correct_weights)


def _save_latex_plot_source(filepath, mse, mse_test, weights, correct_weights):
    """
    Save the coordinates required for the latex (MSE, MSE_test, MRE vs epoch) plot in format:
    % MSE
    (epoch,mse[epoch])
    ...

    % MSE_test
    (epoch, mse_test[epoch])
    ...

    % MRE
    (epoch, mre[epoch])
    ...

    :param filepath: The file where to write the coordinates to.
    :type filepath: str
    :param mse: A list containing the mean square error (MSE) for each epoch.
    :type mse: list[float]
    :param mse_test: A list containing the mean square error of the test set (MSE_test) for each epoch.
    :type mse_test: list[float]
    :param weights: A list containing the weights (dict of term to utility) for each epoch.
    :type weights: list[dict[Term, float]]
    :param correct_weights: The correct weight for each term (dictionary).
    :type correct_weights: dict[Term, float]
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

        f.write("% MRE\n")
        for i in range(0, len(weights)):
            rme = statistics.mean(_construct_rel_error_list(correct_weights, weights[i]))
            f.write("({},{})".format(i, rme))
        f.write("\n")


def _read_python_plot_info(filename):
    """
    Read the information required for a python plot for the given filename. The data for this are assumed to be in:
    ./data/results/filename_mse.p, ./data/results/filename_mse_test.p, ./data/results/filename_correct_results.p and
     ./data/results/filename_weights.p
    Afterwards, one can call _create_python_plot(mse, mse_test, weights, correct_weights)
    :param filename: The filename from which to obtain the mse, mse_test, correct weights and found weights.
    :type filename: str
    :return: The mse for each epoch, the mse of the test set for each epoch, the correct weights and the weights found
    in each epoch.
    :rtype: list[float], list[float], dict[Term,float], list[dict[Term, float]]
    """
    mse_filename = './data/results/' + filename.replace('.pl', '') + '_mse.p'
    mse_test_filename = './data/results/' + filename.replace('.pl', '') + '_mse_test.p'
    correct_weights_filename = './data/results/' + filename.replace('.pl', '') + '_correct_results.p'
    found_weights_filename = './data/results/' + filename.replace('.pl', '') + '_weights.p'

    with open(mse_filename, 'rb') as f:
        mse = pickle.load(f)

    with open(mse_test_filename, 'rb') as f:
        mse_test = pickle.load(f)

    with open(correct_weights_filename, 'rb') as f:
        correct_weights = pickle.load(f)

    with open(found_weights_filename, 'rb') as f:
        found_weights = pickle.load(f)

    return mse, mse_test, correct_weights, found_weights


def _create_python_plot(mse, mse_test, weights, correct_weights, log_scale=False):
    """
    Create a python plot of MSE, MSE_test, MRE vs epoch using the given information. Afterwards,
    the figure is available via plt, e.g.
            plt.savefig(plot_filename, bbox_inches='tight')
            plt.show()
            plt.clf()

    :param mse: A list containing the mean square error (MSE) for each epoch.
    :type mse: list[float]
    :param mse_test: A list containing the mean square error of the test set (MSE_test) for each epoch.
    :type mse_test: list[float]
    :param weights: A list containing the weights (dict of term to utility) for each epoch.
    :type weights: list[dict[Term, float]]
    :param correct_weights: The correct weight for each term (dictionary).
    :type correct_weights: dict[Term, float]
    :param log_scale: Whether to use log scale for MSE.
    :type log_scale: bool
    """
    import matplotlib.pyplot as plt
    epochs = list(range(0, len(mse)))
    mre = [statistics.mean(_construct_rel_error_list(correct_weights, c_weights)) for c_weights in weights]

    fig, ax1 = plt.subplots()
    ax1.set_xlabel('epoch')

    ax1.set_ylabel('MSE')
    line = ax1.plot(epochs, mse, 'b-')[0]
    if log_scale:
        ax1.set_yscale('log')

    if mse_test is not None and len(mse_test) > 0:
        line.set_label('MSE_Train')
        line = ax1.plot(epochs, mse_test, 'g^-')[0]
        line.set_label('MSE_Test')
    else:
        line.set_label('MSE')

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    ax2.set_ylabel('MRE', color='tab:red')
    line = ax2.plot(epochs, mre, 'r--')[0]
    line.set_label('MRE')
    ax2.tick_params(axis='y', labelcolor='tab:red')

    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    #plt.show()


def test_learning(real_model_filename, input_model_filename, examples_filename, new_filename,
                  max_epoch=80, adaptive_learning_rate=False, left_out=False):
    """
    Test the learning process for the given input model and examples, evaluating based on the given real model and
    writing the results based on new_filename.
    Creates the following files:
    * log file in ./data/results/new_filename.replace(.pl,.txt)
    * found_results (dict of term to utility) in ./data/results/new_filename.replace('.pl', '')_found_results.p
    * correct_results (dict of term to utility) in ./data/results/new_filename.replace('.pl', '')_correct_results.p
    * mse for each epoch (list of float) in ./data/results/new_filename.replace('.pl', '')_mse.p
    * test set mse for each epoch (list of float) in ./data/results/new_filename.replace('.pl', '')_mse_test.p
    * weights for each epoch (list of dict[Term,float]) in ./data/results/new_filename.replace('.pl', '')_weights.p
    * input model where the unknown utilities are replaced with the found weights, in
        ./data/results/new_filename.replace('.pl', '')_result.pl
    :param real_model_filename: The path to the real model (known utilities), used to evaluate the learning process.
    :type real_model_filename: str
    :param input_model_filename: The path to the input of the learning process (model with unknown utilities).
    :type input_model_filename: str
    :param examples_filename: The path to the examples used in the learning process (partially observed examples).
    :type examples_filename: str
    :param new_filename: The filename used when creating new files.
    :type new_filename: str
    :param max_epoch: The maximum amount of epochs in the gradient ascent process before it should stop.
    :param adaptive_learning_rate: Whether to dynamically change the learning rate when results improve/worsen.
    :param left_out: Whether a third of the data should be left out and used for testing instead of training.
    :return: ulearn.log.mse, ulearn.log.mse_test, ulearn.log.weights, correct_results, rel_error_list
    :rtype: list[float], list[float], list[dict[Term, float]], dict[Term, float], list[float]
    """
    learning_rate = 0.2
    batch_size = None
    increase_rate = 1.05  # adaptive learning rate
    decrease_rate = 0.8  # adaptive learning rate

    ulearn = ulearner.get_ulearner(input_model_filename, examples_filename,
                                   max_epoch=max_epoch, learning_rate=learning_rate, batch_size=batch_size)
    correct_results = utils.get_term_to_utilities(real_model_filename)

    os.makedirs(os.path.dirname('./data/results/'), exist_ok=True)
    with open('./data/results/' + new_filename.replace('.pl', '.txt'), 'w') as f:
        printer = Printer(f)
        ulearn.printer = printer
        # Learning
        _print_parameters(adaptive_learning_rate, increase_rate, decrease_rate, max_epoch, learning_rate, batch_size,
                      left_out, printer)
        actual_results = _learn(ulearn, adaptive_learning_rate, increase_rate, decrease_rate, left_out, printer)

        # Report progress & save
        printer.print("MSE")
        mse_results = list(zip(list(range(0, len(ulearn.log.mse))), ulearn.log.mse))
        for epoch_nr, mse in mse_results:
            printer.print("Total MSE after epoch {} is {}".format(epoch_nr, mse))

        printer.print("")
        printer.print("TEST_MSE")
        mse_test_results = list(zip(list(range(0, len(ulearn.log.mse_test))), ulearn.log.mse_test))
        for epoch_nr, mse_test in mse_test_results:
            printer.print("Test_MSE after epoch {} is {}".format(epoch_nr, mse_test))

        printer.print("")
        printer.print("Weights")
        weight_results = list(zip(list(range(0, len(ulearn.log.weights))), ulearn.log.weights))
        for epoch_nr, weights in weight_results:
            printer.print("Weights after epoch %s is %s" % (epoch_nr, weights))

        printer.print("")
        printer.print("Weight errors")
        for epoch_nr, weights in weight_results:
            w_error = statistics.mean(_construct_rel_error_list(correct_results, weights))
            printer.print("Weight errors after epoch %s is %s" % (epoch_nr, w_error))

        # Evaluate results
        printer.print("----------------------")
        printer.print("RESULTS")
        rel_error_list = _construct_rel_error_list(correct_results, actual_results, printer)
        printer.print("Mean relative error: %s" % statistics.mean(rel_error_list))
        printer.print("Median of relative error: %s" % statistics.median(rel_error_list))
        printer.print("Variance of relative error: %s" % statistics.pvariance(rel_error_list))
        printer.print("Minimum relative error: %s" % min(rel_error_list))
        printer.print("Maximum relative error: %s" % max(rel_error_list))

        # Report correct results
        ulearn.set_current_util_weights(correct_results)
        actual_mse = ulearn.mse(ulearn.get_processed_examples())
        printer.print("----------------------------------------------")
        printer.print("MSE of actual solution: %s" % actual_mse)
        printer.print("Expected weights: %s" % correct_results)
        printer.print("Found weights: %s" % actual_results)

    # Save
    with open('./data/results/' + new_filename.replace('.pl', '') + '_found_results.p', 'wb') as f:
        pickle.dump(actual_results, f)
    with open('./data/results/' + new_filename.replace('.pl', '') + '_correct_results.p', 'wb') as f:
        pickle.dump(correct_results, f)
    with open('./data/results/' + new_filename.replace('.pl', '') + '_mse.p', 'wb') as f:
        pickle.dump(ulearn.log.mse, f)
    with open('./data/results/' + new_filename.replace('.pl', '') + '_weights.p', 'wb') as f:
        pickle.dump(ulearn.log.weights, f)
    if ulearn.log.mse_test is not None:
        with open('./data/results/' + new_filename.replace('.pl', '') + '_mse_test.p', 'wb') as f:
            pickle.dump(ulearn.log.mse_test, f)

    results_path = './data/results/' + new_filename.replace('.pl', '') + '_result.pl'
    utils.save_db_w_replaced_utilities(ulearn.db, results_path, actual_results)

    return ulearn.log.mse, ulearn.log.mse_test, ulearn.log.weights, correct_results, rel_error_list

    #print("Gradients")
    #print(list(zip(list(range(0, len(ulearn.log.gradients))), ulearn.log.gradients)))


class Printer:
    """
    A class used to abstract the writing of a message to a console or a file or, ...
    """

    def __init__(self, f):
        """
        Create an instance of a printer that prints messages to file f and to the console.
        :param f: The file to write the messages to. This file must be opened and closed by the user.
        """
        self.f = f

    def print(self, msg):
        """ Prints the given message """
        print(msg)
        self.f.write(msg + "\n")


def _construct_rel_error_list(correct_results, actual_results, printer=None, verbose=False):
    """
    Construct a list providing the relative utility error for each term in actual_results.
    Each term in actual_results must be present in correct_results.
    :param correct_results: The correct utility for each term.
    :type correct_results: dict[Term, float]
    :param actual_results: The found utility for each term.
    :type actual_results: dict[Term, float]
    :param printer: The printer to write the information to.
    :type printer: Printer
    :param verbose: Whether to print intermediate information.
    :type verbose: bool
    """
    rel_error_list = list()
    for term, found_utility in actual_results.items():
        correct_utility = correct_results[term]
        error = (abs(correct_utility - found_utility))
        if correct_utility != 0:
            rel_error = error / abs(correct_utility)
            rel_error_list.append(rel_error)
        else:
            rel_error = '-'
        if printer is None and verbose:
            print("Expected: %s; \t Found: %s; \t Error: %s; \t Relative error: %s; \t For term: %s;" %
                  (correct_utility, found_utility, error, rel_error, term))
        elif printer is not None:
            printer.print("Expected: %s; \t Found: %s; \t Error: %s; \t Relative error: %s; \t For term: %s;" %
                          (correct_utility, found_utility, error, rel_error, term))
    return rel_error_list


def _print_parameters(adaptive_learning_rate, increase_rate, decrease_rate, max_epoch, learning_rate, batch_size, left_out, printer):
    """
    Print the given parameters using the given printer.

    :param adaptive_learning_rate: Whether to dynamically change the learning rate when results improve/worsen.
    :type adaptive_learning_rate: bool
    :param increase_rate: The rate with which to multiply the learning rate when an improvement was found (>= 1).
    :type increase_rate: float
    :param decrease_rate: The rate with which to multiply the learning rate when a worse solution was found (<= 1)
    :type decrease_rate: float
    :param max_epoch: The maximum amount of epochs in the gradient ascent process before it should stop.
    :type max_epoch: int
    :param learning_rate: The learning rate to start the gradient ascent process with.
    :type learning_rate: float
    :param batch_size: The batch size to use.
    :type batch_size: (int | None)
    :param left_out: Whether a third of the data should be left out and used for testing instead of training.
    :type left_out: bool
    :param printer: The printer to write the information to.
    :type printer: Printer
    """
    printer.print("----------------------------------------------")
    if adaptive_learning_rate:
        printer.print("Running adaptive_learning_rate learning with:")
        printer.print("\t learning_rate's increase_rate: %s" % increase_rate)
        printer.print("\t learning_rate's decrease_rate: %s" % decrease_rate)
        printer.print("\t Left out approach: %s" % left_out)
    else:
        printer.print("Running normal learning with:")
    printer.print("\t max_epoch: %s" % max_epoch)
    printer.print("\t learning_rate: %s" % learning_rate)
    printer.print("\t batch_size: %s" % batch_size)
    printer.print("----------------------------------------------")


def _learn(ulearn, adaptive_learning_rate, increase_rate, decrease_rate, left_out, printer):
    """
    Perform the learning process on ulearn with the given parameters.
    Prints the preparation and learning time of the process using the printer.

    :param ulearn: The learning object
    :type ulearn: ULearner
    :param adaptive_learning_rate: Whether to dynamically change the learning rate when results improve/worsen.
    :type adaptive_learning_rate: bool
    :param increase_rate: The rate with which to multiply the learning rate when an improvement was found (>= 1).
    :type increase_rate: float
    :param decrease_rate: The rate with which to multiply the learning rate when a worse solution was found (<= 1).
    :type decrease_rate: float
    :param left_out: Whether a third of the data should be left out and used for testing instead of training.
    :type left_out: bool
    :param printer: The printer to write logging information to.
    :type printer: Printer
    """
    # Prepare
    starttime = time.time()
    ulearn.prepare()
    endtime = time.time()
    printer.print("Preparation took %s seconds" % (endtime - starttime))

    # Learn
    starttime = time.time()
    if adaptive_learning_rate and left_out:
        left_out_rate = 0.3333
        printer.print("Using %s of the data to validate." % left_out_rate)
        actual_results = ulearn.learn_adaptive_rate_left_out(increase_rate=increase_rate, decrease_rate=decrease_rate,
                                                             left_out=left_out_rate)
    elif adaptive_learning_rate and not left_out:
        actual_results = ulearn.learn_adaptive_rate(increase_rate=increase_rate, decrease_rate=decrease_rate)
    else:
        actual_results = ulearn.learn()
    endtime = time.time()
    printer.print("---")
    printer.print("Ran %s seconds." % (endtime - starttime))
    return actual_results


def _argparser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', help="The name of the file located in ./data/raw/inputfile.pl")
    parser.add_argument('--max_epoch', '-m', type=int, default=80,
                        help='The maximum amount of epochs in the gradient ascent process.')
    parser.add_argument('--drop', '-d', type=float, default=0.5,
                        help='The probability that a term is dropped from the observations.')
    parser.add_argument('--left_out', '-l', type=bool, default=False,
                        help='Whether to leave out a third of the data and use its signal to stop the process.')
    parser.add_argument('--repeat', '-r', type=int, default=5,
                        help='The number of times the experiment should be repeated.')
    parser.add_argument('--nb_of_examples', '-n', type=int, default=150,
                        help='The number of partial interpretations that should make up the dataset of examples.')
    parser.add_argument('--seed', '-s', type=int, default=5,
                        help='The seed to use by the random module.')
    return parser


if __name__ == '__main__':
    main(sys.argv)
