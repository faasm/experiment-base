from invoke import task
from tasks.util.env import PROJ_ROOT
from os.path import join, exists
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd

import matplotlib

RESULTS_DIR = join(PROJ_ROOT, "results", "lammps")


def _read_results(csv):
    csv = join(RESULTS_DIR, "covid", csv)

    if not exists(csv):
        raise RuntimeError("CSV not found: {}".format(csv))

    results = pd.read_csv(csv)

    grouped = results.groupby("WorldSize")
    times = grouped.mean()
    errs = grouped.std()

    return grouped, times, errs


@task(default=True)
def plot(ctx):
    """
    Plot the LAMMPS results
    """
    matplotlib.use("tkagg")

    native_csv = join(RESULTS_DIR, "lammps_native.csv")
    wasm_csv = join(RESULTS_DIR, "lammps_wasm.csv")

    native_grouped, native_times, native_errs = _read_results(native_csv)
    wasm_grouped, wasm_times, wasm_errs = _read_results(wasm_csv)

    ax = plt.subplot(111)

    wasm_times.plot.line(
        y="Actual",
        yerr=wasm_errs,
        ecolor="gray",
        elinewidth=0.8,
        capsize=1.0,
        ax=ax,
        label="Faasm",
    )

    native_times.plot.line(
        y="Actual",
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
