import json
import numpy as np
import pandas as pd
import math
import logging

from typing import List, Dict, Set
from teradataml.analytics.valib import *
from teradataml import DataFrame
from decimal import Decimal
from aoa.stats import store

logger = logging.getLogger(__name__)


class _NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating) or isinstance(obj, Decimal):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(_NpEncoder, self).default(obj)


def _compute_continuous_edges(variables: List[str], statistics: pd.DataFrame, dtypes: Dict, bins=10) -> List[float]:
    edges = []

    # should return what is in the feature catalog.. for now calculate linspace boundaries based on min/max
    ranges = statistics.drop(statistics.columns.difference(["xcol", "xmin", "xmax"]), axis=1)
    ranges = ranges.set_index("xcol")
    ranges.index = ranges.index.map(str.lower)
    ranges = ranges.to_dict(orient='index')

    for var in variables:
        x_min, x_max = ranges[var]["xmin"], ranges[var]["xmax"]

        # if integer type and range is less than the number of bins, only use 'range' bins
        if x_max - x_min < bins and dtypes[var].startswith("int"):
            edges.append(np.linspace(x_min, x_max, int(x_max) - int(x_min) + 1).tolist())
        # if decimal fix to two decimal places for now.. we really need to know the decimal precision to do this
        # correctly.
        elif dtypes[var].startswith("decimal") or dtypes[var].startswith("float"):
            # for bins other than 1st and last, round to two decimal places
            # (min / max must be rounded up / down accordingly so easier to just use the vals from stats)
            vals = np.linspace(x_min, x_max, bins + 1).tolist()

            for i in range(1, bins):
                vals[i] = float(Decimal("{:.2f}".format(vals[i])))

            # VAL Histogram function fails for some reason when FLOAT min boundary is set to min value,
            # so rounding min down  max is rounded up just for symmetry (max boundary set to max value
            # does work with VAL)
            p = 2
            vals[0] = np.true_divide(np.floor(vals[0] * 10 ** p), 10 ** p)
            vals[bins] = np.true_divide(np.ceil(vals[bins] * 10 ** p), 10 ** p)

            edges.append(vals)
        else:
            edges.append(np.linspace(x_min, x_max, bins + 1).tolist())

    return edges


def _convert_all_edges_to_val_str(all_edges):
    # boundaries for multiple columns follows the following format..
    # ["{10, 0, 200000}", "{5, 0, 100}"]
    boundaries = []
    for edges in all_edges:
        edges_str = ",".join(str(edge) for edge in edges)
        boundaries.append("{{ {} }}".format(edges_str))

    return boundaries


def _fill_missing_bins(bin_edges: List[float], bin_values: List[float], reference_edges: List[float]) -> List[float]:
    """
    Compare the `bin_edges` returned by VAL to `reference_edges` and fill in any missing bins with `0`.
    This is required as VAL doesn't return empty bins and so if we want to ensure we always have all the bins
    represented in the `bin_values` (which we do or else indices vs reference edges mean nothing), then we must do this.

    """
    new_bin_values = list(bin_values)

    epsilon = 1e-08
    for i, edge in enumerate(reference_edges):
        is_present = False
        for curr_edge in bin_edges:
            if abs(float(curr_edge) - float(edge)) < epsilon:
                is_present = True

        if not is_present:
            new_bin_values.insert(i, 0.0)

    return new_bin_values


def _process_categorical_var(frequencies: pd.DataFrame,
                             group_label: str,
                             variable_name: str,
                             feature_importance: float,
                             reference_categories: List) -> Dict:
    """
    Adds the following struct
    {
        "type": "categorical",
        "group": "<group-name>",
        "importance": "<feature-importance>",
        "statistics": {
            "nulls": <missing-values>,
            "categories": ["cat1", "cat2", ...]
            "frequency": {
                "cat1": 50,
                "cat2": 10,
                ...
            }
        }
    }
    """

    data_struct = {
        "type": "categorical",
        "group": group_label,
        "statistics": {}
    }

    if feature_importance:
        data_struct["importance"] = feature_importance

    var_freq = frequencies[frequencies.xcol == variable_name]

    # if first row is nan then it is the null values in the dataset. remove from histogram
    if var_freq["xval"].isnull().values.any():
        n = var_freq[var_freq["xval"].isnull()]
        data_struct["statistics"]["nulls"] = n.xcnt.tolist()[0]
        var_freq = var_freq[var_freq["xval"].notnull()]

    frequencies_dict = var_freq[["xval", "xcnt"]].set_index("xval").T.to_dict(orient='records')[0]

    # Record the reference categories. This is so we can map based on category -> index consistently for the
    # prometheus labels. This should be removed when this mapping is removed from handling in prometheus on backend.
    data_struct["categories"] = reference_categories

    # Record the `statistics.frequency` for each category (using the category as key).
    # `0` is set as the frequency for any category which is in `reference_categories` but not in `frequencies_dict`
    # This approach allows for new categories to be added over time (never removed) to reference_categories and
    # for everything to remain consistent.
    data_struct["statistics"]["frequency"] = {
        cat: frequencies_dict.get(cat, 0) if cat in reference_categories else 0 for i, cat in enumerate(reference_categories)
    }

    return data_struct


