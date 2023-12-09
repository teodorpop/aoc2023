import sys

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    data = parse_input(input_text)
    print('Problem 1:', solve_problem_1(data))
    print('Problem 2:', solve_problem_2(data))


def solve_problem_1(data):
    extrapolations = []
    for history in data:
        extrapolations.append(extrapolate(history))
    return sum(extrapolations)


def solve_problem_2(data):
    extrapolations = []
    for history in data:
        extrapolations.append(extrapolate_beginning(history))
    return sum(extrapolations)

def get_next_line(line):
    new_line = []
    for i in range(len(line) - 1):
        new_line.append(line[i + 1] - line[i])
    return new_line


def extrapolate(history):
    new_line = get_next_line(history)
    all_zeroes = new_line.count(0) == len(new_line)
    if all_zeroes:
        return history[len(history) - 1]
    return history[len(history) - 1] + extrapolate(new_line)


def extrapolate_beginning(history):
    new_line = get_next_line(history)
    all_zeroes = new_line.count(0) == len(new_line)
    if all_zeroes:
        return history[0]
    return history[0] - extrapolate_beginning(new_line)


def parse_input(input_text):
    data = []
    for line_string in input_text.split('\n'):
        line_data = []
        for num in line_string.split(' '):
            line_data.append(int(num))
        data.append(line_data)
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