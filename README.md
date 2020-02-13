# Paper-AC-Decisions-Learning

The project files for the paper 'Algebraic Circuits for Decision Theoretic Inference and Learning'. Submitted to ECAI2020.
The main features are 
* **maxeu.py** - Solves the maximum expected utility problem by constraining the ordering in the algebraic circuit (X-constrained SDDs).
* **gradientmeu.py** - Solves the maximum expected utility problem by utilising the algebraic circuit as function to be optimised. The circuit is a function which calculates the expected utility given a set of decisions parameters. These parameters are optimised via gradient ascent. To illustrate the power of algebraic circuits, the gradient is calculated using the circuit.
* **ulearner.py** - Learns a value for the unknown utility labels, using partially observed intepretations of which the total utility is observed.

More details on these approaches can be found in the paper.

## Experiment files

#### script_dataset.py
A script used to create a ProbLog dataset from Bayesian networks. The Bayesian networks were first compiled into ProbLog programs using ProbLog's conversion script (12/2019). The script adds utilities and decisions, creates the input model and the partially observed examples to learning from. 

#### script_maximisation.py
A script used to perform a maximisation experiment (constrained or unconstrained) on a created ProbLog BN dataset.
The dataset creation relies on script_dataset.py and performs a maximisation experiment using maxeu.py or gradientmeu.py

#### script_maximisation_report.py
Small code example that was used to interactively extract information from previous maximisation experiments.

#### script_learning.py
A script used to perform a learning experiment on a created ProbLog BN dataset.
The dataset creation relies on script_dataset.py and performs a learning experiment
using ulearner.py

#### script_test.py
Small code example that was used to interactively extract information from previous learning experiments.

#### script_plot.py
A script used to create a plot (MSE, MSE_Test, RME vs epoch) for each previously executed learning experiment 
in a specified folder.

#### script_msse_plot.py
A script to calculate and create a plot of the mean squared sampled error (MSSE) over each epoch of the learning process.

#### script_scatter_plot.py
A script to create scatter plots (regret vs drop_prob) of regret.p files in a specified folder. The regret files can be 
created using evaluator.py

#### evaluator.py
A script to calculate the regret of a learned ProbLog model compared to the correct model.

## Requirements

[ProbLog 2.1.0.39+](https://dtai.cs.kuleuven.be/problog/)

[PySDD 0.2.9+](https://github.com/wannesm/PySDD)

## Paper experiments

### Maximisation
To reproduce the results of the paper, run the following:
```
script_maximisation.py survey --decisions 1 --approach both --seed 5 --repeat 10 --max_epoch 80 --lr 1.0
script_maximisation.py survey --decisions 2 --approach both --seed 5 --repeat 10 --max_epoch 80 --lr 1.0
script_maximisation.py asia --decisions 1 --approach both --seed 5 --repeat 10 --max_epoch 80 --lr 1.0
script_maximisation.py asia --decisions 2 --approach both --seed 5 --repeat 10 --max_epoch 80 --lr 1.0
script_maximisation.py earthquake --decisions 1 --approach both --seed 5 --repeat 10 --max_epoch 80 --lr 1.0
script_maximisation.py earthquake --decisions 2 --approach both --seed 5 --repeat 10 --max_epoch 80 --lr 1.0
```
Several lr's were tried, the conclusion remains roughly the same.

Report
script_maximisation_report.py

### Learning
Perform experiments [asia, survey, earthquake] x [0.0, 0.1, ..., 0.9, 0.25, 0.75] x 5
```
script_learning.py survey --drop 0.0 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.1 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.2 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.25 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.3 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.4 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.5 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.6 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.7 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.75 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.8 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py survey --drop 0.9 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.0 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.1 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.2 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.25 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.3 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.4 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.5 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.6 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.7 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.75 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.8 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py asia --drop 0.9 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.0 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.1 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.2 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.25 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.3 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.4 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.5 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.6 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.7 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.75 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.8 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
script_learning.py earthquake --drop 0.9 --seed 5 --max_epoch 80 --left_out "" --repeat 5 --nb_of_examples 150
```

Evaluating [survey1, ..., survey5] x [0.0, 0.1, ..., 0.9, 0.25, 0.75] x 3
```
evaluator.py survey --drop 0.0 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.1 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.2 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.25 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.3 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.4 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.5 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.6 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.7 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.75 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.8 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
evaluator.py survey --drop 0.9 --left_out "" --seed 5 --nb_of_examples 150 --nb_of_eval 3
```

Report
```
script_plot.py "0.7_0.5_150/"
script_plot.py "0.8_0.5_150/"
script_msse_plot.py survey --drop 0.7 -- seed 5 --nb_of_examples 150 --nb_of_samples 100
script_msse_plot.py survey --drop 0.8 -- seed 5 --nb_of_examples 150 --nb_of_samples 100
script_scatter_plot.py survey --left_out "" --nb_of_examples 150
```

Figure 4: `./data/results/0.8_0.5_150/survey_80_1337671202_False`

Figure 5: `./data/results/0.8_0.5_150/survey_80_1337671202_False`

Figure 6: `./data/results/scatter.txt`

Figure 7: MSSE from each survey network used in learning
