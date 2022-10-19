import geopandas as gpd


def get_data(data_path: str) -> gpd.GeoDataFrame:
    # import data (filtered building footprints Microsoft)
    gdf = gpd.read_file(data_path)
    gdf.columns = gdf.columns.str.lower()

    subset = gdf.sample(25000)

    return subset
