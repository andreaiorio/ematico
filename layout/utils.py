import numpy as np
import pandas as pd


def get_min_max_threshold(test, df, df_rif, threshold=0.1):
    opt_min, opt_max = get_optimal_values(test, df_rif)
    min_y = np.round((1 - threshold) * min(min(df[test]), opt_min), 2)
    max_y = np.round((1 + threshold) * max(max(df[test]), opt_max), 2)
    return min_y, max_y


def get_percentage(value, test, df, df_rif, threshold=0.25):
    opt_min, opt_max = get_optimal_values(test, df_rif)

    # Normalize value between 0 and 1
    value = (value - opt_min) / (opt_max - opt_min)

    # Shrink the range between 0.25 and 0.75
    value = threshold + 2 * threshold * value

    # Convert to percentage and round
    return int(value * 100)


def get_last_date(df):
    date = df.tail(1)["Data"].values[0]
    date = pd.to_datetime(str(date)).strftime("%B %d, %Y")
    return date


def get_last_date_test(test, df):
    index_date = df[test].dropna().tail(1).index[-1]
    date = df.loc[index_date, "Data"]
    date = date.strftime("%d/%m/%Y")
    return date


def get_optimal_values(test, df_rif):
    return df_rif[test][0], df_rif[test][1]


def get_label(test, df_rif):
    return df_rif[test][2]


def make_slug(word):
    return word.replace(" ", "-").lower()
