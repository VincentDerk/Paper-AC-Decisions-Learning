"""
By Vincent Derkinderen (DTAI lab KU Leuven, 2019)

A script to create a ProbLog dataset from bayesian networks that were compiled into ProbLog programs using ProbLog's
conversion script (12/2019).

Given a ProbLog program of a BN, this can create files used for making decisions or learning (task_type)
* task_type = d: Files used in decision making. Adds decisions based on Annotated Disjunctions and probabilistic facts,
and randomly assigns utilities to terms.
* task_type = d2: Files used in decision making. Adds decisions based on Annotated Disjunctions and probabilistic facts.
For the utilities, new terms are introduced and the body of their rules are constructed using program samples.
* else: files used for learning. Real model: utilities are randomly assigned to terms. Input model: some utilities are
randomly made unknown. Examples to learn from: the real program is sampled and observations are randomly left out.

Input files are read from ./data/raw/inputfile.pl and all files will be created into ./data/processed/
"""
import sys
import shutil
import experiments_utils as utils
import random

from problog.engine import DefaultEngine
from problog.program import PrologFile


def main(argv):
    args = _argparser().parse_args(argv[1:])

    seed = args.seed
    filename = args.inputfile
    drop_prob = args.drop
    prob_of_unknown = args.unknown_prob
    task_type = args.task_type

    if task_type == 'd':  # decisions + utility on existing nodes
        def cr(filename):
            _create_decision_template(name=filename, seed=seed)
    elif task_type == 'd2':  # new utility nodes
        nb_util_nodes = args.nb_util_nodes
        nb_rules = args.nb_rules

        def cr(filename):
            _create_decision_template2(name=filename, seed=seed, nb_of_utility_nodes=nb_util_nodes, nb_of_rules=nb_rules)
    else:   # utility on existing nodes + unknowns + observations
        nb_of_examples = args.nb_of_examples

        def cr(filename):
            _create_template(name=filename, seed=seed, drop_prob=drop_prob, prob_of_unknown=prob_of_unknown,
                             n=nb_of_examples)

    cr(filename)


def _create_decision_template(name, seed):
    random.seed(a=seed)
    filename = name + '.pl'
    new = name + "_decision.pl"
    create_dataset(filename=filename, n=1, new_filename=new, decisions=True, learning=False, verbose=True)


def _create_decision_template2(name, seed, nb_of_utility_nodes, nb_of_rules):
    random.seed(a=seed)
    filename = name + '.pl'
    new = name + "_decision2.pl"
    create_dataset2(filename=filename, n=1, new_filename=new, decisions=True, learning=False,
                    nb_utility_nodes=nb_of_utility_nodes, samples_per_utility_node=nb_of_rules, verbose=True)


def _create_template(name, seed, drop_prob, prob_of_unknown, n):
    random.seed(a=seed)
    filename = name + '.pl'
    create_dataset(filename=filename, n=n, decisions=False, learning=True, drop_prob=drop_prob,
                   prob_of_unknown=prob_of_unknown, verbose=True)


