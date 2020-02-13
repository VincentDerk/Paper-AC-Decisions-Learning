"""
By Vincent Derkinderen (DTAI lab KU Leuven, 2019)

Small example illustrating how to use the gradient maximisation process to obtain the best decisions and eu.
"""
import sys
import random

import gradientmeu


def main(args):
    seed = 5
    random.seed(a=seed)
    filename = 'survey_decision.pl'
    processed_real_model_filename = "./data/processed/" + filename
    grad_maximiser = gradientmeu.get_maximisation(processed_real_model_filename, learning_rate=1, max_epoch=50)
    grad_maximiser.prepare()
    decisions, eu = grad_maximiser.maximise_adaptive_w_restarts()
    print("\n")
    print("RESULTS")
    print("Decisions %s" % decisions)
    print("Expected utility %s" % eu)


if __name__ == '__main__':
    main(sys.argv)
