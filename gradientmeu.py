import random
import math
import time
from collections import namedtuple

from problog.ddnnf_formula import DDNNF
from problog.engine import DefaultEngine
from problog.evaluator import Evaluator, Semiring
from problog.program import PrologFile
from problog.logic import Term, Constant
from problog.formula import LogicFormula
from problog import get_evaluatable

from ulearner import PrinterDefault

EU_TERM_NAME = 's'
printer = PrinterDefault()

pn_weight = namedtuple('pos_neg_weight', 'p_weight, n_weight')


def get_maximisation(model_filename, max_epoch=3, learning_rate=0.1):
    """
    Get a maximisation instance for the given model and set the max epoch and learning rate.
    :param model_filename: The filepath to the model.
    :param max_epoch: The maximum amount of epochs, gradient ascent parameter.
    :param learning_rate: The initial learning rate, gradient ascent parameter.
    :return: An instance of Gradient_MEU which can be used to find decisions that maximise the expected utility.
    :rtype Gradient_MEU
    """
    program = PrologFile(model_filename)
    maximisation = GradientMEU(program)
    maximisation.max_epoch = max_epoch
    maximisation.learning_rate = learning_rate
    return maximisation


class GradientMEU:

    def __init__(self, db, max_epoch=100, convergence_threshold=1, learning_rate=0.1):
        """
        Initialise the utility learner

        :param db: The ProbLog database to use
        """
        assert db is not None
        self.db = db
        self.max_epoch = max_epoch
        self.convergence_threshold = convergence_threshold
        self.learning_rate = learning_rate

        self._semiring_eu = SemiringEU()
        self._kc = None
        self._weights = None
        self._decision_weights = None
        self._key_to_decision_index = None
        self.term_to_key = dict()
        self.log = GradMeuLog()
        self.compile_time = -1
        self.runtime = -1

    @staticmethod
    def get_maximiser(program):
        """ Get a maximiser for the given program """
        engine = DefaultEngine(label_all=True, keep_order=True)
        db = engine.prepare(program)
        return GradientMEU(db)

    def prepare(self):
        """
        Prepare the process by compiling a circuit that represents the expected utility, and by extracting the weights.
        """
        # Prepare LF
        engine = DefaultEngine(label_all=True, keep_order=True)
        utilities = dict(engine.query(self.db, Term('utility', None, None)))
        pl_queries = [q[0] for q in engine.query(self.db, Term('query', None))]
        queries = set(pl_queries).union(set(utilities.keys()))

        # Ground as utilities
        lf = engine.ground_all(self.db, queries=queries)  # type: LogicFormula
        #print("lf")
        #print(lf)
        #print("")

        # Decisions
        decisions = []
        decision_term = Term("?")
        for _, n, type in lf:
            if type == 'atom' and n.probability == decision_term:  # TODO remove type == 'atom' ??
                decisions.append(n.name)

        # Knowledge compilation
        kc_class = get_evaluatable(name="sddx")  # TODO: let user choose
        printer.print("Starting compilation")
        starttime = time.time()
        self._kc = kc_class.create_from(lf)  # type: DDNNF
        self.compile_time = time.time() - starttime
        printer.print("Compilation took %s seconds." % self.compile_time)

        for decision in decisions:
            self.term_to_key[decision] = self._kc.get_node_by_name(decision)

        # Fix weights
        self._weights, self._decision_weights, self._key_to_decision_index = \
            self._get_fixed_weights(self._kc, utilities, decisions)
        printer.print("\nFixed weights: %s" % self._weights)
        printer.print("decision_weights: %s" % self._decision_weights)
        printer.print("key_to_decision_index: %s" % self._key_to_decision_index)

    def maximise(self):
        """
        Get the decisions that lead to the maximum expected utility by performing a gradient ascent process which
        uses the circuit to compute the expected utility of a set of decisions. These decisions are represented as
        probabilistic parameters such that maximising them will lead to decisions with the highest expected utility.
        :return: The found decisions and the expected utility
        :rtype: dict[Term, int], float
        """
        if self._kc is None:
            self.prepare()

        evaluator_eu = self._kc.get_evaluator(semiring=self._semiring_eu, weights=self._weights)  # type: Evaluator

        epoch = 0
        while epoch < self.max_epoch:  # TODO and converging difference < ... OR MSE < ...?
            epoch += 1

            # Reset gradients
            dec_gradients = {key: 0 for key in self._key_to_decision_index}
            evaluator_eu.propagate()

            # Calculate gradients
            for key, index in self._key_to_decision_index.items():
                eu_d = evaluator_eu.evaluate(key).args[1].compute_value()
                eu_nd = evaluator_eu.evaluate(-key).args[1].compute_value()
                sigma_d = 1 / (1 + math.e**-self._decision_weights[index])
                dec_gradients[key] = (1 - sigma_d) * eu_d + (sigma_d - 1) * eu_nd

            #printer.print("\nGradients: %s" % dec_gradients)
            #printer.print("key_to_decision_index: %s" % self._key_to_decision_index)
            #self.log.gradients.append(dec_gradients)

            # Move decisions in direction of gradients
            for key, index in self._key_to_decision_index.items():
                self._decision_weights[index] += self.learning_rate * dec_gradients[key]
                if self._decision_weights[index] <= -7:  # p <= 0.0009110511944006456
                    self._decision_weights[index] = -100
                elif self._decision_weights[index] >= 7:  # p >= 0.9990889488055994
                    self._decision_weights[index] = 100

            printer.print("Updated to decisions: %s" % self._decision_weights)
            printer.print("Decisions: %s" % self.get_current_decision_weights())
            evaluator_eu.propagate()
            expected_utility = evaluator_eu.evaluate(0)  # .args[1].compute_value()
            printer.print("Expected utility: %s" % expected_utility)

        decisions = self.get_current_decisions()
        self.set_current_decision_weights(decisions=decisions)
        evaluator_eu.propagate()
        expected_utility = evaluator_eu.evaluate(0).args[1].compute_value()
        printer.print("Final decisions: %s" % decisions)
        printer.print("Final expected utility: %s" % expected_utility)
        return self.get_current_decisions(), expected_utility

    def maximise_adaptive_w_restarts(self, increase_rate=1.1, decrease_rate=0.8, max_random_restarts=4):
        """
        Get the decisions that lead to the maximum expected utility by performing a gradient ascent process which
        uses the circuit to compute the expected utility of a set of decisions. These decisions are represented as
        probabilistic parameters such that maximising them will lead to decisions with the highest expected utility.
        This gradient ascent implementation adapts the learning rate over time in attempt to converge faster.
        When an improvement is found, the rate is multiplied with increase_rate, otherwise with decrease_rate.
        The process is restarted max_random_restarts times.
        :param increase_rate: The rate with which to multiply the learning rate when a solution improved.
        :param decrease_rate: The rate with which to multiply the learning rate when a solution got worse.
        :param max_random_restarts: The maximum amount of restarts to perform.
        :return: The best found decisions, the expected utility and the size of the used algebraic circuit (SDD).
        :rtype: dict[Term, int], float, int
        """
        starttime = time.time()
        max_decisions, max_eu = self.maximise_adaptive(increase_rate, decrease_rate)
        printer.print("-------------------------------\n")
        for i in range(1, max_random_restarts):
            self.set_random_decisions()
            decisions, eu = self.maximise_adaptive(increase_rate, decrease_rate)
            if eu > max_eu:
                max_eu = eu
                max_decisions = decisions
            printer.print("-------------------------------\n")
        self.runtime = time.time() - starttime
        sdd_size = self._kc.get_manager().get_manager().size()
        return max_decisions, max_eu, sdd_size,

    def maximise_adaptive(self, increase_rate=1.1, decrease_rate=0.8):
        """
        Get the decisions that lead to the maximum expected utility by performing a gradient ascent process which
        uses the circuit to compute the expected utility of a set of decisions. These decisions are represented as
        probabilistic parameters such that maximising them will lead to decisions with the highest expected utility.
        This gradient ascent implementation adapts the learning rate over time in attempt to converge faster.
        When an improvement is found, the rate is multiplied with increase_rate, otherwise with decrease_rate.
        :param increase_rate: The rate with which to multiply the learning rate when a solution improved.
        :param decrease_rate: The rate with which to multiply the learning rate when a solution got worse.
        :return: The best found decisions, the expected utility and the size of the used algebraic circuit (SDD).
        :rtype: dict[Term, int], float, int
        """
        if self._kc is None:
            self.prepare()

        evaluator_eu = self._kc.get_evaluator(semiring=self._semiring_eu, weights=self._weights)  # type: Evaluator
        learning_rate = self.learning_rate

        # Starting EU
        evaluator_eu.propagate()
        prev_eu = evaluator_eu.evaluate(0).args[1].compute_value()
        print("\nStarting with expected utility: %s" % prev_eu)
        print("Starting with weights: %s" % self.get_current_decision_weights())

        epoch = 0
        converged = False
        while epoch < self.max_epoch and learning_rate > 10e-3 and not converged:
            epoch += 1

            # Reset gradients
            dec_gradients = {key: 0 for key in self._key_to_decision_index}
            evaluator_eu.propagate()

            # Calculate gradients
            for key, index in self._key_to_decision_index.items():
                eu_d = evaluator_eu.evaluate(key).args[1].compute_value()
                eu_nd = evaluator_eu.evaluate(-key).args[1].compute_value()
                sigma_d = 1 / (1 + math.e**-self._decision_weights[index])
                dec_gradients[key] = (1 - sigma_d) * eu_d + (sigma_d - 1) * eu_nd
            printer.print("\nGradients: %s" % dec_gradients)

            # Move decisions in direction of gradients
            diff = 0
            for key, index in self._key_to_decision_index.items():
                old = self._decision_weights[index]
                self._decision_weights[index] += learning_rate * dec_gradients[key]
                if self._decision_weights[index] <= -7:  # p <= 0.0009110511944006456
                    self._decision_weights[index] = -100
                elif self._decision_weights[index] >= 7:  # p >= 0.9990889488055994
                    self._decision_weights[index] = 100
                diff += abs(self._decision_weights[index] - old)
            printer.print("Updated to decisions: %s" % self._decision_weights)
            printer.print("Decisions: %s" % self.get_current_decision_weights())

            if diff == 0:
                printer.print("Result converged.")
                converged = True
            else:
                evaluator_eu.propagate()
                eu = evaluator_eu.evaluate(0).args[1].compute_value()
                if eu < prev_eu:
                    # Revert change
                    for key, index in self._key_to_decision_index.items():
                        self._decision_weights[index] -= learning_rate * dec_gradients[key]

                    # learning rate lower
                    learning_rate *= decrease_rate
                    printer.print("Worse eu %s, decreasing learning rate to %s" % (eu, learning_rate))
                    epoch -= 1
                else:
                    learning_rate *= increase_rate
                    prev_eu = eu
                    self.log.eu_per_epoch.append(eu)
                    printer.print("After epoch %s, expected utility: %s and learning_rate %s" % (epoch, eu, learning_rate))

        decisions = self.get_current_decisions()
        self.set_current_decision_weights(decisions=decisions)
        evaluator_eu.propagate()
        eu = evaluator_eu.evaluate(0).args[1].compute_value()
        printer.print("Final decisions: %s" % decisions)
        printer.print("Final expected utility: %s" % eu)
        return decisions, eu

    def set_current_decision_weights(self, decisions):
        """
        Set the current decision weights (probability).
        :param decisions: For each term, the decision weight (probability) to set. Only terms which have unknown
        decisions and were prepared earlier are set, the rest is ignored.
        :type decisions: dict[Term, float]
        """
        for term, prob in decisions.items():
            key = self.term_to_key.get(term)
            if key is not None:
                index = self._key_to_decision_index.get(key)
                if index is not None:
                    if prob == 0:  # weight = z
                        self._decision_weights[index] = -230  # z=-230 == p=1e-100
                    elif prob == 1:
                        self._decision_weights[index] = 34  # z=34 == p=0.9999999999999982
                    else:
                        self._decision_weights[index] = -math.log(1/prob - 1)

    def get_current_decision_weights(self):
        """
        Get the currently set decision weights (probability).
        :return: The decision weights set for each term. The returned dictionary can safely be modified.
        :rtype: dict[Term, float]
        """
        result_dict = dict()
        for term, key in self.term_to_key.items():
            index = self._key_to_decision_index.get(key)
            if index is not None:
                result_dict[term] = 1 / (1 + math.e**-self._decision_weights[index])
        return result_dict

    def get_eu(self):
        """
        Get the expected utility for the currently set decision weights
        Precondition: self.prepare() must have been executed already.
        :return: The expected utility
        :rtype: float
        """
        evaluator_eu = self._kc.get_evaluator(semiring=self._semiring_eu, weights=self._weights)  # type: Evaluator
        evaluator_eu.propagate()
        return evaluator_eu.evaluate(0).args[1].compute_value()

    def get_current_decisions(self):
        """
        Get the currently set decisions (0 or 1). This differs from get_current_decision_weights in that the probability
        is rounded to the nearest int, 0 or 1.
        :return: A dictionary with decision Terms and for each term, 1 if the decision should be taken and 0 otherwise.
         The returned dictionary can safely be modified.
        :rtype: dict[Term, int]
        """
        result_dict = dict()
        for term, key in self.term_to_key.items():
            index = self._key_to_decision_index.get(key)
            if index is not None:
                p = 1 / (1 + math.e**-self._decision_weights[index])
                result_dict[term] = 1 if p > 0.5 else 0
        return result_dict

    def set_random_decisions(self):
        """
        Set all the unknown decisions to a random value between 0 and 1.
        """
        for index in range(1, len(self._decision_weights)):
            self._decision_weights[index] = random.random()*3 - 1.5  # z=[-1.5,1.5] == p=[0.18,0.81]

    def _get_fixed_weights(self, kc, utilities, decisions):
        """
        Get the weights present in kc, adjusted with the weights provided in utilities.
        A weight for the 0 node is used to keep track of the costs for the utility variables which are always true.

        An unknown utility is represented as an LfiTerm storing an index and reference to a list of values. During
        evaluation, the value at the index in the list and at any time, its value is determined by its index and list.

        :param kc: The BaseFormula of which to retrieve existing weights.
        :type kc: problog.formula.BaseFormula
        :param utilities: The utility variables to adjust the weight of. A dict of type {Term : external_weight} where
        external weights are those given to the semiring to get the internal value.
        :type utilities: dict[Term, Any]
        :return:
            1) The weights of kc adjusted with the weights of utilities (dict of type {name : external_weight}) and
            decisions. When both a positive and negative weight are specified, the pn_weight namedtuple
            is used.
            2) decision_weights - A list of decisions, one for each unknown decision term. The LfiTerms store a
            reference to this list and retrieve their value using their index. The first element is a dummy.
            3) key_to_decision_index - A dictionary mapping each node to the index in the decision_weights list.
        :rtype: Tuple[dict[Term, (pn_weight | Any)], list[float], dict[int, int]]
        """
        current_weights = dict(kc.get_weights())
        new_weights = dict()
        decision_weights = list()  # Stores init values. ID -> init weight
        decision_weights.append(-1)  # Sentinel because 0 = -0

        key_to_decision_index = dict()  # node key : index of value in decisions_weights

        ZERO_CST = Constant(0)
        ONE_CST = Constant(1.0)

        current_weights[0] = pn_weight(eu_term(ONE_CST, ZERO_CST), eu_term(ONE_CST, ZERO_CST))

        # Prepare all but the True weights to eu_term(p, cst) with p or cst potentially unknown lfi_term(lfi_id)
        for key, weight in current_weights.items():
            if isinstance(weight, Constant):
                prob = weight.compute_value()
                p_weight = eu_term(weight, ZERO_CST)
                n_weight = eu_term(Constant(1 - prob), ZERO_CST)
                new_weights[abs(key)] = pn_weight(p_weight, n_weight) if key >= 0 else pn_weight(n_weight, p_weight)

            elif isinstance(weight, Term) and weight.functor == '?':  # t(_):
                z_init = 0  # p = 0.5 <-> z = 0
                decision_weights.append(z_init)
                lfi_id = len(decision_weights) - 1
                p_weight = eu_term(prob_dec_term(decision_weights, lfi_id), ZERO_CST)
                n_weight = eu_term(prob_dec_term(decision_weights, -lfi_id), ZERO_CST)
                if key >= 0:
                    key_to_decision_index[key] = lfi_id
                else:
                    key_to_decision_index[-key] = -lfi_id
                new_weights[abs(key)] = pn_weight(p_weight, n_weight)
            else:
                new_weights[abs(key)] = weight
        current_weights = new_weights
        # post-condition: Every weight is pn_weight or True

        # term to key
        util_term_to_key = {util: self._kc.get_node_by_name(util) for util in utilities}

        # Start adding/replacing utilities
        for util, cost_cst in utilities.items():
            key = util_term_to_key[util]

            if key is None:
                continue  # TODO Possible?
            else:
                current_weight = current_weights.get(abs(key))

            if isinstance(cost_cst, Constant):  # Known utility
                cost = cost_cst.compute_value()
                if key >= 0:
                    if current_weight is True:
                        pos_weight = eu_term(ONE_CST, cost_cst)
                        neg_weight = eu_term(ONE_CST, ZERO_CST)
                        current_weights[key] = pn_weight(pos_weight, neg_weight)
                    elif isinstance(current_weight, pn_weight):
                        pos_weight, neg_weight = current_weight
                        pos_weight_utility = pos_weight.args[1]
                        pos_new_cost = Constant(pos_weight_utility.compute_value() + cost)
                        new_pos_weight = eu_term(pos_weight.args[0], pos_new_cost)
                        current_weights[key] = pn_weight(new_pos_weight, neg_weight)
                    else:
                        raise ValueError("Expected True or a value of type pn_weight. Found: %s of type %s" %
                                         (current_weight, type(current_weight)))
                else:  # = key < 0
                    if current_weight is True:
                        pos_weight = eu_term(ONE_CST, ZERO_CST)
                        neg_weight = eu_term(ONE_CST, cost_cst)
                        current_weights[abs(key)] = pn_weight(pos_weight, neg_weight)
                    elif isinstance(current_weight, pn_weight):
                        pos_weight, neg_weight = current_weight
                        neg_weight_utility = neg_weight.args[1]
                        neg_new_cost = Constant(neg_weight_utility.compute_value() + cost)
                        new_neg_weight = eu_term(neg_weight.args[0], neg_new_cost)
                        current_weights[abs(key)] = pn_weight(pos_weight, new_neg_weight)
                    else:
                        raise ValueError("Expected True or a value of type pn_weight. Found: %s of type %s" %
                                         (current_weight, type(current_weight)))

            else:
                raise ValueError("Expected a Constant Term as utility but received %s with type %s" %
                                 (cost_cst, type(cost_cst)))

        """
        # Convert current_weights to util_name -> weight
        result = dict()
        for name in utilities:
            key = kc.get_node_by_name(name)
            if key is not None:
                if key >= 0:
                    result[name] = current_weights[key]
                else:
                    value = current_weights[abs(key)]
                    result[name] = pn_weight(value.n_weight, value.p_weight)
        """
        return current_weights, decision_weights, key_to_decision_index


