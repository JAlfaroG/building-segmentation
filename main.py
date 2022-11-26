
import os
import json
import argparse
import webbrowser

from data_processing import get_data
from create_aoi import get_aoi, get_building_segments, get_aoi_subset, load_aoi
from create_map import get_map


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('conf', type=str)
    parser.add_argument('--radius', type=int, help='Radius around POI in meters', default=1000)
    parser.add_argument('--browser', action='store_true', help='Flag to open the map in a new browser tab.')
    parser.add_argument('--sample', type=float, help='Sample proportion.', default=0.5)
    parser.add_argument('--save', action='store_true', help="Flag to save the area of interest dataset.")
    args = parser.parse_args()

    conf = json.load(open(f'{args.conf}', 'r'))

    subset = get_data(conf["data_path"], sample_proportion=args.sample)

    esa_poi, esa_aoi = load_aoi(conf["esa_aoi_path"])

    # circle_poly = get_aoi(esa_poi, args.radius)
    buildings_within_area, poly_list = get_building_segments(esa_aoi, subset)
    gdf = get_aoi_subset(subset, poly_list)
    
    m = get_map(esa_poi, gdf, buildings_within_area, esa_aoi)

    save_dir = './outputs'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    output_file = os.path.join(save_dir, "esa-buildings.html")
    m.save(output_file)

    if args.browser:
        webbrowser.open(output_file, new=2)

    output_file = os.path.join(save_dir, "esa-buildings.geojson")
    if args.save:
        gdf.to_file(output_file, driver="GeoJSON")
        print(f"successfully saved {output_file}")    


if __name__ == "__main__":
    main()
