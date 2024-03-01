import pandas as pd
import ujson
import re


def load_excel(file_path, usecols, start_row):
    df = pd.read_excel(file_path, usecols=usecols, skiprows=start_row - 1, header=None)
    df.columns = (
        ["SEMEL_YISH", "CLUSTER"]
        if len(usecols) == 2
        else ["SEMEL_YISH", "STAT11", "CLUSTER"]
    )
    df["SEMEL_YISH"] = (
        pd.to_numeric(df["SEMEL_YISH"], errors="coerce").fillna(0).astype(int)
    )
    if "STAT11" in df.columns:
        df["STAT11"] = (
            pd.to_numeric(df["STAT11"], errors="coerce").fillna(0).astype(int)
        )
    return df


# Load data
df_authorities = load_excel("data/authorities.xlsx", [1, 6], 11)
df_localities = load_excel("data/localities.xlsx", [5, 12], 10)
df_areas = load_excel("data/areas.xlsx", [0, 2, 6], 9)

# Load the GeoJSON file
with open("data/statistical_areas.geojson", "r") as f:
    geojson_data = ujson.load(f)

matched_features = []

for feature in geojson_data["features"]:
    semel_yish = int(feature["properties"].get("SEMEL_YISH", 0))
    stat11 = int(feature["properties"].get("STAT11", 0))
    cluster = None

    # Check authorities
    match_authorities = df_authorities[df_authorities["SEMEL_YISH"] == semel_yish]
    if not match_authorities.empty:
        cluster = match_authorities.iloc[0]["CLUSTER"]

    # Check localities
    match_localities = df_localities[df_localities["SEMEL_YISH"] == semel_yish]
    if not match_localities.empty:
        cluster = match_localities.iloc[0]["CLUSTER"]

    # Check statistical areas if STAT11 is provided
    if stat11:
        match_areas = df_areas[
            (df_areas["SEMEL_YISH"] == semel_yish) & (df_areas["STAT11"] == stat11)
        ]
        if not match_areas.empty:
            cluster = match_areas.iloc[0]["CLUSTER"]

    # If a match was found in any of the checks, update the feature
    if cluster is not None:
        feature["properties"]["CLUSTER"] = cluster
        matched_features.append(feature)

geojson_data["features"] = matched_features

with open("output/updated_statistical_areas.geojson", "w") as f:
    ujson.dump(geojson_data, f, ensure_ascii=False)
