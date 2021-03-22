import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys

NATIVE_DATA_FILE = "kernels_native_aks.dat"
FAASM_DATA_FILE = "kernels_faasm_aks.dat"
OUT_FILE = "kernels.png"


def _load_results():
    with open(NATIVE_DATA_FILE) as json_file:
        native_results = json.load(json_file)
    with open(FAASM_DATA_FILE) as json_file:
        faasm_results = json.load(json_file)
    return native_results, faasm_results


def _check_results(native_results, faasm_results):
    """
    Check that both native and faasm experiments have:
    (1) Run with the same kernels
    (2) Run with the same number of processes
    """
    # If the two experiments recorded results for different kernels, error out
    if native_results.keys() != faasm_results.keys():
        print(
            "Kernels mismatch!\n - Native: {}\n - Faasm: {}".format(
                native_results.keys(), faasm_results.keys()
            )
        )
        return False

    # If the experiments run with different number of processes, error out
    for key in native_results.keys():
        if len(native_results[key]) != len(faasm_results[key]):
            print("Number of processes in kernel {} mismatch!".format(key))
            print(
                " - Native: {}\n - Faasm: {}".format(
                    native_results[key], faasm_results[key]
                )
            )
            return False

    return True


def main():
    native_results, faasm_results = _load_results()

    # Check for the validity of results
    if not _check_results(native_results, faasm_results):
        sys.exit(1)

    # Define the independent variables
    # Note that we must fit all the columns for each kernel, e.g. if n is odd:
    # ... [x - w - w /2, x - w/2] [x - w/2, x + w/2] [x + w/2, x + w + w/2] ...
    labels = list(native_results.keys())
    num_procs = len(native_results[labels[0]])
    xs = np.arange(len(labels))
    xmin = xs[0] - 0.5
    xmax = xs[-1] + 0.5
    if (num_procs % 2) == 0:
        col_width = 0.5 / (0.5 + num_procs / 2)
        x_base = [x - (num_procs / 2 * col_width + col_width / 2) for x in xs]
    else:
        col_width = 0.5 / (1 + num_procs / 2)
        x_base = [x - (num_procs / 2 * col_width) for x in xs]
    print(labels)

    # Define the dependent variables
    fig, ax = plt.subplots()
    y = []
    for num_proc in range(num_procs):
        _faasm = [faasm_results[label][num_proc] for label in labels]
        _native = [native_results[label][num_proc] for label in labels]
        # Each bar must be set at the midpoint of the right offset
        x = [_x + num_proc * col_width + col_width / 2 for _x in x_base]
        # We plot the slowdown
        y = [float(_f / _n) for _f, _n in zip(_faasm, _native)]
        ax.bar(x, y, col_width)

    # Prepare legend
    ax.legend(["{} MPI proc.".format(2 ** num) for num in range(num_procs)])

    # Aesthetics
    plt.hlines(1, xmin, xmax, linestyle="dashed", colors="red")
    plt.xlim(xmin, xmax)
    plt.ylim(0, 2)
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Slowdown [faasm / native]")
    ax.set_title("Kernels time to completion slowdown Faasm vs Native")
    fig.tight_layout()
    plt.savefig(OUT_FILE)


if __name__ == "__main__":
    main()
