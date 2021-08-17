import pandas as pd


def read_hoststats(csv_file, base_ts=None):
    results = pd.read_csv(csv_file)

    results["Timestamp"] = pd.to_datetime(results["Timestamp"])

    # If no base timestamp given, take the first in the data
    if not base_ts:
        base_ts = results["Timestamp"][0]

    # Put all timestamps relative to the base timestamp in seconds
    results["Timestamp"] -= base_ts

    return results


def avg_hoststats_across_hosts(stats, stat_name):
    pass
