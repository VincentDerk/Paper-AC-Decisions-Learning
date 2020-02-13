from problog.program import PrologString, PrologFile, LogicProgram
from problog.logic import Term, Constant, Clause, AnnotatedDisjunction, Not
from problog.engine import ClauseDB, DefaultEngine
from problog.tasks.sample import sample

import random
import re


def create_observations(processed_model_filename, n=2):
    """
    Create n examples from processed_model_filename each observing all queried terms.
    :param processed_model_filename: The filename of the problog program to observe from.
    :type processed_model_filename: str
    :param n: The amount of examples to create/sample.
    :type n: int
    :return: n examples (interpretations) and their utility. Each example is a tuple of observations and their utility.
    The observations are represented as a list of tuples, each consisting of a queried Term and their truth-value in this
    example. The utility of an example is the sum of the utilities of each term in the example.
    :rtype: list[tuple[list[(Term, bool)], int]]
    """
    model = PrologFile(processed_model_filename)

    # Prepare dict Term to utility
    engine = DefaultEngine()
    db = engine.prepare(model)

    def convert(t):
        if isinstance(t, Not) or str(t.functor) == 'not' or str(t.functor) == '\+':
            return t.args[0], False
        else:
            return t, True
    term_to_utility = {convert(q[0]): q[1] for q in engine.query(db, Term('utility', None, None))}

    # Construct examples
    examples_list = list()  # type: list[tuple[list[(Term, bool)], int]]
    for example in sample(model, n=n, format='dict'):
        # Convert to list of observed terms: (Term, True/False)
        observations = list(example.items())

        # Calculate utility
        utility = 0
        for observation in observations:
            utility_obs = term_to_utility.get(observation)
            utility_obs = utility_obs.compute_value() if utility_obs is not None else 0
            utility += utility_obs

        # Store result
        examples_list.append((observations, utility))
    return examples_list


def get_term_to_utilities(filename):
    """
    Get a dictionary mapping each term to its utility.
    :param filename: The file (path) from which to extract the terms and utilities.
    :type filename: str
    :return: A mapping of term to utility.
    :rtype: dict[Term, float]
    """
    pl = PrologFile(filename)
    engine = DefaultEngine()
    terms_to_utilities = {q[0]: q[1].compute_value() for q in engine.query(pl, Term('utility', None, None))}
    return terms_to_utilities


def query_all_terms(db):
    """
    Change the given database to query all its terms.
    :param db: The database to extract the terms from and to add the query(terms) to.
    :type db: ClauseDB
    """
    term_set = get_terms(db)
    for term in term_set:
        db.add_fact(Term('query', term))


def add_utility_terms_to_db(db, nb_utility_nodes, samples_per_utility_node):
    """
    Add nb_of_utility new utility nodes, each with a positive and negative utility. The rules that make a utility node
    true are based on random samples from the model. Each utility node has samples_per_utility_node, not per se unique.
    :param db: The database to add to.
    :type db: ClauseDB
    :param nb_utility_nodes: The amount of utility facts to add.
    :type nb_utility_nodes: int
    :param samples_per_utility_node: The amount of rules to add per introduced utility fact. These rules are
    constructed by sampling the model.
    :type samples_per_utility_node: int
    :return: db extended with utility facts and rules to make those new utility facts true.
    :rtype: ClauseDB
    """
    db_new = db.extend()

    def observation_to_str(observation):
        not_str = "" if observation[1] else "\+"
        return "{}{}".format(not_str, str(observation[0]))

    for i in range(0, nb_utility_nodes):
        util_term = Term('util_node', Constant(i))

        # Add utility facts
        utility_pos = random.randint(-50, 50)
        utility_neg = random.randint(-50, 50)
        db_new.add_fact(Term('utility', util_term, Constant(utility_pos)))
        db_new.add_fact(Term('utility', Not('\\+', util_term), Constant(utility_neg)))

        # Add rules
        for example in sample(db, n=samples_per_utility_node, format='dict'):
            observations = list(example.items())
            pl_str = "{} :- {}".format(str(util_term), observation_to_str(observations[0]))
            for observation in observations[1:]:
                pl_str += ", {}".format(observation_to_str(observation))
            pl_str += "."

            for statement in PrologString(pl_str):
                db_new += statement
    return db_new


