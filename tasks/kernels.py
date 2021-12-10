from invoke import task
from os import makedirs
from os.path import join, exists

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.util.env import PLOTS_FORMAT, PLOTS_ROOT, PROJ_ROOT

RESULTS_DIR = join(PROJ_ROOT, "results", "kernels")
PLOTS_DIR = join(PLOTS_ROOT, "kernels")
NATIVE_CSV = join(RESULTS_DIR, "kernels_native.csv")
WASM_CSV = join(RESULTS_DIR, "kernels_wasm.csv")
OUT_FILE = join(PLOTS_DIR, "slowdown.png")


def _read_results(csv):
    if not exists(csv):
        raise RuntimeError("CSV not found: {}".format(csv))

    results = pd.read_csv(csv)

    # First filter only the timing stats, and then group by kernel
    results = results.loc[results["StatName"] == "Avg time (s)"]
    results = results.groupby("Kernel", as_index=False)

    # Second, group by world size
    result_dict = {}
    for name, group in results:
        # TODO - how do we present errors in a slowdown plot?
        result_dict[name] = group.groupby("WorldSize", as_index=False).mean()

    return result_dict


def _check_results(native_results, wasm_results):
    """
    Check that both native and faasm experiments have:
    (1) Run with the same kernels
    (2) Run with the same number of processes
    """
    # If the two experiments recorded results for different kernels, error out
    if native_results.keys() != wasm_results.keys():
        print(
            "Kernels mismatch!\n - Native: {}\n - Faasm: {}".format(
                native_results.keys(), wasm_results.keys()
            )
        )
        return False

    # If the experiments run with different number of processes, error out
    for key in native_results.keys():
        if (
            native_results[key]["WorldSize"].count()
            != wasm_results[key]["WorldSize"].count()
        ):
            print("Number of processes in kernel {} mismatch!".format(key))
            print(
                " - Native: {}\n - Faasm: {}".format(
                    native_results[key], wasm_results[key]
                )
            )
            return False

    return True


@task
def plot(ctx):
    """
    Plot slowdown for MPI kernels
    """
    makedirs(PLOTS_DIR, exist_ok=True)

    # Load results and sanity check
    native_results = _read_results(NATIVE_CSV)
    wasm_results = _read_results(WASM_CSV)
    if not _check_results(native_results, wasm_results):
        return

    # Define the independent variables
    # Note that we must fit all the columns for each kernel, e.g. if n is odd:
    # ... [x - w - w /2, x - w/2] [x - w/2, x + w/2] [x + w/2, x + w + w/2] ...
    kernels = wasm_results.keys()
    num_procs = len(
        wasm_results[next(iter(wasm_results))]["WorldSize"].tolist()
    )
    xs = np.arange(len(kernels))
    xmin = xs[0] - 0.5
    xmax = xs[-1] + 0.5
    if (num_procs % 2) == 0:
        col_width = 0.5 / (0.5 + num_procs / 2)
        x_base = [x - (num_procs / 2 * col_width + col_width / 2) for x in xs]
    else:
        col_width = 0.5 / (1 + num_procs / 2)
        x_base = [x - (num_procs / 2 * col_width) for x in xs]

    # Define the dependent variables
    fig, ax = plt.subplots()
    y = []
    # We group the results by kernel, but plot them world size by world size,
    # in order to get the right x offset
    for num_proc in range(num_procs):
        _faasm = [
            wasm_results[kern]["StatValue"].tolist()[num_proc]
            for kern in wasm_results.keys()
        ]
        _native = [
            native_results[kern]["StatValue"].tolist()[num_proc]
            for kern in native_results.keys()
        ]
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
    ax.set_xticklabels(wasm_results.keys())
    ax.set_ylabel("Slowdown [faasm / native]")
    ax.set_title("Kernels time to completion slowdown Faasm vs Native")
    fig.tight_layout()
    plt.savefig(OUT_FILE, format=PLOTS_FORMAT)
