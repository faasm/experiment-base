from invoke import task
from tasks.util.env import PROJ_ROOT
from os.path import join
import matplotlib.pyplot as plt
import pandas as pd

import matplotlib

matplotlib.use("tkagg")

RESULTS_DIR = join(PROJ_ROOT, "results")


def _do_individual_plot(csv, label, ax):
    results = pd.read_csv(csv)

    # Average over runs
    grouped = results.groupby("Threads")
    times = grouped.mean()
    errs = grouped.std()

    times.plot.line(
        y=["Setup", "Execution", "Total"],
        yerr=errs,
        ecolor="gray",
        elinewidth=0.8,
        capsize=1.0,
        ax=ax,
    )

    plt.title("{} CovidSim".format(label))
    plt.ylabel("Time (s)")

    return grouped, times, errs


@task
def plot(ctx):
    """
    Plot the covid results
    """
    native_csv = join(RESULTS_DIR, "covid", "covid_native.csv")
    wasm_csv = join(RESULTS_DIR, "covid", "covid_wasm.csv")

    ax = plt.subplot(311)
    native_grouped, native_times, native_errs = _do_individual_plot(
        native_csv, "Native", ax
    )

    ax = plt.subplot(312)
    wasm_grouped, wasm_times, wasm_errs = _do_individual_plot(
        wasm_csv, "Wasm", ax
    )

    # Combined plot
    ax = plt.subplot(313)
    wasm_times.plot.line(y="Total", yerr=wasm_errs, ecolor="gray", ax=ax)
    native_times.plot.line(y="Total", yerr=native_errs, ecolor="gray", ax=ax)
    plt.title("Combined")

    plt.tight_layout()
    plt.show()
