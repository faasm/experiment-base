from os import makedirs
from os.path import join, exists

from math import sqrt
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
from invoke import task
from hoststats.results import HostStatsResults

from tasks.util.env import PLOTS_FORMAT, PLOTS_ROOT, PROJ_ROOT

RESULTS_DIR = join(PROJ_ROOT, "results", "lammps")
PLOTS_DIR = join(PLOTS_ROOT, "lammps")

BENCHMARKS = ["compute", "network"]
PLOT_COORDS = [0, 1]


def _read_results(csv):
    csv = join(RESULTS_DIR, csv)

    if not exists(csv):
        raise RuntimeError("CSV not found: {}".format(csv))

    results = pd.read_csv(csv)

    grouped = results.groupby("WorldSize", as_index=False)
    times = grouped.mean()
    # Note that we use the standard error for correct error propagation
    errs = grouped.sem()

    return grouped, times, errs


@task(default=True)
def plot(ctx, gui=False, plot_elapsed_times=True):
    """
    Plot the LAMMPS results
    """
    fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True)
    makedirs(PLOTS_DIR, exist_ok=True)
    plot_file = join(PLOTS_DIR, "runtime.png")

    fig.suptitle(
        "LAMMPS speed-up Faasm vs OpenMPI\n(overlayed with elapsed time)"
    )

    for bench, coords in zip(BENCHMARKS, PLOT_COORDS):
        # Process data
        native_csv = join(RESULTS_DIR, "lammps_native_{}.csv".format(bench))
        wasm_csv = join(RESULTS_DIR, "lammps_wasm_{}.csv".format(bench))

        native_grouped, native_times, native_errs = _read_results(native_csv)
        wasm_grouped, wasm_times, wasm_errs = _read_results(wasm_csv)

        # Divide by first result to obtain speedup
        native_single = native_times["Actual"][0]
        wasm_single = wasm_times["Actual"][0]
        native_speedup = [
            native_single / time for time in native_times["Actual"]
        ]
        wasm_speedup = [wasm_single / time for time in wasm_times["Actual"]]

        # Error propagation (for dummies)
        # https://www.dummies.com/education/science/biology/simple-error-propagation-formulas-for-simple-expressions/
        native_speedup_errs = []
        native_err_single = native_errs["Actual"][0]
        for native_sup, native_e, native_t in zip(
            native_speedup, native_errs["Actual"], native_times["Actual"]
        ):
            native_speedup_errs.append(
                native_sup
                * sqrt(
                    pow(native_err_single / native_single, 2)
                    + pow(native_e / native_t, 2)
                )
            )
        wasm_speedup_errs = []
        wasm_err_single = wasm_errs["Actual"][0]
        for wasm_sup, wasm_e, wasm_t in zip(
            wasm_speedup, wasm_errs["Actual"], wasm_times["Actual"]
        ):
            wasm_speedup_errs.append(
                wasm_sup
                * sqrt(
                    pow(wasm_err_single / wasm_single, 2)
                    + pow(wasm_e / wasm_t, 2)
                )
            )

        # Plot speed up data with error bars
        ax[coords].errorbar(
            wasm_times["WorldSize"],
            wasm_speedup,  # Change to wasm_times["Actual"] for time elapsed plot
            yerr=wasm_speedup_errs,
            fmt=".-",
            label="Faasm",
            ecolor="gray",
            elinewidth=0.8,
            capsize=1.0,
        )
        ax[coords].errorbar(
            native_times["WorldSize"],
            native_speedup,  # Change to native_times["Actual"] for time elapsed plot
            yerr=native_speedup_errs,
            fmt=".-",
            label="OpenMPI",
            ecolor="gray",
            elinewidth=0.8,
            capsize=1.0,
        )

        if plot_elapsed_times:
            # Plot elapsed time in a separate y axis
            ax_et = ax[coords].twinx()
            ax_et.errorbar(
                wasm_times["WorldSize"],
                wasm_times["Actual"],
                yerr=wasm_errs["Actual"],
                fmt=".--",
                label="Faasm",
                ecolor="gray",
                elinewidth=0.8,
                capsize=1.0,
                alpha=0.3,
            )
            ax_et.errorbar(
                native_times["WorldSize"],
                native_times["Actual"],
                yerr=native_errs["Actual"],
                fmt=".--",
                label="OpenMPI",
                ecolor="gray",
                elinewidth=0.8,
                capsize=1.0,
                alpha=0.3,
            )
            ax_et.set_ylabel("Elapsed time [s]")

        ax[coords].title.set_text("{}-bound benchmark".format(bench))
        ax[coords].set_ylim(bottom=0)
        ax[coords].set_xlim(left=1)
        ax[coords].set_xlabel("MPI World Size")
        ax[coords].set_ylabel("Speed Up (vs 1 MPI Proc performance)")

    #         tick_spacing = 1
    #         ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

    # Print legend
    handles, labels = ax[1].get_legend_handles_labels()
    fig.legend(handles, labels)

    fig.tight_layout()

    # Manually add common axis labels
    fig.text(0.015, 0.5, "", ha="center", va="center", rotation="vertical")

    if gui:
        fig.show()
    else:
        fig.savefig(plot_file, format=PLOTS_FORMAT)