def create_dataset(filename, n, new_filename=None, decisions=True, learning=True, drop_prob=0.25, prob_of_unknown=0.5,
                   verbose=False):
    """
    Create a dataset for problog model ./data/raw/filename.
    The following files will be created:
        * ./data/processed/new_filename - contains the model with each term queried and utilities attached. When
            decisions=True, decisions are also present.
    If learning = True then the following files are also created:
        * ./data/processed/new_filename-without-pl_input.pl - contains the model with each term queried and utilities
            attached. Some utilities are unknown.
        * ./data/processed/new_filename-without-pl_examples.pl - contains n partially observed examples and their utility.
    :param filename: The name of the ProbLog file to create a dataset for.
    :param n: The number of samples to take, aka the number of examples in the resulting examples file.
    :param new_filename: The filename to use for the new files. When none, the original filename appended with
    _{drop_prob}_{prob_of_unknown}_{n}.pl is used.
    :param decisions: Whether to decisions to the dataset.
    :param learning: Whether to also create a file with unknown utilities and observations.
    :param drop_prob: The probability that a term is dropped in an example.
    :param prob_of_unknown: The probability that a utility becomes unknown.
    :param verbose: Whether to print when a stage is finished.
    :type filename: str
    :type n: int
    :type new_filename: str
    :type decisions: bool
    :type learning: bool
    :type drop_prob: float
    :type prob_of_unknown: float
    :type verbose: bool
    """
    raw_model_filename = "./data/raw/" + filename
    if new_filename is None:
        new_filename = filename.replace('.pl', '') + "_{}_{}_{}.pl".format(drop_prob, prob_of_unknown, n)
    processed_real_model_filename = "./data/processed/" + new_filename
    processed_input_model_filename = f"./data/processed/{new_filename.replace('.pl', '')}_input.pl"
    examples_filename = f"./data/processed/{new_filename.replace('.pl', '')}_examples.pl"

    def next_random_utility(t, p):
        return random.randint(-50, 50)

    # Add queries to file
    db = _add_queries(raw_model_filename)
    if decisions:
        db, nb_of_decisions = utils.add_decisions_to_db(db)
        if verbose:
            print("%s decisions added in: %s" % (nb_of_decisions, processed_real_model_filename))
    db_utilities = db.extend()
    db_unknown_utilities = db.extend()

    # Create real model - add utilities
    utils.add_utilities_to_db(db_utilities, next_random_utility, prob_of_utility_for_pos=0.8, prob_of_utility_for_neg=0.5)
    utils.save_db(db_utilities, processed_real_model_filename)
    if verbose:
        print("Utilities added in: %s" % processed_real_model_filename)

    if learning:
        # Create input model - add unknown utilities
        utils.add_unknown_utilities_to_db(db_utilities, db_unknown_utilities, prob_of_unknown=prob_of_unknown)
        utils.save_db(db_unknown_utilities, processed_input_model_filename)
        if verbose:
            print("Unknown utilities added in: %s" % processed_input_model_filename)
        # Create observation file
        examples = utils.create_observations(processed_real_model_filename, n=n)
        examples = utils.drop_observations(examples, drop_prob=drop_prob)
        utils.save_examples(examples, examples_filename)
        if verbose:
            print("Examples constructed: %s" % examples_filename)
        return processed_real_model_filename, processed_input_model_filename, examples_filename
    else:
        return processed_real_model_filename