def eu_term(prob, cost):
    return Term(EU_TERM_NAME, prob, cost)


def prob_dec_term(decision_list, decision_index):
    return DynamicDecisionTerm(value_source=decision_list, value_index=decision_index)


class DynamicDecisionTerm(Term):
    """
        Class to represent decision Terms. The value of this term is dynamically computed using a source and index.
        Where the value in the source[abs(index)] is stored as the inverse sigmoid z such that prob = sigmoid(z)
    """

    def __init__(self, value_source, value_index, **kwdargs):
        """
        Instantiate this dynamic decision term with a source and index such that its value is dynamically computed from
        source[abs(index)].
        :param value_source:
        :param value_index: The key or index to retrieve the value from value_source as value_source[value_index]
        :param kwdargs: additional arguments for the superclass Term
        """
        Term.__init__(self, 't', **kwdargs)
        self.value_source = value_source
        self.value_index = value_index

    def compute_value(self, functions=None):
        z = self.value_source[abs(self.value_index)]
        if z >= 34:
            p = 1
        elif z <= -230:
            p = 0
        else:
            p = 1 / (1 + math.e**-z)

        if self.value_index > 0:
            return p
        else:
            return 1 - p

    def __repr__(self):
        self.repr = 't(%s, %s)' % (self.value_index, self.value_source)
        self.reprhash = hash(self.repr)
        return self.repr