def add_utilities_to_db(db, next_random_utility, prob_of_utility_for_pos=0.8, prob_of_utility_for_neg=0.3):
    """
    Add utilities for the terms in db for which there is a query(term) fact. Utilities are added for both the positive
    and negative term with a given probability. The utility to assign is determined by next_random_utility, a function
    taking the Term and a boolean as argument.

    :param db: The database to add utilities to
    :type db: ClauseDB
    :param next_random_utility: A function which provides the next random utility to assign to a term. This function
    takes two arguments, a Term and a boolean. The Term is the term for which we want to assign a value. The boolean
    denotes whether it is a positive term.
    :type next_random_utility: function[Term,boolean]
    :param prob_of_utility_for_pos The probability that a term should have a utility.
    :type prob_of_utility_for_pos: float
    :param prob_of_utility_for_neg The probability that the negation of a term should have a utility.
    :type prob_of_utility_for_neg: float
    """
    engine = DefaultEngine()
    queries = [q[0] for q in engine.query(db, Term('query', None))]
    for query in queries:
        if random.random() <= prob_of_utility_for_pos:
            utility = next_random_utility(query, True)
            db.add_fact(Term("utility", query, Constant(utility)))
        if random.random() <= prob_of_utility_for_neg:
            utility = next_random_utility(query, False)
            db.add_fact(Term("utility", Not('\+', query), Constant(utility)))


def add_unknown_utilities_to_db(db_source, db_target, prob_of_unknown=0.3):
    """
    Add utilities and unknown utilities to the target database. For each utility term in the source database: with
    probability prob_of_unknown, the term has an unknown probability in the target database. With a probability of
    1-prob_of_unknown, the term has the same utility in the target database as in the source database.
    :param db_source: The source database
    :type db_source: ClauseDB
    :param db_target: The target database
    :type db_target: ClauseDB
    :param prob_of_unknown: Probability that a utility from the source db becomes an unknown utility in the target db.
    :type prob_of_unknown: float
    """
    engine = DefaultEngine()
    queries = [(q[0], q[1]) for q in engine.query(db_source, Term('utility', None, None))]
    for query in queries:
        if random.random() <= prob_of_unknown:
            db_target.add_fact(Term('utility', query[0], Term('t', -1)))
            #for statement in PrologString("utility({},t(_)).".format(query[0])):
            #    db_target += statement
        else:
            db_target.add_fact(Term('utility', query[0], query[1]))


def add_decisions_to_db(db, decision_prob=0.10):
    """
    Add decisions to a database by changing leafs into decisions. The resulting db is a new db based on the
    input db and the added decisions. If less than 4 decisions were added, we also add a decision for each AD with more
    than 2 values (with a probability of decision_prob).
    :param db: The database to start from.
    :type db: ClauseDB
    :param decision_prob: The probability that an AD with more than 2 values introduces a decision when less than 4
    decisions were added.
    :type decision_prob: float
    :return: The new database and the number of decisions added to that database
    :rtype: ClauseDB, int
    """
    nb_of_decisions = 0
    remove_list = list()
    true_terms = set()
    true_terms_statement = dict()

    # Add decisions
    temp_db = db.extend()
    temp_db_pl = temp_db.to_prolog()
    for term in db:
        if isinstance(term, Clause) and str(term.args[1]) == 'true':
            true_terms.add(term.args[0])
            true_terms_statement[term.args[0]] = term
        elif isinstance(term, AnnotatedDisjunction) and term.args[1] in true_terms and len(term.args[0]) == 2:
            remove_list.append(str(term) + ".")
            remove_list.append(str(true_terms_statement[term.args[1]]) + ".")
            temp_db_pl += "\n?::dec_{}.".format(nb_of_decisions)
            temp_db_pl += "\n{} :- dec_{}.".format(str(term.args[0][0]), nb_of_decisions)
            temp_db_pl += "\n{} :- \\+dec_{}.".format(str(term.args[0][1]), nb_of_decisions)
            nb_of_decisions += 1
        elif not isinstance(term, Clause) and not isinstance(term, AnnotatedDisjunction) and term.functor != 'query' \
                and term.functor != 'utility' and term.functor != 'evidence':
            temp_db_pl += "\n" + str(term.with_probability(Term('?'))) + "."
            remove_list.append(str(term) + ".")
            nb_of_decisions += 1

    # invent more decisions if there are only few.
    if nb_of_decisions <= 3:
        for term in db:
            if isinstance(term, AnnotatedDisjunction) and (not term.args[1] in true_terms) and random.random() <= decision_prob:
                temp_db_pl += "\n?::dec_{}.".format(nb_of_decisions)
                rand_index = random.randint(0, len(term.args[0])-1)
                temp_db_pl += "\n{} :- dec_{}.".format(str(term.args[0][rand_index]), nb_of_decisions)
                nb_of_decisions += 1

    # Remove old probabilistic lines.
    for rem_str in remove_list:
        temp_db_pl = temp_db_pl.replace(rem_str, "")

    program = PrologString(temp_db_pl)
    engine = DefaultEngine(label_all=True, keep_order=True)
    db_new = engine.prepare(program)

    return db_new, nb_of_decisions


