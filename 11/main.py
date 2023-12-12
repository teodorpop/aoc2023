import sys
from collections import OrderedDict
import numpy

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    galaxies_per_line, galaxies_per_col = parse_input(input_text)
    print('Problem 1:', solve_problem_1(galaxies_per_line, galaxies_per_col))
    print('Problem 2:', solve_problem_2(galaxies_per_line, galaxies_per_col))


def solve_problem_1(galaxies_per_line, galaxies_per_col):
    return dilate_and_measure_distances(galaxies_per_line, galaxies_per_col, 2)


def solve_problem_2(galaxies_per_line, galaxies_per_col):
    return dilate_and_measure_distances(galaxies_per_line, galaxies_per_col, 1000000)


def dilate_and_measure_distances(galaxies_per_line, galaxies_per_col, dilation_factor = 2):
    '''In O(number of galaxies) :)'''
    galaxies_per_line = numpy.copy(galaxies_per_line)
    galaxies_per_col = numpy.copy(galaxies_per_col)
    dilate_space(galaxies_per_line, dilation_factor=dilation_factor)
    dilate_space(galaxies_per_col, dilation_factor=dilation_factor)
    sum_manhattan_x = sum_manhattan_axis(galaxies_per_line[1:, :],
                                         galaxies_per_line[0, 0] * galaxies_per_line[0, 1],
                                         galaxies_per_line[0, 1])
    sum_manhattan_y = sum_manhattan_axis(galaxies_per_col[1:, :],
                                         galaxies_per_col[0, 0] * galaxies_per_col[0, 1],
                                         galaxies_per_col[0, 1])
    return sum_manhattan_x + sum_manhattan_y


def sum_manhattan_axis(arr, propagated_total_distance_from_border = 0, num_propagated_galaxies = 0):
    distance = arr[0, 0] * arr[0, 1] * num_propagated_galaxies - propagated_total_distance_from_border * arr[0, 1]
    if arr.size == 2:
        return distance
    return distance + sum_manhattan_axis(arr[1:, :],
                                         propagated_total_distance_from_border + arr[0, 0] * arr[0, 1],
                                         num_propagated_galaxies + arr[0, 1])


def dilate_space(galaxies_per_axis, propagated_dilation = 0, dilation_factor = 3):
    previous_position = galaxies_per_axis[0, 0]
    galaxies_per_axis[0, 0] += propagated_dilation
    if len(galaxies_per_axis) == 1:
        return
    propagated_dilation += (galaxies_per_axis[1, 0] - previous_position - 1) * (dilation_factor - 1)
    dilate_space(galaxies_per_axis[1:], propagated_dilation, dilation_factor)
    return


def parse_input(input_text):
    lines = []
    for line in input_text.split('\n'):
        lines.append([c for c in line])
    arr = numpy.array(lines)
    galaxies_per_line = get_galaxies_per_line(arr)
    galaxies_per_col = get_galaxies_per_line(arr.T)
    return galaxies_per_line, galaxies_per_col


def get_galaxies_per_line(arr):
    galaxies_per_line = []
    for i, line in enumerate(arr):
        num_galaxies = (line == '#').sum()
        if num_galaxies:
            galaxies_per_line.append((i, num_galaxies))
    return numpy.array(galaxies_per_line)


def validate_run():
    if not len(sys.argv) == 2:
        print("How to run: python3 main.py <input_file>")
        return False
    return True


def read_input(file_name):
    file = open(file_name, "r")
    content = file.read()
    file.close()
    return content


if __name__ == "__main__":
    main()