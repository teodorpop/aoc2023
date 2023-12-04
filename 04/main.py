import sys
import re
import functools

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    data = parse_input(input_text)

    print(solve_problem_1(data))
    print(solve_problem_2(data))


def solve_problem_1(data):
    score = 0
    for _, numbers in data.items():
        card_score = 0
        for number in get_winning_numbers(numbers["actual"], numbers["winning"]):
            if card_score == 0:
                card_score = 1
            else:
                card_score *= 2 
        score += card_score
    return score


def solve_problem_2(data):
    num_copies = {}
    num_cards = 0

    for card in list(data):
        num_copies[card] = 1

    for card, numbers in data.items():
        num_cards += num_copies[card]
        winning_numbers = get_winning_numbers(numbers["actual"], numbers["winning"])
        for next_card in range(card + 1, card + 1 + len(winning_numbers)):
            if next_card <= len(data):
                num_copies[next_card] = num_copies[next_card] + num_copies[card]

    return sum(num_copies.values())


def get_winning_numbers(actual, winning):
    winning_numbers = []
    for number in actual:
        if number in winning:
            winning_numbers.append(number)
    return winning_numbers


def parse_input(input_text):
    """Parses input file into an easily useable data structure:
    {
        1: {
            "winning": [41, 48, 83, 86, 17],
            "actual" : [83, 86, 6, 31, 17, 9, 48, 53]
        },
        2: {...}, ...
    }
    """
    lines = input_text.split('\n')

    data = {}
    
    for line in lines:
        tokens = re.split(r': | \| ', line)
        card_no = int(re.findall(r'\d+', tokens[0])[0])
        winning = list(map(int, re.findall(r'\d+', tokens[1])))
        actual = list(map(int, re.findall(r'\d+', tokens[2])))
        data[card_no] = {
            "winning": winning,
            "actual": actual
        }

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