from invoke import task
from tasks.util.env import PROJ_ROOT
from os.path import join
import matplotlib.pyplot as plt
import pandas as pd

RESULTS_DIR = join(PROJ_ROOT, "results")


@task
def covid(ctx):
    """
    Plot the covid results
    """
    native_csv = join(RESULTS_DIR, "covid", "covid_native.csv")
    native_df = pd.read_csv(native_csv)

    # Average over runs
    native_df = native_df.groupby(["Threads"]).mean()

    # Plot
    native_df.plot.line(y="Time(s)")
    plt.show()
