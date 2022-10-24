import folium
import geopandas as gpd


def get_map(esa_poi: list, gdf: gpd.GeoDataFrame, building_counts: int, area_poly):
    """
    Creates a folium map centered at 'esa_poi' with displaying the buildings (polygons) of the given GeoDataFrame.

    It will also display the selected area of interest ('area_poly') with the building counts within it.
    """
    print("generating map...")
    print(f"location: {esa_poi}")
    print(f"found {building_counts:,d} buildings within selected area")
    print('-' * 100)


    if type(esa_poi) is not list:
        esa_poi = [esa_poi.centroid.y, esa_poi.centroid.x]

    m = folium.Map(location=esa_poi, zoom_start=13, tiles='cartodbpositron')

    # draws main map and shows coordinates at point
    folium.GeoJson(gdf).add_to(m)
    folium.LatLngPopup().add_to(m)

    # add the selected area of interest
    sim_geo = gpd.GeoSeries(area_poly) #.simplify(tolerance=0.001)
    geo_j = sim_geo.to_json()

    folium.GeoJson(
        geo_j,
        style_function=lambda x: {'fillColor': 'orange'}
        ).add_to(m)

    folium.Marker(
        location=esa_poi,
        popup=f"{building_counts:,d} buildings within area."
        ).add_to(m)

    return m
    