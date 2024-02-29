import pandas as pd
import json
import re


# Function to remove all spaces and non-Hebrew characters
def clean_hebrew(input_string):
    return re.sub(r"[^\u0590-\u05FF]", "", str(input_string))


# Function to load Excel files for authorities and localities
def load_excel(file_path, code_col_idx, cluster_col_idx, start_row):
    df = pd.read_excel(
        file_path,
        usecols=[code_col_idx, cluster_col_idx],
        skiprows=start_row - 1,
        header=None,
    )
    df.columns = ["SEMEL_YISH", "CLUSTER"]
    return df


# Specialized function for loading the areas.xlsx file, including STAT11
def load_areas_excel(file_path, code_col_idx, stat_col_idx, cluster_col_idx, start_row):
    df = pd.read_excel(
        file_path,
        usecols=[code_col_idx, stat_col_idx, cluster_col_idx],
        skiprows=start_row - 1,
        header=None,
    )
    df.columns = ["SEMEL_YISH", "STAT11", "CLUSTER"]
    return df


# Load authorities and localities
df_authorities = load_excel("authorities.xlsx", 1, 6, 11)
df_localities = load_excel("localities.xlsx", 5, 12, 10)

# Load areas with STAT11
df_areas = load_areas_excel("areas.xlsx", 0, 2, 6, 9)

# Check if 382 exists in df_localities for SEMEL_YISH
exists_382 = df_localities["SEMEL_YISH"].astype(str).str.contains("382").any()
print(f"Does 382 exist in localities for SEMEL_YISH? {exists_382}")

# Load the GeoJSON file
with open("statistical_areas.geojson", "r") as f:
    geojson_data = json.load(f)

# Initialize an empty list to hold features with matches
matched_features = []

for feature in geojson_data["features"]:
    # Use SEMEL_YISH for matching
    semel_yish = feature["properties"].get("SEMEL_YISH")
    stat11 = feature["properties"].get("STAT11")

    # Attempt to find the corresponding row in each DataFrame using SEMEL_YISH and STAT11 for areas
    match = pd.concat(
        [
            df_authorities[
                df_authorities["SEMEL_YISH"]
                .apply(pd.to_numeric, errors="coerce")
                .fillna(0)
                .astype(int)
                == int(semel_yish)
            ],
            df_localities[
                df_localities["SEMEL_YISH"]
                .apply(pd.to_numeric, errors="coerce")
                .fillna(0)
                .astype(int)
                == int(semel_yish)
            ],
            df_areas[
                (
                    df_areas["SEMEL_YISH"]
                    .apply(pd.to_numeric, errors="coerce")
                    .fillna(0)
                    .astype(int)
                    == int(semel_yish)
                )
                & (
                    df_areas["STAT11"]
                    .apply(pd.to_numeric, errors="coerce")
                    .fillna(0)
                    .astype(int)
                    == int(stat11)
                )
            ],
        ],
        ignore_index=True,
    )

    # If there's a match, update the GeoJSON feature properties
    if not match.empty:
        feature["properties"]["CLUSTER"] = match.iloc[0]["CLUSTER"]
        matched_features.append(feature)

# Replace the original features with the matched features
geojson_data["features"] = matched_features

# Write the updated GeoJSON to a new file
with open("updated_statistical_areas.geojson", "w") as f:
    json.dump(geojson_data, f, ensure_ascii=False)
