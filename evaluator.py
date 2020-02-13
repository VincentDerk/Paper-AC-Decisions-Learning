"""
By Vincent Derkinderen (DTAI lab KU Leuven, 2019)

A script to evaluate a learned ProbLog model by calculating the regret compared to the correct model.

Input
    Learned models to evaluate: ./data/results/{drop_prob}_0.5_{nb_of_examples}/{file}_result.pl
    The correct file is assumed to be in ./data/processed/{drop_prob}_0.5_{nb_of_examples}/{file}.pl

Output
    Logs: ./data/results/{file}_print_{used_seed}_regret.txt
    Results: ./data/results/{file}_results_{used_seed}_regret.p storing
    [correct_decisions, best_eu, found_decisions, best_learned_eu, best_found_eu]
        * correct_decisions and best_eu are the best decisions and expected utility achievable in the correct model.
        * found_decisions are the best possible decisions according to the learned model.
        * best_learned_eu is the eu we get when making found_decisions and if the learned model was the correct model.
        * best_found_eu is the actual eu we get when making found_decisions in the correct model.
"""
import pickle
import sys
import os
import random

from problog.program import PrologString, PrologFile
from problog.logic import Term, Clause, AnnotatedDisjunction
from problog.engine import ClauseDB, DefaultEngine

from gradientmeu import GradientMEU
import maxeu

from script_learning import Printer
from ulearner import PrinterDefault


def main(argv):
    """
    Evaluate each learned ProbLog model based on the regret. The regret is the difference between the maximum eu and
    the eu obtained by making decisions based on the learned utilities instead of the actual decisions.
    Since this metric also depends on the decisions, each learned model is evaluated multiple times (3) for different
    models (differently introduced decisions).

    Input
    All the ProbLog models to evaluate are obtained from ./data/results/{drop_prob}_0.5_{nb_of_examples}/{file}_mse.p
    where {file} contains {name} and str({left_out}). Where the learned file is assumed to be {file}_result.pl and the
    correct file is assumed to be in ./data/processed/{drop_prob}_0.5_{nb_of_examples}/{file}.pl

    Output
    Log prints are written to ./data/results/{file}_print_{used_seed}_regret.txt
    The resulting list, [correct_decisions, best_eu, found_decisions, best_learned_eu, best_found_eu], is written to
    ./data/results/{file}_results_{used_seed}_regret.p Where
        * correct_decisions and best_eu are the best decisions and expected utility achievable in the correct model.
        * found_decisions are the best possible decisions according to the learned model.
        * best_learned_eu is the eu we get when making found_decisions and if the learned model was the correct model.
        * best_found_eu is the actual eu we get when making found_decisions in the correct model.
    """
    args = _argparser().parse_args(argv[1:])
    seed = args.seed
    random.seed(a=seed)
    name = args.name
    drop_prob = args.drop
    nb_of_example = args.nb_of_examples
    left_out = args.left_out
    name_extension = "{}_0.5_{}".format(drop_prob, nb_of_example)
    folder = name_extension + '/'
    filepath = "./data/results/" + folder
    nb_of_evaluations = args.nb_of_evals

    # Create task list
    task_list = list()
    for file in os.listdir(filepath):
        if file.endswith("_mse.p") and name in file and str(left_out) in file:
            learned_model_filename = folder + file.replace('_mse.p', '') + "_result.pl"
            correct_model_filename = folder + file.replace('_mse.p', '.pl')
            task_list.append((learned_model_filename, correct_model_filename))

    # Create random seeds
    random_seeds = list()
    for i in range(0, len(task_list)):
        one_task_list = [random.randint(0, 2147000000) for j in range(0, nb_of_evaluations)]
        random_seeds.append(one_task_list)

    # Perform tasks
    for (learned_model_filename, correct_model_filename), seed_list in zip(task_list, random_seeds):
        for new_seed in seed_list:
            random.seed(a=new_seed)
            print_filename = "./data/results/" + learned_model_filename.replace('_result.pl', '_print_{}_regret.txt'.
                                                                                format(new_seed))
            with open(print_filename, 'w') as f:
                printer = Printer(f)
                correct_decisions, best_eu, found_decisions, best_learned_eu, best_found_eu = \
                    use_exact(learned_model_filename, correct_model_filename, printer)
                results = [correct_decisions, best_eu, found_decisions, best_learned_eu, best_found_eu]
                results_filename = "./data/results/" + learned_model_filename.replace('_result.pl',
                                                                                      '_results_{}_regret.p'.
                                                                                      format(new_seed))
            with open(results_filename, 'wb') as f:
                pickle.dump(results, f)


def temp(args):
    a = 2
    random.seed(a=a)
    print("Using seed %s" % a)
    filename = args[1]
    correct_filename = args[2]
    use_exact(filename, correct_filename)


