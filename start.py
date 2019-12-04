from geopy.distance import geodesic
import requests_cache
from requests import get as get_request
import csv
import os


USGS_URI = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

requests_cache.install_cache(cache_name='usgs_cache', backend='sqlite', expire_after=300)


def earthquakes():

    r = get_request(USGS_URI)
    feature = r.json().get('features', [])

    for f in feature:

        place = f['properties']['title']
        longitude = f['geometry']['coordinates'][0]
        latitude = f['geometry']['coordinates'][1]
        coords_2 = (latitude, longitude)
        distance = geodesic(coords_1, coords_2).km
        target = [place, str(int(distance))]

        with open(r'quakes.csv', 'a') as ff:
            writer = csv.writer(ff)
            writer.writerow(target)

    with open('quakes.csv') as sample, open('sorted.csv', "w") as out:
        csv1 = csv.reader(sample)
        header = next(csv1, None)
        csv_writer = csv.writer(out)
        if header:
            csv_writer.writerow(header)
        csv_writer.writerows(sorted(csv1, key=lambda x: int(x[1])))

    with open('sorted.csv', 'r') as infile:
        with open('change.csv', 'w') as outfile:
            reader = csv.reader(infile, delimiter=',')
            writer = csv.writer(outfile, delimiter=',')
            for row in reader:
                new_row = [row[0], '||']
                new_row += row[1:]
                writer.writerow(new_row)

    with open('change.csv', 'r') as input:
        lines = input.readlines()

    conversion = '",'
    newtext = ' '
    outputLines = []
    for line in lines:
        temp = line[:]
        for c in conversion:
            temp = temp.replace(c, newtext)
        outputLines.append(temp)

    with open('done.csv', 'w') as output:
        for line in outputLines:
            output.write(line + "\n")

    with open('done.csv') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)

        quake_list = rows[2:21]

    for i in range(len(quake_list)):
        if i % 2 == 0:
            stri = str(quake_list[i])
            print(stri[2:-2])


if __name__ == "__main__":
    print('podaj szerokość')
    source_latitude = float(input())
    print('podaj długosc')
    source_longtitude = float(input())
    coords_1 = (source_latitude, source_longtitude)
    earthquakes()

    os.remove('quakes.csv')
    os.remove('sorted.csv')
    os.remove('change.csv')
    os.remove('done.csv')

