import sys
import re
import math
import numpy

EPSILON = 0.0000001

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    data_pb1, data_pb2 = parse_input(input_text)
    print('Problem 1:', solve_problem_1(data_pb1))
    print('Problem 2:', solve_problem_2(data_pb2))


def solve_problem_1(data):
    num_solutions = []
    for pair in data:
        num_solutions.append(get_num_solutions_for_pair(pair['time'], pair['distance']))
    
    return numpy.prod(num_solutions)


def solve_problem_2(data):
    return get_num_solutions_for_pair(data['time'], data['distance'])


def get_num_solutions_for_pair(n, d):
    # For each pair of time and distance, we end up with a range of times that are
    # good for waiting. May k be any time in that range, and n the total time for the round.
    # 0...k...n
    # the distance travelled is k * (n - k) > distance desired (d)
    # -k^2 + n * k - d > 0
    # delta = n^2 - 4 * d
    # k is any positive value between ((n - sqrt(delta)) / 2), ((n + sqrt(delta)) / 2)
    # if delta < 0, there are no solutions.
    delta = n ** 2 - 4 * d
    if delta < 0:
        return 0
    return math.ceil((n + math.sqrt(delta)) / 2) - max(0, math.ceil((n - math.sqrt(delta)) / 2 + EPSILON))



def parse_input(input_text):
    lines = input_text.split('\n')
    times = list(re.findall(r'\d+', lines[0].split(':')[1]))
    distances = list(re.findall(r'\d+', lines[1].split(':')[1]))
    data_pb1 = []
    for i in range(len(times)):
        data_pb1.append({'time': int(times[i]), 'distance': int(distances[i])})
    
    data_pb2 = {'time': int(lines[0].split(':')[1].replace(' ', '')),
                'distance': int(lines[1].split(':')[1].replace(' ', ''))}
    return data_pb1, data_pb2


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