import sys
import re
import math
import itertools


POSITION_START = 'AAA'
POSITION_END = 'ZZZ'

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    data = parse_input(input_text)

    print('Problem 1:', solve_problem_1(data))
    print('Problem 2:', solve_problem_2(data))


def solve_problem_1(data):
    if POSITION_START not in data['graph']:
        return -1
    num_steps = 0
    done = False
    position_now = POSITION_START
    while not done:
        for direction in data['rules']:
            num_steps += 1
            position_now = data['graph'][position_now][direction]
            if position_now == POSITION_END:
                done = True
                break
    return num_steps


def solve_problem_2(data):
    '''Solve problem 2 on this particular input type.
    This is the struct we get from precomputations:
        {'AAA': {'loop_size': inf, 'times_to_Z': [14893]},
        'BJA': {'loop_size': inf, 'times_to_Z': [16579]},
        'GFA': {'loop_size': inf, 'times_to_Z': [12083]},
        'LQA': {'loop_size': inf, 'times_to_Z': [13207]},
        'SGA': {'loop_size': inf, 'times_to_Z': [22199]},
        'SVA': {'loop_size': inf, 'times_to_Z': [20513]}}
    This function can solve for any number of times_to_Z in an element,
    however it is not generalized to work for other loop sized than infinity.
    Python 3.9 or greater is required for math.lcm().
    '''
    precomputations = precompute_loops(data)
    times_to_Z = []
    for _, val in precomputations.items():
        times_to_Z.append(val['times_to_Z'])
    all_possibilities = list(list(tup) for tup in itertools.product(*times_to_Z))
    possible_times = []
    for possibility in all_possibilities:
        possible_times.append(math.lcm(*possibility))
    
    return min(possible_times)


def precompute_loops(data):
    precomputations = {}
    for key in data['graph']:
        if key[2] != 'A':
            continue
        precomputations[key] = precompute_loop(data['rules'], data['graph'], key)
    return precomputations


def precompute_loop(rules, graph, start):
    position_now = start
    num_steps = 0
    times_to_Z = []
    done = False
    visited = {} # {'AAA': [2, 5, 8] # the indexes of the instruction in rules this was visited on, ...}
    while not done:
        for direction in rules:
            num_steps += 1
            position_now = graph[position_now][direction]
            if position_now[2] == 'Z':
                times_to_Z.append(num_steps)
            if position_now == start and num_steps % len(rules) == 0:
                done = True
                break
            if position_now in visited:
                if num_steps % len(rules) in visited[position_now]:
                    num_steps = float('inf')
                    done = True
                    break
                visited[position_now].append(num_steps % len(rules))
            else:
                visited[position_now] = [num_steps % len(rules)]
    return {'loop_size': num_steps, 'times_to_Z': times_to_Z}


def parse_input(input_text):
    data = {'graph': {}}
    lines = input_text.split('\n')
    data['rules'] = lines[0]
    for line in lines[2:]:
        words = list(re.findall(r'[0-9a-zA-Z]+', line))
        data['graph'][words[0]] = {'L': words[1], 'R': words[2]}
    return data


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