class SemiringEU(Semiring):
    """
    The expected utility semiring. Each element is a tuple of probability and expected utility: (p, eu).
    """
    def one(self):
        return 1.0, 0.0

    def zero(self):
        return 0.0, 0.0

    def plus(self, a, b):
        return a[0] + b[0], a[1] + b[1]

    def times(self, a, b):
        return a[0] * b[0], a[0] * b[1] + b[0] * a[1]

    def negate(self, a):
        if isinstance(a, tuple):
            return 1 - a[0], 0
        else:
            return 1 - a, 0

    def value(self, a):
        if isinstance(a, Term) and a.functor == EU_TERM_NAME:
            p = a.args[0].compute_value()
            u = a.args[1].compute_value()
            return p, p * u
        else:
            return float(a), 0

    def result(self, a, formula=None):
        return eu_term(Constant(a[0]), Constant(a[1]))

    def normalize(self, a, z):
        p_a, eu_a = a
        p_z, eu_z = z
        # each world I has p(I) and eu(I) = p(I) * u(I).
        # Normalizing the probability of the world (p(I)/p(Z) results p(I) / p(Z) * u(I) = eu(I) / p(Z)
        # Since total result = Sum_I [p(I) * u(I)]
        if p_a == 0.0:
            return 0.0, 0.0
        return p_a / p_z, eu_a / p_z

    def pos_value(self, a, key=None):
        if isinstance(a, pn_weight):
            return self.value(a.p_weight)
        else:
            return self.value(a)

    def neg_value(self, a, key=None):
        """Extract the negative internal value for the given external value."""
        if isinstance(a, pn_weight):
            return self.value(a.n_weight)
        else:
            return self.negate(self.value(a))

    def is_dsp(self):
        return True

    def is_nsp(self):
        return True

    def in_domain(self, a):
        import numbers
        return 0.0 - 1e-6 <= a[0] <= 1.0 + 1e-6 and isinstance(a[1], numbers.Number)

    def ad_complement(self, ws, key=None):
        s = self.zero()
        for w in ws:
            s = self.plus(s, w)
        return self.negate(s)

    def true(self, key=None):
        """Handle weight for deterministically true."""
        return self.one(), self.zero()

    def false(self, key=None):
        """Handle weight for deterministically false."""
        return self.zero(), self.one()

    def to_evidence(self, pos_weight, neg_weight, sign):
        # Note: When eu = 0 because of p = 0 and now we set p = 1 then the eu can not be reconstructed and stays 0.
        if sign > 0:
            return pos_weight, (0.0, 0.0)  # positive weight rescaled to p=1
        else:
            return (0.0, 0.0), neg_weight  # negative weight rescaled to p=1

    def ad_negate(self, pos_weight, neg_weight):
        #p_p, p_eu = pos_weight
        n_p, n_eu = neg_weight
        if n_p == 0:
            return 1.0, n_eu
        else:
            return 1.0, n_eu / n_p


class GradMeuLog:
    """
    Used to store information on the gradient process.
    """
    def __init__(self):
        self.eu_per_epoch = list()
        self.gradients = list()

