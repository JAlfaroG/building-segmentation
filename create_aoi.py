from functools import partial
import pyproj
from shapely import geometry
from shapely.geometry import Point, Polygon
from shapely.ops import transform

import geopandas as gpd


def get_aoi(point_coord: list, radius: int) -> geometry:
    """
    Creates an area of given radius (meters) with the provided coordinates as its centroid.

    Transforms the provided coordinates to an approximately planar local reference system: WGS84
    """
    print("generating area of interest...")
    print(f"location: {point_coord}")
    print(f"radius: {radius:,d} meters")
    print('-' * 100)

    lat, lon = point_coord

    local_azimuthal_projection = "+proj=aeqd +R=6371000 +units=m +lat_0={} +lon_0={}".format(
        lat, lon
    )
    wgs84_to_aeqd = partial(
        pyproj.transform,
        pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"),
        pyproj.Proj(local_azimuthal_projection),
    )
    aeqd_to_wgs84 = partial(
        pyproj.transform,
        pyproj.Proj(local_azimuthal_projection),
        pyproj.Proj("+proj=longlat +datum=WGS84 +no_defs"),
    )

    center = Point(float(lon), float(lat))
    point_transformed = transform(wgs84_to_aeqd, center)
    buffer = point_transformed.buffer(radius)
    
    # Get the polygon with lat lon coordinates
    circle_poly = transform(aeqd_to_wgs84, buffer)

    return circle_poly


def get_building_segments(polygon: Polygon, gdf: gpd.GeoDataFrame):
    """
    Counts the polygons from the given GeoDataFrame that are within the polygon of interest.
    """
    try:
        polygons_of_interest = [poly.within(polygon) for poly in gdf.geometry]
        return sum(polygons_of_interest), polygons_of_interest
    except Exception as e:
        print(e)
        

def get_aoi_subset(gdf:gpd.GeoDataFrame, poly_list:list, filter_data=False) -> gpd.GeoDataFrame:
    filter_cols = ['name_1', 'name_2', 'geometry', 'area_m2', 'area_km2']
    gdf["within_aoi"] = poly_list

    if filter_data:
        return gdf[gdf.within_aoi == True][filter_cols]

    return gdf[gdf.within_aoi == True]


def load_aoi(shapefile):
    gdf = gpd.read_file(shapefile)

    if len(gdf) != 2:
        raise Exception("Missing polygon or point in data.")

    try:
        for geom in gdf.geometry:
            gtype = type(geom)
            if gtype == Point:
                esa_poi = geom
            elif gtype == Polygon:
                esa_aoi = geom
    except Exception as e:
        print(e)
        
    return esa_poi, esa_aoi