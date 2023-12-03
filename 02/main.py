import sys

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    data = parse_input(input_text)
    max_values_per_game = get_max_values_per_game(data)
    solve_problem_1(max_values_per_game)
    solve_problem_2(max_values_per_game)


def solve_problem_1(max_values_per_game):
    games_where_condition_is_ok = []
    for i, max_values in enumerate(max_values_per_game):
        i += 1 # games are 1-indexed, i is 0-indexed. Maybe we should have stored the game index in the raw data...
        if max_values["red"] <= 12 and max_values["green"] <= 13 and max_values["blue"] <= 14:
            games_where_condition_is_ok.append(i)
    print(sum(games_where_condition_is_ok))


def solve_problem_2(max_values_per_game):
    total_power = 0
    for max_values in max_values_per_game:
        total_power += max_values["red"] * max_values["green"] * max_values["blue"]
    print(total_power)


def get_max_values_per_game(data):
    max_values_per_game = []
    for game in data:
        max_values = {"red": 0, "green": 0, "blue": 0}
        for set_data in game:
            for color in max_values:
                if color in set_data:
                    if set_data[color] > max_values[color]:
                        max_values[color] = set_data[color]
        max_values_per_game.append(max_values)
    return max_values_per_game


def parse_input(input_text):
    """Parse the input string into a usable format.
    [
        [
            {"red": 4, "blue": 3, "green": 2},
            {"red": ...},
            ...
        ],
        [
            {...}
        ],
        ...
    ]
    """
    lines = input_text.split('\n')
    arr = []
    for line in lines:
        arr.append(parse_line(line))
    return arr


def parse_line(line):
    """Parse a line string into a usable format.
    [
        {"red": 4, "blue": 3, "green": 2},
        {"red": ...},
        ...
    ]
    """
    # Get rid of the "Game 1" header, we have no useful data there
    line_data = line.split(':')[1]
    set_strings = line_data.split(';')
    arr = []
    for set_string in set_strings:
        arr.append(parse_set(set_string))
    return arr


def parse_set(set_string):
    """Parse a set string into a usable format.
    {"red": 4, "blue": 3, "green": 2}
    """
    set_data = {}
    pair_strings = set_string.split(',')
    for pair_string in pair_strings:
        pair_data = pair_string.split(' ')
        set_data[pair_data[2]] = int(pair_data[1])
    
    return set_data


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