from os.path import join, exists

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from invoke import task

from tasks.util.env import PROJ_ROOT
from tasks.util.hoststats import read_hoststats

RESULTS_DIR = join(PROJ_ROOT, "results", "lammps")


def _read_results(csv):
    csv = join(RESULTS_DIR, csv)

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
        csv_elinewidth=0.8,
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

    plt.title("Runtime Faasm vs native")
    ax.set_ylim(bottom=0)

    ax.set_ylabel("Time (s)")
    ax.set_xlabel("MPI world size")

    plt.tight_layout()
    plt.show()


@task
def plot_resources(ctx, world_size, run=0):
    native_file = join(
        RESULTS_DIR, "hoststats_native_{}_{}.csv".format(world_size, run)
    )

    wasm_file = join(
        RESULTS_DIR, "hoststats_wasm_{}_{}.csv".format(world_size, run)
    )

    native_stats = read_hoststats(native_file)
    wasm_stats = read_hoststats(wasm_file)

    fig = plt.figure()
    fig.suptitle("World size {}, run {}".format(world_size, run))

    ax = plt.subplot(221)
    plot_hoststats_resource(ax, native_stats, wasm_stats, "CPU_PCT", "%")

    ax = plt.subplot(222)
    plot_hoststats_resource(ax, native_stats, wasm_stats, "MEMORY_USED", "MB")

    ax = plt.subplot(223)
    plot_hoststats_resource(ax, native_stats, wasm_stats, "DISK_READ_MB", "MB")

    ax = plt.subplot(224)
    plot_hoststats_resource(ax, native_stats, wasm_stats, "NET_SENT_MB", "MB")

    plt.tight_layout()
    plt.show()


def plot_hoststats_resource(ax, native_stats, wasm_stats, stat, y_label):
    plt.title("{}".format(stat))

    wasm_stats.plot.line(
        y=stat,
        ax=ax,
        label="Faasm",
    )

    native_stats.plot.line(
        y=stat,
        ax=ax,
        label="Native",
    )

    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)

    ax.set_ylabel(y_label)
    ax.set_xlabel("Time (s)")