def use_exact(filename, correct_filename, printer):
    """
    Use the exact maximum expected utility tool to evaluate the regret of the given ProbLog model (filename). The
    regret is the difference between the maximum eu and the eu obtained by making decisions based on the learned
    utilities instead of the actual decisions. This metric also depends on the decisions so decisions are introduced to
    the learned model by using add_decisions_to_databases(..). Next, the best decision and resulting eu
    (in both correct and learned model) is found using the exact meu solver.

    :param filename: The filepath of the learned model, such that we evaluate ./data/results/filename
    :param correct_filename: The filepath of the correct model, to compare with ./data/processed/correct_filename
    :param printer: The printer to which logging messages are written. If None, the default output console is used.
    :return: [correct_decisions, best_eu, found_decisions, best_learned_eu, best_found_eu] where
        * correct_decisions and best_eu are the best decisions and expected utility achievable in the correct model.
        * found_decisions are the best possible decisions according to the learned model.
        * best_learned_eu is the eu we get when making found_decisions and if the learned model was the correct model.
        * best_found_eu is the actual eu we get when making found_decisions in the correct model.
    :rtype: dict[Term, int], float, dict[Term, int], float, float
    """
    if printer is None:
        printer = PrinterDefault
    resultfile = "./data/results/" + filename
    correctfile = "./data/processed/" + correct_filename

    # Add decision to both
    engine = DefaultEngine(label_all=True, keep_order=True)
    db_correct = engine.prepare(PrologFile(correctfile))
    db_result = engine.prepare(PrologFile(resultfile))
    db_result, db_correct, nb_of_decisions = add_decisions_to_databases(db_result, db_correct)
    printer.print("Added %s decisions" % nb_of_decisions)

    # Find max EU of correct
    correct_decisions, best_eu, _, _, _ = maxeu.get_best_decision(db_correct)

    # Find best decision of result
    found_decisions, best_learned_eu, _, _, _ = maxeu.get_best_decision(db_result)

    # Find EU of best decision of result, in correct
    maximiser_correct = GradientMEU(db_correct)
    maximiser_correct.prepare()
    maximiser_correct.set_current_decision_weights(found_decisions)
    best_found_eu = maximiser_correct.get_eu()

    # Report
    printer.print("Correct decisions: %s" % correct_decisions)
    printer.print("Best EU: %s" % best_eu)
    printer.print("Found decisions: %s" % found_decisions)
    printer.print("Best learned EU: %s" % best_learned_eu)
    printer.print("Best found EU: %s" % best_found_eu)
    if best_eu != 0.0:
        printer.print("Regret: %s" % ((best_eu - best_found_eu) / best_eu))
    else:
        printer.print("Absolute regret: %s" % (best_eu - best_found_eu))

    return correct_decisions, best_eu, found_decisions, best_learned_eu, best_found_eu


def use_gradient(filename, correct_filename, printer):
    """
    Use the gradient maximum expected utility tool to evaluate the regret of the given ProbLog model (filename). The
    regret is the difference between the maximum eu and the eu obtained by making decisions based on the learned
    utilities instead of the actual decisions. This metric also depends on the decisions so decisions are introduced to
    the learned model by using add_decisions_to_databases(..). Next, the best decision and resulting eu
    (in both correct and learned model) is found using the gradient meu solver.

    :param filename: The filepath of the learned model, such that we evaluate ./data/results/filename
    :param correct_filename: The filepath of the correct model, to compare with ./data/processed/correct_filename
    :param printer: The printer to which logging messages are written. If None, the default output console is used.
    :return: [correct_decisions, best_eu, found_decisions, best_learned_eu, best_found_eu] where
        * correct_decisions and best_eu are the best decisions and expected utility achievable in the correct model.
        * found_decisions are the best possible decisions according to the learned model.
        * best_learned_eu is the eu we get when making found_decisions and if the learned model was the correct model.
        * best_found_eu is the actual eu we get when making found_decisions in the correct model.
    :rtype: dict[Term, int], float, dict[Term, int], float, float
    """
    resultfile = "./data/results/" + filename
    correctfile = "./data/processed/" + correct_filename

    # Add decision to both
    engine = DefaultEngine(label_all=True, keep_order=True)
    db_correct = engine.prepare(PrologFile(correctfile))
    db_result = engine.prepare(PrologFile(resultfile))
    db_result, db_correct, nb_of_decisions = add_decisions_to_databases(db_result, db_correct)
    print("Added %s decisions" % nb_of_decisions)

    # Find max EU of correct
    maximiser_correct = GradientMEU(db_correct)
    correct_decisions, best_eu = maximiser_correct.maximise_adaptive_w_restarts(max_random_restarts=4)

    # Find best decision of result
    maximiser_found = GradientMEU(db_result)
    found_decisions, best_learned_eu = maximiser_found.maximise_adaptive_w_restarts(max_random_restarts=4)

    # Find EU of best decision of result, in correct
    maximiser_correct.set_current_decision_weights(found_decisions)
    best_found_eu = maximiser_correct.get_eu()

    # Report
    printer.print("Correct decisions: %s" % correct_decisions)
    printer.print("Best EU: %s" % best_eu)
    printer.print("Found decisions: %s" % found_decisions)
    printer.print("Best learned EU: %s" % best_learned_eu)
    printer.print("Best found EU: %s" % best_found_eu)
    printer.print("Regret: %s" % (best_eu - best_found_eu))