def add_decisions_to_db_archived(db, decision_prob=0.10):
    """
    Add decisions to a database by changing leafs into decisions. The resulting db is a new db based on the
    input db and the added decisions. If less than 4 decisions were added, we also add a decision for each AD with more
    than 2 values (with a probability of decision_prob).
    :param db: The database to start from.
    :type db: ClauseDB
    :param decision_prob: The probability that an AD with more than 2 values introduces a decision when less than 4
    decisions were added.
    :type decision_prob: float
    :return: The new database and the number of decisions added to that database
    :rtype: ClauseDB, int
    """
    nb_of_decisions = 0
    remove_list = list()
    true_terms = set()
    true_terms_statement = dict()

    # Add decisions
    temp_db = db.extend()
    for term in db:
        if isinstance(term, Clause) and str(term.args[1]) == 'true':
            true_terms.add(term.args[0])
            true_terms_statement[term.args[0]] = term
        elif isinstance(term, AnnotatedDisjunction) and term.args[1] in true_terms and len(term.args[0]) == 2:
            remove_list.append(str(term) + ".")
            remove_list.append(str(true_terms_statement[term.args[1]]) + ".")
            new_pl_str = "?::dec_{}.\n".format(nb_of_decisions)
            new_pl_str += "{} :- dec_{}.\n".format(str(term.args[0][0]), nb_of_decisions)
            new_pl_str += "{} :- \\+dec_{}.".format(str(term.args[0][1].with_probability(None)), nb_of_decisions)
            for statement in PrologString(new_pl_str):
                temp_db += statement
            nb_of_decisions += 1
        elif not isinstance(term, Clause) and not isinstance(term, AnnotatedDisjunction) and term.functor != 'query' \
                and term.functor != 'utility' and term.functor != 'evidence':
            temp_db.add_fact(term.with_probability(Term('?')))
            remove_list.append(str(term) + ".")
            nb_of_decisions += 1

    # invent more decisions if there are only few.
    if nb_of_decisions <= 3:
        for term in db:
            if isinstance(term, AnnotatedDisjunction) and (not term.args[1] in true_terms) and random.random() <= decision_prob:
                new_pl_str = "?::dec_{}.\n".format(nb_of_decisions)
                rand_index = random.randint(0, len(term.args[0])-1)
                new_pl_str += "{} :- dec_{}.\n".format(str(term.args[0][rand_index]), nb_of_decisions)
                for statement in PrologString(new_pl_str):
                    temp_db += statement
                nb_of_decisions += 1

    # Remove old probabilistic lines.
    new_pl = temp_db.to_prolog()
    for rem_str in remove_list:
        new_pl = new_pl.replace(rem_str, "")

    program = PrologString(new_pl)
    engine = DefaultEngine(label_all=True, keep_order=True)
    db_new = engine.prepare(program)

    return db_new, nb_of_decisions


def get_terms(db):
    """
    Get all the terms in the db.
    :param db: The database to extract the terms from.
    :type db: ClauseDB
    :return: A set of terms in the database, using the following extraction rules:
        0.1::a -> returns a.
        0.1::a :- x. -> returns a.
        0.1::a ; 0.9::b :- x. -> returns a and b.
        a :- x. -> returns a.
        query(b). -> returns nothing.
        body(96,_) :- x,z. -> returns nothing.
    :rtype: set[Term], set[Term]
    """
    term_set = set()
    fact_term_set = set()
    for term in db:
        if isinstance(term, Clause):
            head, _ = term.args
            if not head.functor.startswith("body"):
                term_set.add(head.with_probability(p=None))
        elif isinstance(term, AnnotatedDisjunction):
            heads, _ = term.args
            for head in heads:
                term_set.add(head.with_probability(p=None))
        elif term.functor != 'query' and term.functor != 'utility' and term.functor != 'evidence':
            term_set.add(term.with_probability(p=None))
    return term_set


