from glob import glob
from invoke import task
from os import makedirs
from os.path import join

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from tasks.util.env import PLOTS_FORMAT, PLOTS_ROOT, PROJ_ROOT

RESULTS_DIR = join(PROJ_ROOT, "results", "lulesh")
PLOTS_DIR = join(PLOTS_ROOT, "lulesh")
OUT_FILE = join(PLOTS_DIR, "runtime.{}".format(PLOTS_FORMAT))


def _read_results(mode):
    result_dict = {}

    for csv in glob(join(RESULTS_DIR, "lulesh_{}_*.csv".format(mode))):
        results = pd.read_csv(csv)

        num_thread = int(csv.split("_")[-1].split(".")[0])

        result_dict[num_thread] = [
            results["Time"].mean(),
            results["Time"].sem(),
        ]

    return result_dict


@task
def plot(ctx):
    """
    Plot migration figure
    """
    makedirs(PLOTS_DIR, exist_ok=True)

    # Load results
    native_results = _read_results("native")

    # Plot results
    fig, ax = plt.subplots()
    x = list(native_results.keys())
    x.sort()
    y = [native_results[xs][0] for xs in x]
    yerr = [native_results[xs][1] for xs in x]
    ax.errorbar(x, y, yerr=yerr, fmt=".-")

    # Prepare legend
    ax.legend(["OpenMP"])

    # Aesthetics
    ax.set_ylabel("Elapsed time [s]")
    ax.set_xlabel("# of parallel functions")
    ax.set_ylim(0)
    ax.set_xlim(0)

    fig.tight_layout()
    # plt.gca().set_aspect(0.012)
    plt.savefig(OUT_FILE, format=PLOTS_FORMAT, bbox_inches="tight")

    return