def add_decisions_to_databases(db1, db2, decision_prob=0.5):
    """
    Add decisions to db1 and db2 by going over the rules in db1 and for each AD with 2 possible values and for which
    the body is true, a decision is introduced that makes the first value true and the second false. Any probabilistic
    fact is also turned into a decision. When all of this results in less than 4 decisions, For each AD not yet covered,
    one of its values (randomly decided) is made true by a new decision with probability decision_prob. Any decision and
    rules are added to an extension of both db1 and db2.

    :param db1: The database to start from.
    :type db1: ClauseDB
    :param db2: The additional database to add to.
    :type db2: ClauseDB
    :param decision_prob: The probability that an AD with more than 2 values introduces a decision when less than 4
    decisions were added.
    :type decision_prob: float
    :return: The two new databases and the number of decisions added to both databases
    :rtype: ClauseDB, ClauseDB, int
    """
    nb_of_decisions = 0
    remove_list = list()
    true_terms = set()
    true_terms_statement = dict()

    # Add decisions
    temp_db1 = db1.extend()
    temp_db2 = db2.extend()
    temp_db1_pl = temp_db1.to_prolog()
    temp_db2_pl = temp_db2.to_prolog()
    for term in db1:
        if isinstance(term, Clause) and str(term.args[1]) == 'true':
            true_terms.add(term.args[0])
            true_terms_statement[term.args[0]] = term
        elif isinstance(term, AnnotatedDisjunction) and term.args[1] in true_terms and len(term.args[0]) == 2:
            remove_list.append(str(term) + ".")
            remove_list.append(str(true_terms_statement[term.args[1]]) + ".")
            temp_db1_pl += "\n?::dec_{}.".format(nb_of_decisions)
            temp_db1_pl += "\n{} :- dec_{}.".format(str(term.args[0][0]), nb_of_decisions)
            temp_db1_pl += "\n{} :- \\+dec_{}.".format(str(term.args[0][1]), nb_of_decisions)
            temp_db2_pl += "\n?::dec_{}.".format(nb_of_decisions)
            temp_db2_pl += "\n{} :- dec_{}.".format(str(term.args[0][0]), nb_of_decisions)
            temp_db2_pl += "\n{} :- \\+dec_{}.".format(str(term.args[0][1]), nb_of_decisions)
            nb_of_decisions += 1
        elif not isinstance(term, Clause) and not isinstance(term, AnnotatedDisjunction) and term.functor != 'query' \
                and term.functor != 'utility' and term.functor != 'evidence':
            temp_db1_pl += "\n" + str(term.with_probability(Term('?'))) + "."
            temp_db2_pl += "\n" + str(term.with_probability(Term('?'))) + "."
            remove_list.append(str(term) + ".")
            nb_of_decisions += 1

    # invent more decisions if there are only few.
    if nb_of_decisions <= 3:
        for term in db1:
            if isinstance(term, AnnotatedDisjunction) and (not term.args[1] in true_terms) and random.random() <= decision_prob:
                temp_db1_pl += "\n?::dec_{}.".format(nb_of_decisions)
                temp_db2_pl += "\n?::dec_{}.".format(nb_of_decisions)
                rand_index = random.randint(0, len(term.args[0])-1)
                temp_db1_pl += "\n{} :- dec_{}.".format(str(term.args[0][rand_index]), nb_of_decisions)
                temp_db2_pl += "\n{} :- dec_{}.".format(str(term.args[0][rand_index]), nb_of_decisions)
                nb_of_decisions += 1

    # Remove old probabilistic lines.
    for rem_str in remove_list:
        temp_db1_pl = temp_db1_pl.replace(rem_str, "")
        temp_db2_pl = temp_db2_pl.replace(rem_str, "")

    engine = DefaultEngine(label_all=True, keep_order=True)
    program = PrologString(temp_db1_pl)
    db_new1 = engine.prepare(program)
    engine = DefaultEngine(label_all=True, keep_order=True)
    program = PrologString(temp_db2_pl)
    db_new2 = engine.prepare(program)

    return db_new1, db_new2, nb_of_decisions


def _argparser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('name', help="The name of each file that should be processed in "
                                     "./data/results/{drop_prob}_0.5_{nb_of_examples}/filename.")
    parser.add_argument('--drop', '-d', type=float, default=0.5,
                        help='The probability that a term is dropped from the observations.')
    parser.add_argument('--left_out', '-l', type=bool, default=False,
                        help='Whether to leave out a third of the data and use its signal to stop the process.')
    parser.add_argument('--seed', '-s', type=int, default=5,
                        help='The seed to use by the random module.')
    parser.add_argument('--nb_of_examples', '-n', type=int, default=150,
                        help='The number of partial interpretations that make up the dataset of examples.')
    parser.add_argument('--nb_of_evals', '-e', type=int, default=3,
                        help='The amount of times each network should be evaluated (different decisions).')
    return parser


if __name__ == '__main__':
    main(sys.argv)
