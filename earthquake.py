from geopy.distance import geodesic
import requests_cache
from requests import get as get_request
import csv
from csv_parser import parser


URI = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"
requests_cache.install_cache(cache_name='usgs_cache', backend='sqlite', expire_after=300)


def earthquakes():

    r = get_request(URI)
    feature = r.json().get('features', [])

    for f in feature:

        place = f['properties']['title']
        longitude = f['geometry']['coordinates'][0]
        latitude = f['geometry']['coordinates'][1]
        coords_2 = (latitude, longitude)
        distance = geodesic(coords_1, coords_2).km
        target = [place, str(int(distance))]

        with open(r'raw_earthquakes.csv', 'a') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(target)


if __name__ == "__main__":
    try:
        print('Enter a latitude value between -90 and 90:')
        source_latitude = float(input())
        print('Enter a longitude value between -180 and 180:')
        source_longitude = float(input())
        coords_1 = (source_latitude, source_longitude)
        earthquakes()
        parser()
    except Exception as exc:
        print('Please input float number for latitude from -90 to 90 and for longitude from -180 to 180')




