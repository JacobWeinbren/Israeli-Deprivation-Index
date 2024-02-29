import pandas as pd
import json
import re

# Load the CSV file and rename columns directly
df = pd.read_csv("Socio-Economical 2019.csv").rename(
    columns={
        "town_code": "SEMEL_YISH",
        "STAT19": "STAT11",
        "SocioRank19": "RANK_2019",
        "town_hebrew": "SHEM_YISHU",
    }
)

# Load the GeoJSON file
with open("statistical_areas.geojson", "r") as f:
    geojson_data = json.load(f)


# Function to remove all spaces and non-Hebrew characters
def clean_hebrew(input_string):
    return re.sub(r"[^\u0590-\u05FF]", "", str(input_string))


# Preprocess SHEM_YISHU in DataFrame for efficient matching
df["SHEM_YISHU_CLEANED"] = df["SHEM_YISHU"].apply(clean_hebrew)

# Initialize an empty list to hold features with matches
matched_features = []

for feature in geojson_data["features"]:
    # Extract properties for matching
    semel_yish = feature["properties"]["SEMEL_YISH"]
    stat11 = feature["properties"].get("STAT11")
    shem_yishu = clean_hebrew(feature["properties"]["SHEM_YISHU"])

    # Attempt to find the corresponding row in the DataFrame
    match = df.loc[
        ((df["SEMEL_YISH"] == semel_yish) & (df["STAT11"] == stat11))
        | (df["SHEM_YISHU_CLEANED"] == shem_yishu),
        ["RANK_2019"],
    ]

    # If there's a match, update the GeoJSON feature properties
    if not match.empty:
        feature["properties"]["RANK_2019"] = match.iloc[0]["RANK_2019"]
        matched_features.append(feature)

# Replace the original features with the matched features
geojson_data["features"] = matched_features

# Write the updated GeoJSON to a new file
with open("updated_statistical_areas.geojson", "w") as f:
    json.dump(geojson_data, f, ensure_ascii=False)
