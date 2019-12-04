import csv
import os


def parser():

    with open('raw_earthquakes.csv') as infile, open('sorted.csv', "w") as outfile:
        csv1 = csv.reader(infile)
        header = next(csv1, None)
        csv_writer = csv.writer(outfile)
        if header:
            csv_writer.writerow(header)
        csv_writer.writerows(sorted(csv1, key=lambda x: int(x[1])))

    with open('sorted.csv', 'r') as infile:
        with open('changed.csv', 'w') as outfile:
            reader = csv.reader(infile, delimiter=',')
            writer = csv.writer(outfile, delimiter=',')
            for row in reader:
                new_row = [row[0], '||']
                new_row += row[1:]
                writer.writerow(new_row)

    with open('changed.csv', 'r') as sample:
        lines = sample.readlines()

    conversion = '",'
    new_text = ' '
    output_lines = []
    for line in lines:
        temp = line[:]
        for c in conversion:
            temp = temp.replace(c, new_text)
        output_lines.append(temp)

    with open('earthquakes.csv', 'w') as outfile:
        for line in output_lines:
            outfile.write(line)

    with open('earthquakes.csv') as outfile:
        csv_reader = csv.reader(outfile)
        rows = list(csv_reader)
        earthquake_list = rows[1:11]

    for i in range(len(earthquake_list)):
        earthquake = str(earthquake_list[i])
        print(earthquake[2:-2])

    os.remove('raw_earthquakes.csv')
    os.remove('sorted.csv')
    os.remove('changed.csv')
    os.remove('earthquakes.csv')
