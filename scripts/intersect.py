import geopandas as gpd
import sys


def intersect_geojson(file1, file2, output_file):
    # Load the GeoJSON files
    print(f"Loading GeoJSON files: {file1} and {file2}")
    gdf1 = gpd.read_file(file1)
    gdf2 = gpd.read_file(file2)

    # Perform the intersection
    print("Performing intersection...")
    intersection = gpd.overlay(gdf1, gdf2, how="intersection")

    # Save the result to a new GeoJSON file
    intersection.to_file(output_file, driver="GeoJSON", decimal=6)


if __name__ == "__main__":
    file1 = "output/updated_statistical_areas.geojson"
    file2 = "data/israel-palestine.geojson"
    output_file = "output/merged.geojson"

    intersect_geojson(file1, file2, output_file)