@task
def plot_resources(ctx, world_size, run=0, gui=False):
    native_file = join(
        RESULTS_DIR,
        "hoststats_native_compute_{}_{}.csv".format(world_size, run),
    )

    wasm_file = join(
        RESULTS_DIR, "hoststats_wasm_compute_{}_{}.csv".format(world_size, run)
    )

    native_stats = HostStatsResults(native_file)
    wasm_stats = HostStatsResults(wasm_file)

    makedirs(PLOTS_ROOT, exist_ok=True)
    plot_file = join(PLOTS_DIR, "resources.png")

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

    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles, labels)

    plt.tight_layout()

    if gui:
        plt.show()
    else:
        plt.savefig(plot_file, format=PLOTS_FORMAT)


@task
def plot_all_resources(ctx, bench, run=0, gui=False):
    # TODO - this is hardcoded for a run from 1 to 16 procs
    fig = plt.figure(figsize=(32, 8))
    outer = gridspec.GridSpec(8, 2, wspace=0.2, hspace=3)

    makedirs(PLOTS_ROOT, exist_ok=True)
    plot_file = join(PLOTS_DIR, "all_resources_{}.png".format(bench))

    for world_size in range(16):
        ax = plt.Subplot(
            fig, outer[world_size], frameon=False, xticks=[], yticks=[]
        )
        ax.set_title(
            "MPI World Size: {}".format(world_size + 1), fontweight="bold"
        )
        fig.add_subplot(ax)

        inner = gridspec.GridSpecFromSubplotSpec(
            1, 4, subplot_spec=outer[world_size], wspace=0.4, hspace=0
        )

        plot_single_run(plt, fig, inner, bench, world_size + 1)

    plt.tight_layout()
    plt.suptitle("Resource Usage for {}-bound benchmark".format(bench), fontsize="x-large", fontweight="bold")

    if gui:
        plt.show()
    else:
        plt.savefig(plot_file, format=PLOTS_FORMAT)


# TODO: average the runs
def plot_single_run(plt, fig, grid, bench, world_size, run=0):
    native_file = join(
        RESULTS_DIR,
        "hoststats_native_{}_{}_{}.csv".format(bench, world_size, run),
    )
    wasm_file = join(
        RESULTS_DIR,
        "hoststats_wasm_{}_{}_{}.csv".format(bench, world_size, run),
    )

    try:
        native_stats = HostStatsResults(native_file)
    except RuntimeError:
        print("native stats file not found")
        return
    try:
        wasm_stats = HostStatsResults(wasm_file)
    except RuntimeError:
        print("wasm stats file not found")
        return

    all_resources = [
        ["CPU_PCT", "%"],
        ["MEMORY_USED", "MB"],
        ["DISK_READ_MB", "MB"],
        ["NET_SENT_MB", "MB"],
    ]

    for index, pair in enumerate(all_resources):
        resource = pair[0]
        unit = pair[1]

        ax = plt.Subplot(fig, grid[index])
        plot_hoststats_resource(ax, native_stats, wasm_stats, resource, unit)

        # Plot legend only on the first run
        if index == 0:
            handles, labels = ax.get_legend_handles_labels()
            fig.legend(handles, labels)

        fig.add_subplot(ax)



def plot_hoststats_resource(
    ax,
    native_stats: HostStatsResults,
    wasm_stats: HostStatsResults,
    stat,
    y_label,
):
    ax.set_title("{}".format(stat), fontsize="small")

    wasm_series = wasm_stats.get_median_stat(stat)
    wasm_series.index = wasm_series.index.total_seconds()
    wasm_series.plot(ax=ax, label="Faasm")

    native_series = native_stats.get_median_stat(stat)
    native_series.index = native_series.index.total_seconds()
    native_series.plot(ax=ax, label="OpenMPI")

    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0)

    ax.set_ylabel(y_label, fontsize="small")
    ax.set_xlabel("Time (s)", fontsize="small")
