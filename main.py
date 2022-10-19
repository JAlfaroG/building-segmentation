
import os
import json
import argparse
import webbrowser

from data_processing import get_data
from create_aoi import get_aoi, get_building_counts
from create_map import get_map


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('conf', type=str)
    parser.add_argument('--radius', type=int, help='Radius around POI in meters', default=1000)
    parser.add_argument('--browser', action='store_true', help='Flag to open the map in a new browser tab.')
    args = parser.parse_args()

    conf = json.load(open(f'{args.conf}', 'r'))

    subset = get_data(conf["data_path"])

    esa_poi = conf["esa_poi"]

    circle_poly = get_aoi(esa_poi, args.radius)
    buildings_within_area = get_building_counts(circle_poly, subset)

    m = get_map(esa_poi, subset, buildings_within_area, circle_poly)

    save_dir = './outputs'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    output_file = os.path.join(save_dir, "esa-buildings.html")
    m.save(output_file)

    if args.browser:
        webbrowser.open(output_file, new=2)


if __name__ == "__main__":
    main()
