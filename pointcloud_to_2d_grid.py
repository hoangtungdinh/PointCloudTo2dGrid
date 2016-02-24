import math
import random

import matplotlib.pyplot as plt
import numpy as np


def valid_pair(map, resolution, origin, destination):
    if map[origin[0]][origin[1]] == 1:
        return False

    if map[destination[0]][destination[1]] == 1:
        return False

    point_origin = (origin[0]*resolution[0], origin[1]*resolution[1])
    point_destination = (destination[0]*resolution[0], destination[1]*resolution[1])
    distance = math.sqrt((point_origin[0] - point_destination[0])**2 + (point_origin[1] - point_destination[1])**2)
    width = len(map)
    min_distance = math.sqrt((width*resolution[0])**2 + (width*resolution[1])**2) / 2 # half of the diagonal path

    if distance < min_distance:
        return False

    return True


def point_cloud_to_2d_gird(input_xyz_file, unit_conversion, output_txt_file, depth, altitude, scatterplot=False, gridplot=False, random_pairs=0):
    points = []

    x_min = float('inf')
    x_max = float('-inf')
    y_min = float('inf')
    y_max = float('-inf')

    x_filtered = []
    y_filtered = []
    x_base = []
    y_base = []

    file = open(input_xyz_file, 'r')

    for line in file:
        line_string = line.split()
        coord = (float(line_string[0]) * unit_conversion, float(line_string[1]) * unit_conversion, float(line_string[2]) * unit_conversion)

        if coord[0] < x_min:
            x_min = coord[0]

        if coord[0] > x_max:
            x_max = coord[0]

        if coord[1] < y_min:
            y_min = coord[1]

        if coord[1] > y_max:
            y_max = coord[1]

        if coord[2] > altitude:
            points.append(coord)
            x_filtered.append(coord[0])
            y_filtered.append(coord[1])

        x_base.append(coord[0])
        y_base.append(coord[1])

    file.close()

    width = 2 ** depth
    map = [[0 for x in range(width)] for x in range(width)]

    x_diff = x_max - x_min
    y_diff = y_max - y_min
    x_res = x_diff / width
    y_res = y_diff / width

    for coord in points:
        coord_x = (coord[0] - x_min) / x_res
        coord_y = (coord[1] - y_min) / y_res
        map[int(coord_x)][int(coord_y)] = 1

    f = open(output_txt_file, 'w')
    f.write('%d\n' % depth)
    f.write('%d\t%d\n' % (round(x_res), round(y_res)))

    for x in range(width):
        for y in range(width):
            f.write('%d %d %d\n' % (x, y, map[x][y]))
    f.close()

    if random_pairs > 0:
        pairs = []
        random.seed(1)
        for i in range(random_pairs):
            row_origin = random.randrange(width)
            col_origin = random.randrange(width)
            row_destination = random.randrange(width)
            col_destination = random.randrange(width)
            while not valid_pair(map, (round(x_res), round(y_res)), (row_origin, col_origin), (row_destination, col_destination)):
                row_origin = random.randrange(width)
                col_origin = random.randrange(width)
                row_destination = random.randrange(width)
                col_destination = random.randrange(width)
            pairs.append((row_origin*round(x_res), col_origin*round(y_res), row_destination*round(x_res), col_destination*round(y_res)))
        pairFile = open('pairs.txt', 'w')
        for pair in pairs:
            pairFile.write('%d\t%d\t%d\t%d\n' % (pair[0], pair[1], pair[2], pair[3]))
        pairFile.close()

    if scatterplot:
        plt.figure(1)
        plt.scatter(x_base, y_base, color='blue')
        plt.scatter(x_filtered, y_filtered, color='red')

    if gridplot:
        numpy_map = np.array(map)
        plt.figure(2)
        plt.imshow(np.rot90(numpy_map), interpolation='nearest')
        plt.grid(True)

    if scatterplot or gridplot:
        plt.show()


if __name__ == '__main__':
    max_depth = 7
    height_threshold = 30000  # (millimeters)

    # data store in inches ~ 25,4 millimeters
    point_cloud_to_2d_gird('sampledparadisecity.xyz', 25.4, 'gridmap.txt', max_depth, height_threshold, False, True, 0)