def create_datasets(filename, n, new_filenames=None, decisions=True, learning=True, drop_probs={0.25},
                    prob_of_unknown=0.5, verbose=False):
    """
    Create a dataset for problog model ./data/raw/filename.
    The following files will be created:
        * ./data/processed/new_filename - contains the model with each term queried and utilities attached. When
            decisions=True, decisions are also present.
    If learning = True then the following files are also created:
        * ./data/processed/new_filename-without-pl_input.pl - contains the model with each term queried and utilities
            attached. Some utilities are unknown.
        * ./data/processed/new_filename-without-pl_examples.pl - contains n partially observed examples and their utility.
    :param filename: The name of the ProbLog file to create a dataset for.
    :param n: The number of samples to take, aka the number of examples in the resulting examples file.
    :param new_filenames: The filenames to use for the new files (dict[drop_prob]:filename). When none, the original
    filename appended with _{drop_prob}_{prob_of_unknown}_{n}.pl is used.
    :param decisions: Whether to decisions to the dataset.
    :param learning: Whether to also create a file with unknown utilities and observations.
    :param drop_probs: The set of probabilities with which a term is dropped in an example. The length of this
    determines the amount of datasets that are created.
    :param prob_of_unknown: The probability that a utility becomes unknown.
    :param verbose: Whether to print when a stage is finished.
    :type filename: str
    :type n: int
    :type new_filenames: dict[float:str]
    :type decisions: bool
    :type learning: bool
    :type drop_probs: set[float]
    :type prob_of_unknown: float
    :type verbose: bool
    """
    raw_model_filename = "./data/raw/" + filename
    drop_probs = list(drop_probs)
    if new_filenames is None:
        new_filenames = {drop_prob: filename.replace('.pl', '') + f"_{drop_prob}_{prob_of_unknown}_{n}.pl" for
                         drop_prob in drop_probs}

    processed_real_model_filenames = {drop_prob: "./data/processed/" + new_filenames[drop_prob] for drop_prob in drop_probs}
    processed_input_model_filenames = {drop_prob: f"./data/processed/{new_filenames[drop_prob].replace('.pl', '')}_input.pl" for drop_prob in drop_probs}
    examples_filenames = {drop_prob: f"./data/processed/{new_filenames[drop_prob].replace('.pl', '')}_examples.pl" for drop_prob in drop_probs}

    def next_random_utility(t, p):
        return random.randint(-50, 50)

    # Add queries to file
    db = _add_queries(raw_model_filename)
    if decisions:
        db, nb_of_decisions = utils.add_decisions_to_db(db)
        if verbose:
            print("%s decisions added in: %s" % (nb_of_decisions, processed_real_model_filenames))
    db_utilities = db.extend()
    db_unknown_utilities = db.extend()

    # Create real model - add utilities
    utils.add_utilities_to_db(db_utilities, next_random_utility, prob_of_utility_for_pos=0.8, prob_of_utility_for_neg=0.5)
    utils.save_db(db_utilities, processed_real_model_filenames[drop_probs[0]])
    for drop_prob in drop_probs[1:]:
        shutil.copyfile(processed_real_model_filenames[drop_probs[0]], processed_real_model_filenames[drop_prob])
    if verbose:
        print("Utilities added in: %s" % processed_real_model_filenames)

    if learning:
        # Create input model - add unknown utilities
        utils.add_unknown_utilities_to_db(db_utilities, db_unknown_utilities, prob_of_unknown=prob_of_unknown)
        utils.save_db(db_unknown_utilities, processed_input_model_filenames[drop_probs[0]])
        for drop_prob in drop_probs[1:]:
            shutil.copyfile(processed_input_model_filenames[drop_probs[0]], processed_input_model_filenames[drop_prob])
        if verbose:
            print("Unknown utilities added in: %s" % processed_input_model_filenames[0])

        # Create observation file
        full_examples = utils.create_observations(processed_real_model_filenames[drop_probs[0]], n=n)
        random_seed = random.randint(0, 2147000000)
        for drop_prob, examples_filename in examples_filenames.items():
            random.seed(a=random_seed)
            examples = utils.drop_observations(full_examples, drop_prob=drop_prob)
            utils.save_examples(examples, examples_filename)
            if verbose:
                print("Examples constructed: %s" % examples_filename)
        return processed_real_model_filenames, processed_input_model_filenames, examples_filenames
    else:
        return processed_real_model_filenames


