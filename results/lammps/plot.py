import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas
import sys

NATIVE_DATA_FILE = "lammps_native.csv"
WASM_DATA_FILE = "lammps_wasm.csv"
OUT_FILE = "lammps.png"


def _load_results():
    native_results = []
    wasm_results = []
    for f in [
        _f for _f in os.listdir(".") if os.path.isfile(_f) and ".csv" in _f
    ]:
        if "native" in f:
            native_results.append((f, pandas.read_csv(f)))
        elif "wasm" in f:
            wasm_results.append((f, pandas.read_csv(f)))
    return native_results, wasm_results


def _beautify_name(file_name):
    return " ".join(file_name.strip(".csv").split("_")[1:])


def main():
    native_results, wasm_results = _load_results()

    # Define the dependent variables
    fig, ax = plt.subplots()
    legend = []
    for file_name, native_result in native_results:
        print("Plotting {}".format(file_name))
        native_out = native_result.groupby("Processes").agg([np.mean, np.std])[
            "Time(s)"
        ]
        print(native_out)
        native_out.plot(y="mean", yerr="std", ax=ax, marker=".")
        legend.append(_beautify_name(file_name))
    for file_name, wasm_result in wasm_results:
        print("Plotting {}".format(file_name))
        wasm_out = wasm_result.groupby("Processes").agg([np.mean, np.std])[
            "Time(s)"
        ]
        print(wasm_out)
        wasm_out.plot(y="mean", yerr="std", ax=ax, marker=".")
        legend.append(_beautify_name(file_name))

    # Prepare legend
    ax.legend(legend)
    ax.set_xlabel("MPI Processes")
    ax.set_ylabel("Average Time [s]")
    ax.set_title("LAMMPS Runtime wasm vs native")
    ymin = 0
    ymax = 25
    plt.ylim(ymin, ymax)

    plt.savefig(OUT_FILE)


if __name__ == "__main__":
    main()