def drop_observations(examples, drop_prob=0.25):
    """
    Drop observations from each example in examples.
    :param examples: The examples, each element of this list is a tuple of 1) a list of observations (Term, truth value) and 2) the utility for that observation.
    :type examples: list[tuple[list[(Term, bool)], int]]
    :param drop_prob: The probability that an observed term is dropped.
    :type drop_prob: float
    :return: The same list of examples except with some observed Terms not present anymore.
    :rtype: list[tuple[list[(Term, bool)], int]]
    """
    def drop(observations, utility):
        remaining_observations = list()
        for observation in sorted(observations, key=str):
            if random.random() > drop_prob:
                remaining_observations.append(observation)
        return remaining_observations, utility
    return [drop(observations, utility) for observations, utility in examples]


def save_db_w_replaced_utilities(db, output_filename, utility_weights):
    """
    Write the given database to file but replace the utilities of some terms.
    More specifically, for each term:util in utility_weights, add a rule utility(term,util). and remove the rules
    utility(term,_). and utility(term,_) :- true.
    :param db: The database to save.
    :type db: ClauseDB
    :param output_filename:  The path of the file to write to.
    :type output_filename: str
    :param utility_weights: A dictionary containing all the terms for which to provide a utility.
    :type utility_weights: dict[Term, float]
    """
    db_extended = db.extend()
    replace_terms = set()
    for term, util in utility_weights.items():
        db_extended.add_fact(Term('utility', term, Constant(util)))
        replace_terms.add(term)

    engine = DefaultEngine()
    pl_str = db_extended.to_prolog()
    for q in engine.query(db_extended, Term('utility', None, None)):
        if q[0] in replace_terms and isinstance(q[1], Term) and (not isinstance(q[1], Constant) or q[1].compute_value() != utility_weights[q[0]]):
            if isinstance(q[1], Constant):
                pl_str.replace(str(Term('utility', q[0], q[1])) + '.', '')
                pl_str.replace(str(Term('utility', q[0], q[1])) + ' :- true.', '')
            else:
                term_str = str(q[0])
                if term_str[0:2] == "\\+":
                    rest = term_str[2:]
                    term_str1 = "\\\\+" + rest
                    term_str2 = "\\\\+(" + rest + ")"
                    term_str1 = term_str1.replace("+", "\\+").replace("(", "\\(").replace(")", "\\)")
                    term_str2 = term_str2.replace("+", "\\+").replace("(", "\\(").replace(")", "\\)")
                    pattern1_1 = r'utility\({},t\((X|V_)[0-9]*\)\)\.'.format(term_str1)
                    pattern1_2 = r'utility\({},t\((X|V_)[0-9]*\)\) :- true\.'.format(term_str1)
                    pattern2_1 = r'utility\({},t\((X|V_)[0-9]*\)\)\.'.format(term_str2)
                    pattern2_2 = r'utility\({},t\((X|V_)[0-9]*\)\) :- true\.'.format(term_str2)
                    pl_str = re.sub(pattern1_1, '', pl_str)
                    pl_str = re.sub(pattern1_2, '', pl_str)
                    pl_str = re.sub(pattern2_1, '', pl_str)
                    pl_str = re.sub(pattern2_2, '', pl_str)
                else:
                    term_str = term_str.replace("(", "\\(").replace(")", "\\)")
                    pattern = r'utility\({},t\((X|V_)[0-9]*\)\)\.'.format(term_str)
                    pattern2 = r'utility\({},t\((X|V_)[0-9]*\)\) :- true\.'.format(term_str)
                    pl_str = re.sub(pattern, '', pl_str)
                    pl_str = re.sub(pattern2, '', pl_str)
    with open(output_filename, 'w') as f:
        f.write(pl_str)


def save_db(db, output_filename):
    """
    Write the given database to file.
    :param db: The database to write to file using db.to_prolog().
    :type db: ClauseDB
    :param output_filename: The path of the file
    :type output_filename: str
    """
    with open(output_filename, 'w') as outputf:
        outputf.writelines(db.to_prolog())


def save_examples(examples, examples_filename):
    """
    Write the given examples to file.
    :param examples: The examples to write to file.
    :type examples: list[tuple[list[(Term, bool)], int]]
    :param examples_filename: The path of the file.
    :type examples_filename: str
    """
    with open(examples_filename, 'w') as outputf:
        for example, utility in examples:
            for observation, truth_value in example:
                outputf.write('evidence({},{}).\n'.format(observation, str(truth_value).lower()))
            outputf.write("utility({}).\n".format(utility))
            outputf.write("-----\n")
