import matplotlib.pyplot as plt
import numpy as np


def point_cloud_to_2d_gird(input_xyz_file, output_txt_file, depth, altitude, visualization):
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
        coord = (float(line_string[0]), float(line_string[1]), float(line_string[2]))

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
    f.write('%f\n' % x_res)
    f.write('%f\n' % y_res)

    for x in range(width):
        for y in range(width):
            f.write('%d %d %d\n' % (x, y, map[x][y]))
    f.close()

    if visualization:
        plt.figure(1)
        plt.scatter(x_base, y_base, color='blue')
        plt.scatter(x_filtered, y_filtered, color='red')

        numpy_map = np.array(map)
        plt.figure(2)
        plt.imshow(np.rot90(numpy_map), interpolation='nearest')
        plt.grid(True)

        plt.show()


if __name__ == '__main__':
    input_file = 'paradisecity.xyz'
    output_file = 'gridmap.txt'
    max_depth = 7
    height_threshold = 1181  # (inches, ~ 30 meters)
    visualize = True

    point_cloud_to_2d_gird(input_file, output_file, max_depth, height_threshold, visualize)
