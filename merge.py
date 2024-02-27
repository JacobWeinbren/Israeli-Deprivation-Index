import pandas as pd
import json

# Load the Excel file and rename columns directly
df = pd.read_excel("deprivation.xlsx", header=9).rename(
    columns={"CODE OF LOCALITY": "SEMEL_YISH", "CODE OF STATISTICAL AREA": "STAT08"}
)

print(df.columns)

# Load the GeoJSON file
with open("statistical_areas.geojson", "r") as f:
    geojson_data = json.load(f)

# Update the GeoJSON features with the deprivation data directly from the DataFrame
for feature in geojson_data["features"]:
    # Extract SEMEL_YISH and STAT08 from the feature
    semel_yish = feature["properties"]["SEMEL_YISH"]
    stat08 = feature["properties"]["STAT08"]

    # Find the corresponding row in the DataFrame
    deprivation_info = df.loc[
        (df["SEMEL_YISH"] == semel_yish) & (df["STAT08"] == stat08),
        ["RANK 2019[3] ", " CLUSTER 2019[4] "],
    ]

    # If there's a match, update the GeoJSON feature properties
    if not deprivation_info.empty:
        feature["properties"]["RANK_2019"] = deprivation_info.iloc[0]["RANK 2019[3] "]
        feature["properties"]["CLUSTER_2019"] = deprivation_info.iloc[0][
            " CLUSTER 2019[4] "
        ]

# Write the updated GeoJSON to a new file
with open("updated_statistical_areas.geojson", "w") as f:
    json.dump(geojson_data, f, ensure_ascii=False)
