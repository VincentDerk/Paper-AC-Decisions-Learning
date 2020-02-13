"""
By Vincent Derkinderen (DTAI lab KU Leuven, 2019)

Small code example that was used to interactively extract information from previous maximisation experiments.
"""
import os
import statistics
import sys
import pickle


def main(args):
    results_constrained = dict()
    results_unconstrained = dict()
    progress = dict()

    # Load info for constrained case
    for file in os.listdir("./data/results/constrained/"):
        if file.endswith("decisionresults.p"):
            with open("./data/results/constrained/" + file, 'rb') as f:
                results_constrained[file] = pickle.load(f)  # [decisions, eu, size, compile_time, runtime]

    # Load info for unconstrained case
    for file in os.listdir("./data/results/unconstrained/"):
        if file.endswith("decisionresults.p"):
            with open("./data/results/unconstrained/" + file, 'rb') as f:
                results_unconstrained[file] = pickle.load(f)  # [decisions, eu, size, compile_time, runtime]
        if file.endswith("_euprogress.p"):
            with open("./data/results/unconstrained/" + file, 'rb') as f:
                progress[file] = pickle.load(f)  #

    # Average difference
    differences = [results[1] - results_unconstrained.get(file)[1] for file, results in results_constrained.items()]
    print("The average EU difference: %s" % statistics.mean(differences))

    # Average relative difference
    relative_differences = [abs((results[1] - results_unconstrained.get(file)[1]) / results[1]) for file, results in
                            results_constrained.items()]
    print("The average relative EU difference: %s" % statistics.mean(relative_differences))

    # fraction of differences less than 0.1
    trimmed_constrained = {file: results for file, results in results_constrained.items() if
                           abs(results[1] - results_unconstrained.get(file)[1]) < 0.1}
    fraction_lower = len(trimmed_constrained) / len(results_constrained)
    #trimmed_unconstrained = {file: results for file, results in results_unconstrained.items() if
    #                       abs(results[1] - results_constrained.get(file)[1]) < 0.1}
    print("The fraction of results with a difference lower than 0.1: %s" % fraction_lower)

    # Average runtime, compiletime and SDD size
    constrained_compile_times = [ctime for file, [dec, eu, size, ctime, rtime] in results_constrained.items()]
    unconstrained_compile_times = [ctime for file, [dec, eu, size, ctime, rtime] in results_unconstrained.items()]
    constrained_run_times = [rtime for file, [dec, eu, size, ctime, rtime] in results_constrained.items()]
    unconstrained_run_times = [rtime for file, [dec, eu, size, ctime, rtime] in results_unconstrained.items()]
    constrained_sizes = [size for file, [dec, eu, size, ctime, rtime] in results_constrained.items()]
    unconstrained_sizes = [size for file, [dec, eu, size, ctime, rtime] in results_unconstrained.items()]

    print('Constrained avg runtime (s): %s' % statistics.mean(constrained_run_times))
    print("Constrained avg compiletime (s): %s" % statistics.mean(constrained_compile_times))
    print("Constrained avg SDD size: %s" % statistics.mean(constrained_sizes))
    print('Unconstrained avg runtime (s): %s' % statistics.mean(unconstrained_run_times))
    print("Unconstrained avg compiletime (s): %s" % statistics.mean(unconstrained_compile_times))
    print("Unconstrained avg SDD size: %s" % statistics.mean(unconstrained_sizes))


    # Averages runtime, compiletime and SDD size per dataset
    for name in ["asia", "survey", "earthquake"]:
        c_compile_times = [ctime for file, [dec, eu, size, ctime, rtime] in results_constrained.items() if name in file]
        u_compile_times = [ctime for file, [dec, eu, size, ctime, rtime] in results_unconstrained.items() if name in file]
        c_run_times = [rtime for file, [dec, eu, size, ctime, rtime] in results_constrained.items() if name in file]
        u_run_times = [rtime for file, [dec, eu, size, ctime, rtime] in results_unconstrained.items() if name in file]
        c_sizes = [size for file, [dec, eu, size, ctime, rtime] in results_constrained.items() if name in file]
        u_sizes = [size for file, [dec, eu, size, ctime, rtime] in results_unconstrained.items() if name in file]
        print("\nFor %s" % name)
        print('Constrained avg runtime (s): %s' % statistics.mean(c_run_times))
        print("Constrained avg compiletime (s): %s" % statistics.mean(c_compile_times))
        print("Constrained avg SDD size: %s" % statistics.mean(c_sizes))
        print('Unconstrained avg runtime (s): %s' % statistics.mean(u_run_times))
        print("Unconstrained avg compiletime (s): %s" % statistics.mean(u_compile_times))
        print("Unconstrained avg SDD size: %s" % statistics.mean(u_sizes))


    #constrained_trimmed, unconstrained_trimmed = print_diff_results(results_constrained, results_unconstrained)

    #results_constrained_trimmed = {file: results for file, results in results_constrained.items() if len(results[0]) >= 4}
    #results_unconstrained_trimmed = {file: results for file, results in results_unconstrained.items() if len(results[0]) >= 4}
    #progress_trimmed = {file: results for file, results in progress.items() if results_constrained_trimmed.get(file.replace("euprogress", "decisionresults")) is not None}

    # Some other stuff
    # diff_c = [c - u for c, u in zip(constrained_compile_times, unconstrained_compile_times)]
    # diff_r = [c - u for c, u in zip(constrained_run_times, unconstrained_run_times)]
    #
    #
    # with open("./data/results/compile_time_differences.txt", 'w') as f:
    #     f.write("% constrained compile_time")
    #     for ctime in constrained_compile_times:
    #         f.write("{}\\\\".format(ctime))
    #     f.write("\n")
    #     f.write("\n")
    #     f.write("% unconstrained compile_time")
    #     for ctime in unconstrained_compile_times:
    #         f.write("{}\\\\".format(ctime))
    #
    # print("constrained compile time")
    # print(constrained_compile_times)
    # print("unconstrained compile time")
    # print(unconstrained_compile_times)


def print_diff_results(results_constrained, results_unconstrained):
    """
    Trim the given results to those with a difference >= 0.1. For each constrained and unconstrained result
    with the same key, if the expected utility (index 1) difference is >= 0.1, the item is added to the trimmed version.

    :param results_constrained: The results of the maximisation process using the constrained approach.
    :type results_constrained: dict[Any, list[Any, float, Any, Any, Any]
    :param results_unconstrained: The results of the maximisation process using the unconstrained approach.
    :type results_unconstrained: dict[Any, list[Any, float, Any, Any, Any]
    :return: The two input results but trimmed to only those files where the abs. difference in result is >= 0.1
    :rtype dict[Any, list[Any, float, Any, Any, Any], dict[Any, list[Any, float, Any, Any, Any]
    """
    diff_files = set()
    for key, results in results_constrained.items():
        diff = abs(results[1] - results_unconstrained.get(key)[1])  # eu_con - eu_uncon
        if diff >= 0.1:
            diff_files.add(key)
    results_constrained_trimmed = {file: results for file, results in results_constrained.items() if file.replace("euprogress.p", "decisionresults.p") in diff_files}
    results_unconstrained_trimmed = {file: results for file, results in results_unconstrained.items() if file.replace("euprogress.p", "decisionresults.p") in diff_files}
    print("Results constrained trimmed to error >= 0.1")
    print(results_constrained_trimmed)
    print("Results unconstrained trimmed to error >= 0.1")
    print(results_unconstrained_trimmed)
    return results_constrained_trimmed, results_unconstrained_trimmed


if __name__ == '__main__':
    main(sys.argv)
