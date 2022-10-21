import geopandas as gpd
from pyproj import Geod


def get_geodesic_area(polygon):
    # specify a named ellipsoid
    geod = Geod(ellps="WGS84")
    
    # abs() is used to return only positive areas. 
    # A negative area may be returned depending on the winding direction of the polygon.
    area = abs(geod.geometry_area_perimeter(polygon)[0])
    
    return area


def get_data(data_path: str) -> gpd.GeoDataFrame:
    # import data (filtered building footprints Microsoft)
    gdf = gpd.read_file(data_path)
    gdf.columns = gdf.columns.str.lower()

    gdf["area_m2"] = gdf.geometry.apply(get_geodesic_area)
    gdf["area_km2"] = gdf["area_m2"] / 1000

    subset = gdf.sample(2500)

    return subset
