import sys
import numpy as np
import re

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    matrix, (areas, stars) = parse_input(input_text)
    print("Problem 1", solve_problem_1(areas))
    print("Problem 2", solve_problem_2(stars))


def solve_problem_1(areas):
    numbers = []
    for _, area in areas.items():
        flattened_area = ''.join(np.array(area["area"]).flatten().tolist())
        if re.match(r".*[^\d\.].*", flattened_area):
            numbers.append(area["number"])
    return sum(numbers)


def solve_problem_2(stars):
    result = 0;
    for _, star in stars.items():
        if len(star) != 2:
            continue
        result += star[0] * star[1]
    return result


def parse_input(input_text):
    lines = input_text.split('\n')
    line_arrays = []
    for line in lines:
        line_arrays.append(list(line))
    matrix = np.matrix(line_arrays)
    return matrix, get_number_areas_and_stars(matrix, get_numbers_indeces(line_arrays))


def get_number_areas_and_stars(matrix, numbers):
    areas = {}
    num_rows, num_cols = matrix.shape
    stars = {}
    for coords, number in numbers.items():
        area_coords = (
            (
                max(coords[0][0] - 1, 0),
                max(coords[0][1] - 1, 0)
            ),
            (
                min(coords[1][0] + 1, num_rows - 1),
                min(coords[1][1] + 1, num_cols - 1)
            )
        )
        value = {
            "number": number,
            "area": matrix[area_coords[0][0]:(area_coords[1][0] + 1),
                           area_coords[0][1]:(area_coords[1][1] + 1)]
        }
        areas[area_coords] = value

        # save any neighbouring '*' indeces\
        iterator = np.nditer(value["area"], flags=['multi_index'])
        for character in iterator:
            if character == '*':
                coords = (area_coords[0][0] + iterator.multi_index[0],
                          area_coords[0][1] + iterator.multi_index[1])
                if coords not in stars:
                    stars[coords] = []
                stars[coords].append(number)
    return areas, stars


def get_numbers_indeces(line_arrays):
    numbers = {}
    for line_idx, line_array in enumerate(line_arrays):
        line = ''.join(line_array)
        for match in re.finditer(r'\d+', line):
            numbers[((line_idx, match.start()), (line_idx, match.end() - 1))] = int(match.group())
    return numbers


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