def _process_continuous_var(histogram: pd.DataFrame,
                            stats: pd.DataFrame,
                            group_label: str,
                            variable_name: str,
                            feature_importance: float,
                            reference_edges: List[float]) -> Dict:
    """
    Adds the following struct
    {
        "type": "continuous",
        "group": "<group-name>",
        "importance": "<feature-importance>",
        "statistics": {
            "nulls": <missing-values>,
            "cnt": 614.0,
            "min": 21.0,
            "max": 81.0,
            ...
            "histogram": {
              "edges": [21.0,27.0,33.0,39.0,45.0,51.0,57.0,63.0,69.0,75.0,81.0],
              "values": [248.0,122.0,77.0,62.0,45.0,23.0,20.0,13.0,3.0,1.0]
            }
        }
    }
    """

    data_struct = {
        "type": "continuous",
        "group": group_label,
        "statistics": {},
    }

    if feature_importance:
        data_struct["importance"] = feature_importance

    var_hist = histogram[histogram.xcol == variable_name].sort_values(by=['xbin'])

    # if first row is nan then it is the null values in the dataset. remove from histogram
    if var_hist["xbin"].isnull().values.any():
        n = var_hist[var_hist["xbin"].isnull()]
        data_struct["statistics"]["nulls"] = n.xcnt.tolist()[0]

        var_hist = var_hist[var_hist["xbin"].notnull()]

    bin_edges = [var_hist.xbeg.tolist()[0]] + var_hist.xend.tolist()
    bin_values = var_hist.xcnt.tolist()

    # (issue #123) VAL docs originally stated that:
    # VAL histograms will values lower than the first bin to the first bin, but values greater than the
    # largest bin are added to a new bin.. Therefore we did the same on both sides. However, it turns out this doc is
    # incorrect.

    is_right_outlier_bin = math.isnan(bin_edges[-1])
    is_left_outlier_bin = math.isnan(bin_edges[0])
    if is_right_outlier_bin:
        bin_edges = bin_edges[:-1]
    if is_left_outlier_bin:
        bin_edges = bin_edges[1:]

    # Add missing bin_values based on the bin_edges vs reference_edges.
    # VAL doesn't return empty bins
    if len(bin_edges) < len(reference_edges):
        bin_values = _fill_missing_bins(bin_edges=bin_edges, bin_values=bin_values, reference_edges=reference_edges)

    if is_right_outlier_bin:
        bin_values[-2] += bin_values[-1]
        bin_values = bin_values[:-1]
    if is_left_outlier_bin:
        bin_values[1] += bin_values[0]
        bin_values = bin_values[1:]

    def _strip_key_x(d: Dict):
        return {k[1:]: v for k, v in d.items()}

    stats_values = stats[stats.xcol == variable_name].drop(["xdb", "xtbl", "xcol"], axis=1).to_dict(orient='records')[0]
    data_struct["statistics"].update(_strip_key_x(stats_values))

    data_struct["statistics"]["histogram"] = {
        "edges": reference_edges,
        "values": bin_values
    }

    return data_struct


def _parse_scoring_stats(features_df: DataFrame,
                         predicted_df: DataFrame,
                         data_stats: Dict,
                         feature_importance: Dict[str, float] = {},
                         feature_metadata_fqtn: str = None,
                         feature_metadata_group: str = None) -> Dict:
    if not isinstance(features_df, DataFrame):
        raise TypeError("We only support teradataml DataFrame for features")

    if not isinstance(predicted_df, DataFrame):
        raise TypeError("We only support teradataml DataFrame for predictions")

    features = []
    targets = []
    categorical = []

    # ensure backward compatible (when we had targets incorrectly named as predictors..)
    if "predictors" in data_stats:
        data_stats["targets"] = data_stats.pop("predictors")

    for var_type in ["features", "targets"]:
        for name, value in data_stats[var_type].items():
            # for backward compatibility with data stats created before we lower-cased
            name = name.lower()

            if var_type == "features":
                features.append(name)
            elif var_type == "targets":
                targets.append(name)
            if "type" in value and value["type"] == "categorical":
                categorical.append(name)

    if predicted_df.shape[0] != features_df.shape[0]:
        raise ValueError("The number of prediction rows do not match the number of features rows!")

    data_stats = _capture_stats(df=features_df,
                                features=features,
                                targets=[],
                                categorical=categorical,
                                feature_importance=feature_importance,
                                feature_metadata_fqtn=feature_metadata_fqtn,
                                feature_metadata_group=feature_metadata_group)

    targets_struct = _capture_stats(df=predicted_df,
                                    features=[],
                                    targets=targets,
                                    categorical=categorical,
                                    feature_importance=feature_importance,
                                    feature_metadata_fqtn=feature_metadata_fqtn,
                                    feature_metadata_group=feature_metadata_group)

    data_stats["targets"] = targets_struct["targets"]

    return data_stats


