"""
By Vincent Derkinderen (DTAI lab KU Leuven, 2019)

A script to create a ProbLog dataset (script_dataset.py) and perform a maximisation experiment on it.

Input files are read from ./data/raw/inputfile.pl and files will be created in ./data/processed/,
./data/results/constrained/ and ./data/results/unconstrained/
"""
import sys
import os
import pickle
import random
import maxeu
import gradientmeu

from script_dataset import create_dataset, create_dataset2
from script_learning import Printer
from problog.program import PrologFile
from problog.engine import DefaultEngine


def main(argv):
    """
    See maximisation_experiment(...)
    """
    args = _argparser().parse_args(argv[1:])
    seed = args.seed
    random.seed(a=seed)
    name = args.inputfile
    decision = args.decisions
    approach = args.approach  # 'constrained' or 'both'
    repeat = args.repeat
    max_epoch = args.max_epoch
    lr = args.lr
    maximisation_experiment(name, decision, approach, repeat, max_epoch, lr)

# - [d1,d2] x10	(5 = verschillend aantal utility values, nodes, beslissingen en SDDX keuze)
# - [survey, asia, earthquake, sachs, child]


def maximisation_experiment(name, decision, approach, repeat=10, max_epoch=80, lr=0.01):
    """
    Create a dataset (determined by decision) and perform maximisation using either a constrained
    or unconstrained (gradient ascent) approach.

    The model on which the dataset is read from ./data/raw/{name}.pl The created dataset will be stored in
    ./data/processed/{name}_{decision}_{used_seed}.pl

    The results, [decisions, eu, size, compile_time, runtime] are stored in
    ./data/results/constrained/{name}_{decision}_{used_seed}_decisionresults.p or
    ./data/results/unconstrained/{name}_{decision}_{used_seed}_decisionresults.p depending on the approach
    with
        * decisions, the a dictionary mapping each Term to its truth value (1 or 0),
        * eu, the maximum expected utility, obtained from the decisions,
        * size, the size reported by the SDD circuit used in the process,
        * compile_time, the time required to create the SDD circuit,
        * runtime, the total runtime of the process (incl. compile_time).
    When approach == 'unconstrained' or 'both', the expected utility of each epoch (list[float]) is stored in:
    ./data/results/unconstrained/{name}_{decision}_{used_seed}_euprogress.p

    A log is stored in ./data/results/constrained/{name}_{decision}_{used_seed}_log.txt (similar for unconstrained).

    :param name: The name of the model to base the dataset on such that the model is in ./data/raw/{name}.pl
    :param decision: The method to use to create a dataset, 1 for create_dataset(..) or 2 for create_dataset2(..)
    :param approach: The approach to use to do maximisation, 'constrained', 'unconstrained' or 'both'.
    :param repeat: The amount of times to repeat the experiment.
    :param max_epoch: The maximum amount of iterations. Only relevant for the unconstrained approach.
    :param lr: The initial learning rate to use. Only relevant for the unconstrained approach.
    :type name: str
    :type decision: int
    :type approach: str
    :type max_epoch: int
    :type lr: int
    """
    random_seeds = list()
    for i in range(0, repeat):
        random_seeds.append(random.randint(0, 2147000000))

    for seed in random_seeds:
        random.seed(a=seed)

        # Create dataset
        new_filename = name + "_{}_{}.pl".format(decision, seed)
        if decision == 1:
            model_path = create_dataset(filename=name + ".pl", n=1, new_filename=new_filename,
                                        decisions=True, learning=False)
        else:
            model_path = create_dataset2(filename=name + ".pl", n=1, new_filename=new_filename,
                                         decisions=True, learning=False, nb_utility_nodes=5, samples_per_utility_node=5)

        # Evaluate
        if approach == 'constrained' or approach == 'both':
            top_folder = "./data/results/constrained/"
            os.makedirs(os.path.dirname(top_folder), exist_ok=True)
            logpath = top_folder + new_filename.replace('.pl', '_log.txt')
            with open(logpath, 'w') as f:
                maxeu.printer = Printer(f)
                engine = DefaultEngine(label_all=True, keep_order=True)
                db = engine.prepare(PrologFile(model_path))

                # Find max EU of correct
                decisions, eu, size, compile_time, runtime = maxeu.get_best_decision(db)

                with open(top_folder + new_filename.replace('.pl', '_decisionresults.p'), 'wb') as f:
                    pickle.dump([decisions, eu, size, compile_time, runtime], f)
            print("")
            print("\n")
            print("Constrained results")
            print("Decisions %s" % decisions)
            print("Expected utility %s" % eu)

        if approach == 'unconstrained' or approach == 'both':
            top_folder = "./data/results/unconstrained/"
            os.makedirs(os.path.dirname(top_folder), exist_ok=True)
            logpath = top_folder + new_filename.replace('.pl', '_log.txt')
            with open(logpath, 'w') as f:
                gradientmeu.printer = Printer(f)
                grad_maximiser = gradientmeu.get_maximisation(model_path, learning_rate=lr, max_epoch=max_epoch)
                grad_maximiser.prepare()
                decisions, eu, size = grad_maximiser.maximise_adaptive_w_restarts()
                compile_time = grad_maximiser.compile_time
                runtime = compile_time + grad_maximiser.runtime

                with open(top_folder + new_filename.replace('.pl', '_decisionresults.p'), 'wb') as f2:
                    pickle.dump([decisions, eu, size, compile_time, runtime], f2)

                with open(top_folder + new_filename.replace('.pl', '_euprogress.p'), 'wb') as f2:
                    pickle.dump(grad_maximiser.log.eu_per_epoch, f2)
            print("")
            print("\n")
            print("Unconstrained results")
            print("Decisions %s" % decisions)
            print("Expected utility %s" % eu)


def _argparser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', help="The name of the file located in ./data/raw/inputfile.pl")
    parser.add_argument('--decisions', '-d', type=int, default=1,
                        help='The method used to add decisions. Use 1 or 2.')
    parser.add_argument('--approach', '-a', type=str, default='constrained',
                        help="Which approach to use, 'constrained', 'unconstrained' or 'both'.")
    parser.add_argument('--seed', '-s', type=int, default=5,
                        help='The seed to use by the random module.')
    parser.add_argument('--repeat', '-r', type=int, default=10,
                        help='The amount of times to repeat the experiment.')
    parser.add_argument('--max_epoch', '-e', type=int, default=80,
                        help='The maximum amount of epochs to use (irrelevant for the constrained approach).')
    parser.add_argument('--lr', type=float, default=1.0,
                        help='The initial learning rate to use (irrelevant for the constrained approach).')
    return parser


if __name__ == '__main__':
    main(sys.argv)
