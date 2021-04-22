from invoke import task
from tasks.util.env import PROJ_ROOT
from os.path import join, exists
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

import matplotlib

matplotlib.use("tkagg")

RESULTS_DIR = join(PROJ_ROOT, "results")


def read_results(csv):
    csv = join(RESULTS_DIR, "covid", csv)

    if not exists(csv):
        raise RuntimeError("CSV not found: {}".format(native_csv))

    results = pd.read_csv(csv)

    grouped = results.groupby("Threads")
    times = grouped.mean()
    errs = grouped.std()

    return grouped, times, errs


@task
def plot(ctx, country="Guam"):
    """
    Plot the covid results
    """
    native_csv = "covid_native_{}.csv".format(country)
    wasm_csv = "covid_wasm_{}.csv".format(country)

    native_grouped, native_times, native_errs = read_results(native_csv)
    wasm_grouped, wasm_times, wasm_errs = read_results(wasm_csv)

    ax = plt.subplot(111)
    
    wasm_times.plot.line(
        y="Execution",
        yerr=wasm_errs,
        ecolor="gray",
        elinewidth=0.8,
        capsize=1.0,
        ax=ax,
        label="Faasm",
    )
   
    native_times.plot.line(
        y="Execution",
        yerr=native_errs,
        ecolor="gray",
        elinewidth=0.8,
        capsize=1.0,
        ax=ax,
        label="Native",
    )

    tick_spacing = 1
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    plt.title("Combined")
    ax.set_ylim(bottom=0)

    plt.tight_layout()
    plt.show()