def _capture_stats(df: DataFrame,
                   features: List,
                   targets: List,
                   categorical: List,
                   feature_importance: Dict[str, float] = {},
                   feature_metadata_fqtn: str = {},
                   feature_metadata_group: str = "default") -> Dict:
    if not isinstance(df, DataFrame):
        raise TypeError("We only support teradataml DataFrame")

    # lowercase all keys/names to avoid mismatches between sql/dataframes case sensitivity
    features = [f.lower() for f in features]
    targets = [t.lower() for t in targets]
    categorical = [c.lower() for c in categorical]
    feature_importance = {k.lower(): v for k, v in feature_importance.items()}
    df_columns = [c.lower() for c in df.columns]

    # validate that the dataframe contains the features/targets provided
    if features and not set(features).issubset(df_columns):
        raise ValueError(f"features dataframe with columns ({df.columns}) does not contain features: {features}")

    if targets and not set(targets).issubset(df_columns):
        raise ValueError(f"targets dataframe with columns ({df.columns}) does not contain targets: {targets}")

    if not feature_metadata_fqtn:
        raise ValueError("feature_metadata_fqtn must be defined")

    total_rows = df.shape[0]
    continuous_vars = list((set(features) | set(targets)) - set(categorical))
    categorical_vars = list((set(features) | set(targets)) - set(continuous_vars))
    reference_edges = []

    if len(continuous_vars) > 0:
        stats = valib.Statistics(data=df, columns=continuous_vars, stats_options="all")
        stats = stats.result.to_pandas().reset_index()
        stats["xcol"] = stats["xcol"].str.lower()

        stats_metadata = store.get_feature_stats(feature_metadata_fqtn, "continuous")

        if not all(x in stats_metadata.keys() for x in continuous_vars):
            raise Exception(f"Ensure feature statistics metadata in {feature_metadata_fqtn} are up to date. "
                            f"Attempted to compute stats for {continuous_vars} but only found the following "
                            f"continuous variables {stats_metadata.keys()}.")

        reference_edges = [stats_metadata[v.lower()]['edges'] for v in continuous_vars]

        histogram = valib.Histogram(data=df,
                                    columns=continuous_vars,
                                    boundaries=_convert_all_edges_to_val_str(reference_edges))
        histogram = histogram.result.to_pandas().reset_index()
        histogram["xcol"] = histogram["xcol"].str.lower()

    if len(categorical_vars) > 0:
        stats_metadata = store.get_feature_stats(feature_metadata_fqtn, "categorical")

        if not all(x in stats_metadata.keys() for x in categorical_vars):
            raise Exception(f"Ensure feature statistics metadata in {feature_metadata_fqtn} are up to date. "
                            f"Attempted to compute stats for {continuous_vars} but only found the following "
                            f"categorical variables {stats_metadata.keys()}.")

        reference_categories = [stats_metadata[v.lower()]["categories"] for v in categorical_vars]

        frequencies = valib.Frequency(data=df, columns=categorical_vars)
        frequencies = frequencies.result.to_pandas().reset_index()
        frequencies["xcol"] = frequencies["xcol"].str.lower()

    data_struct = {
        "num_rows": total_rows,
        "features": {},
        "targets": {}
    }

    def add_var_metadata(variable_type, group_label):
        if variable_name in continuous_vars:
            data_struct[variable_type][variable_name] = _process_continuous_var(
                histogram=histogram,
                stats=stats,
                reference_edges=reference_edges[continuous_vars.index(variable_name)],
                group_label=group_label,
                variable_name=variable_name,
                feature_importance=feature_importance.get(variable_name, None))

        else:
            data_struct[variable_type][variable_name] = _process_categorical_var(
                frequencies=frequencies,
                group_label=group_label,
                variable_name=variable_name,
                feature_importance=feature_importance.get(variable_name, None),
                reference_categories=reference_categories[categorical_vars.index(variable_name)]
            )

    for variable_name in features:
        add_var_metadata("features", feature_metadata_group)

    for variable_name in targets:
        add_var_metadata("targets", feature_metadata_group)

    return data_struct
