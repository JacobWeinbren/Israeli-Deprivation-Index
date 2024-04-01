# Israeli Socio-Economic Classification

## Sources

This project utilizes various data sources:

-   **Deprivation Index Ranking**: Socio-Economic Classification available [here](https://www.cbs.gov.il/en/publications/Pages/2023/socio-2019-e.aspx).
-   **Shapefile**: 2011 Statistical Areas can be found [here](https://www.cbs.gov.il/he/publications/Pages/2022/%D7%A7%D7%98%D7%9C%D7%95%D7%92.aspx).
-   **Israel / Palestine Buildings**: Open Data accessible [here](https://download.geofabrik.de/asia/israel-and-palestine.html).

## Usage

### Data Preparation

After obtaining the necessary data sources, run the following Python scripts to prepare your data:

1. `merge.py` - Merges various data sources.
2. `intersect.py` - Finds intersections between different datasets.

### Map Generation

Generate the map tiles using `tippecanoe` with the following command:

```bash
tippecanoe --output=output/israel.mbtiles --generate-ids --force --no-feature-limit --no-tile-size-limit --detect-shared-borders --coalesce-fraction-as-needed --coalesce-densest-as-needed --coalesce-smallest-as-needed --coalesce --reorder --minimum-zoom=0 --maximum-zoom=17 -x OBJECTID_1 -x OBJECTID -x SEMEL_YISH -x STAT11 -x YISHUV_STA -x SHEM_YISHU -x SHEM_YIS_1 -x Shape_Length -x Shape_Area -x osm_id -x code -x fclass -x name -x type output/merged.geojson
```
