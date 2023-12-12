import sys
import math

CHARACTER_MAPPINGS = {'|': {'print_unvisited': '│', 'print_loop': '┃', 'N': 1, 'S': 1, 'E': 0, 'W': 0},
                      '-': {'print_unvisited': '─', 'print_loop': '━', 'N': 0, 'S': 0, 'E': 1, 'W': 1},
                      'L': {'print_unvisited': '└', 'print_loop': '┗', 'N': 1, 'S': 0, 'E': 1, 'W': 0},
                      'J': {'print_unvisited': '┘', 'print_loop': '┛', 'N': 1, 'S': 0, 'E': 0, 'W': 1},
                      '7': {'print_unvisited': '┐', 'print_loop': '┓', 'N': 0, 'S': 1, 'E': 0, 'W': 1},
                      'F': {'print_unvisited': '┌', 'print_loop': '┏', 'N': 0, 'S': 1, 'E': 1, 'W': 0},
                      '.': {'print_unvisited': 'ˑ', 'print_loop': '·', 'N': 0, 'S': 0, 'E': 0, 'W': 0},
                      'S': {'print_unvisited': 'S', 'print_loop': 'S', 'N': 1, 'S': 1, 'E': 1, 'W': 1}}
GROUND = '.'
START = 'S'

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    data = parse_input(input_text)
    print('Problem 1:', solve_problem_1(data))
    print('Problem 2:', solve_problem_2(data))
    print_map_prety(data)


# 6696 is too low
def solve_problem_1(data):
    line_start, col_start = get_start(data)

    bfs(data, line_start, col_start)
    
    max_steps = 0
    for line in data:
        for cell in line:
            if 'distance' in cell and cell['distance'] > max_steps:
                max_steps = cell['distance']
    return max_steps


def get_neighbours(data, line, col):
    neighbours = []
    if CHARACTER_MAPPINGS[data[line][col]['data']]['N'] and line > 0 and \
            CHARACTER_MAPPINGS[data[line-1][col]['data']]['S']:
        neighbours.append((line - 1, col))
    if CHARACTER_MAPPINGS[data[line][col]['data']]['S'] and line < len(data) - 1 and \
            CHARACTER_MAPPINGS[data[line+1][col]['data']]['N']:
        neighbours.append((line + 1, col))
    if CHARACTER_MAPPINGS[data[line][col]['data']]['E'] and col < len(data[0]) - 1 and \
            CHARACTER_MAPPINGS[data[line][col+1]['data']]['W']:
        neighbours.append((line, col + 1))
    if CHARACTER_MAPPINGS[data[line][col]['data']]['W'] and col > 0 and \
            CHARACTER_MAPPINGS[data[line][col-1]['data']]['E']:
        neighbours.append((line, col - 1))
    return neighbours


def bfs(data, line, col, num_steps = math.inf):
    to_visit = [(line, col, 0)]
    i = 0

    while len(to_visit) and num_steps > i:
        (line, col, step) = to_visit.pop(0)

        if 'visited' in data[line][col] and data[line][col]['visited']:
            continue
        if data[line][col]['data'] == GROUND:
            continue

        i += 1

        data[line][col]['visited'] = True
        data[line][col]['distance'] = step
        for neighbour in get_neighbours(data, line, col):
            to_visit.append((neighbour[0], neighbour[1], step + 1))


def get_start(data):
    for line, line_data in enumerate(data):
        for col, cell in enumerate(line_data):
            if cell['data'] == START:
                return line, col
    return -1, -1


def solve_problem_2(data):
    inside = 0
    
    replace_start_with_pipe(data)

    for line, line_data in enumerate(data):
        for col, cell in enumerate(line_data):
            if is_inside(data, line, col):
                inside += 1
                cell['inside'] = True
    return inside


def replace_start_with_pipe(data):
    line_start, col_start = get_start(data)
    N, S, E, W = (False,)*4
    for neighbour in get_neighbours(data, line_start, col_start):
        if neighbour[0] < line_start:
            N = True
        if neighbour[0] > line_start:
            S = True
        if neighbour[1] < col_start:
            W = True
        if neighbour[1] > col_start:
            E = True
    if N and S:
        data[line_start][col_start]['data'] = "|"
    if N and E:
        data[line_start][col_start]['data'] = "L"
    if N and W:
        data[line_start][col_start]['data'] = "J"
    if E and W:
        data[line_start][col_start]['data'] = "-"
    if S and E:
        data[line_start][col_start]['data'] = "F"
    if S and W:
        data[line_start][col_start]['data'] = "7"


def is_inside(data, line, col):
    if 'visited' in data[line][col]:
        return False
    num_N = 0
    num_S = 0
    ray_right = data[line][col:]
    for cell in ray_right:
        if 'visited' not in cell:
            continue
        num_N += CHARACTER_MAPPINGS[cell['data']]['N']
        num_S += CHARACTER_MAPPINGS[cell['data']]['S']
    return num_N % 2 == 1 and num_S % 2 == 1


def print_map_prety(map):
    for line in map:
        for cell in line:
            if 'inside' in cell:
                print('\033[31;42m', end='')
            print(CHARACTER_MAPPINGS[cell['data']]['print_loop' if 'visited' in cell else 'print_unvisited'], end='')
            print('\033[0m', end='')
        print()


def parse_input(input_text):
    data = []
    for line in input_text.split('\n'):
        l = []
        for c in line:
            l.append({'data': c})
        data.append(l)
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