def create_dataset2(filename, n, new_filename=None, decisions=True, learning=True, drop_prob=0.25,
                    prob_of_unknown=0.5, nb_utility_nodes=5, samples_per_utility_node=5, verbose=False):
    """
    Create a dataset for problog model ./data/raw/filename and introduce new utility facts to the model. For each
    utility fact, samples_per_utility_node rules are introduced such that utility_node :- sampled_observation.
    The following files will be created:
        * ./data/processed/new_filename - contains the model with each term queried and new utility facts introduced.
        When decisions=True, decisions are also present.
    If learning = True then the following files are also created:
        * ./data/processed/new_filename-without-pl_input.pl - contains the model with each term queried and utilities
            attached. Some utilities are unknown.
        * ./data/processed/new_filename-without-pl_examples.pl - contains n partially observed examples and their utility.
    :param filename: The name of the ProbLog file to create a dataset for.
    :param n: The number of samples to take, aka the number of examples in the resulting examples file.
    :param new_filename: The filename to use for the new files. When none, the original filename appended with
    _{drop_prob}_{prob_of_unknown}_{n}_{nb_utility_nodes}_{samples_per_utility_node}.pl is used.
    :param decisions: Whether to decisions to the dataset.
    :param learning: Whether to also create a file with unknown utilities and observations.
    :param drop_prob: The probability that a term is dropped in an example.
    :param prob_of_unknown: The probability that a utility becomes unknown.
    :param nb_utility_nodes: The amount of utility nodes to introduce to the model.
    :param samples_per_utility_node: The amount of rules to add for each introduced utility fact f: 'f :- sample'.
    :param verbose: Whether to print when a stage is finished.
    :type filename: str
    :type n: int
    :type new_filename: str
    :type decisions: bool
    :type learning: bool
    :type drop_prob: float
    :type prob_of_unknown: float
    :type nb_utility_nodes: int
    :type samples_per_utility_node: int
    :type verbose: bool
    """
    raw_model_filename = "./data/raw/" + filename
    if new_filename is None:
        new_filename = filename.replace('.pl', '') + "_{}_{}_{}_{}_{}.pl".format(drop_prob, prob_of_unknown, n,
                                                                                 nb_utility_nodes,
                                                                                 samples_per_utility_node)
    processed_real_model_filename = "./data/processed/" + new_filename
    processed_input_model_filename = f"./data/processed/{new_filename.replace('.pl', '')}_input.pl"
    examples_filename = f"./data/processed/{new_filename.replace('.pl', '')}_examples.pl"

    # Add queries to file
    db = _add_queries(raw_model_filename)
    # Create real model - add utilities
    db_utilities = utils.add_utility_terms_to_db(db, nb_utility_nodes=nb_utility_nodes,
                                                 samples_per_utility_node=samples_per_utility_node)
    if verbose:
        print("Utilities added in: %s" % processed_real_model_filename)
    if decisions:
        db_utilities, nb_of_decisions = utils.add_decisions_to_db(db_utilities)
        if verbose:
            print("%s decisions added in: %s" % (nb_of_decisions, processed_real_model_filename))
    utils.save_db(db_utilities, processed_real_model_filename)

    if learning:
        # Create input model - add unknown utilities
        db_unknown_utilities = db.extend()
        utils.add_unknown_utilities_to_db(db_utilities, db_unknown_utilities, prob_of_unknown=prob_of_unknown)
        utils.save_db(db_unknown_utilities, processed_input_model_filename)
        if verbose:
            print("Unknown utilities added in: %s" % processed_input_model_filename)
        # Create observation file
        examples = utils.create_observations(processed_real_model_filename, n=n)
        examples = utils.drop_observations(examples, drop_prob=drop_prob)
        utils.save_examples(examples, examples_filename)
        if verbose:
            print("Examples constructed: %s" % examples_filename)
        return processed_real_model_filename, processed_input_model_filename, examples_filename
    else:
        return processed_real_model_filename


def _add_queries(raw_model_filename):
    """
    Get a database from raw_model_filename and add 'query(x).' for each term x.
    :param raw_model_filename: The ProbLog file to create a database for.
    :return: The resulting database.
    :rtype: ClauseDB
    """
    program = PrologFile(raw_model_filename)
    engine = DefaultEngine(label_all=True, keep_order=True)
    db = engine.prepare(program)
    utils.query_all_terms(db)
    return db


def _argparser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('inputfile', help="The name of the file located in ./data/raw/inputfile.pl")
    parser.add_argument('--drop', '-d', type=float, default=0.25,
                        help='The probability that a term is dropped frm the observations.')
    parser.add_argument('--unknown_prob', '-u', type=float, default=0.5,
                        help='The probability with which a utility is made unknown.')
    parser.add_argument('--task_type', '-t', type=str, default='',
                        help='d or d2 to create decision models, otherwise learning are models are created.')
    parser.add_argument('--nb_of_examples', '-e', type=int, default=150,
                        help='The number of examples to create. Only relevant when task type is not d or d2.')
    parser.add_argument('--nb_util_nodes', '-n', type=int, default=5,
                        help='The number of utility nodes to add. Only relevant when task type is d2.')
    parser.add_argument('--nb_rules', '-r', type=int, default=5,
                        help='The number of utility nodes to add. Only relevant when task type is d2.')
    parser.add_argument('--seed', '-s', type=int, default=5,
                        help='The seed to use by the random module.')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Write output to given file (default: write to stdout)')
    parser.add_argument('-v', '--verbose', action='count', help='Increase verbosity')
    return parser

if __name__ == '__main__':
    main(sys.argv)
