import sys
import pprint
import functools

CARD_SCORES = {'2': 0, '3': 1, '4': 2, '5': 3, '6': 4, '7': 5, '8': 6, '9': 7, 'T': 8, 'J': 9, 'Q': 10, 'K': 11, 'A': 12}

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    data = parse_input(input_text)
    print('Problem 1:', solve_problem_1(data))
    print('Problem 2:', solve_problem_2(data))


def solve_problem_1(data):
    data = add_hand_types(data)
    data = sorted(data, key=functools.cmp_to_key(custom_compare))
    score = 0
    for i, item in enumerate(data):
        score += (i + 1) * item['bid']
    return score


def solve_problem_2(data):
    data = add_hand_types(data, is_joker = True)
    CARD_SCORES['J'] = -1
    data = sorted(data, key=functools.cmp_to_key(custom_compare))
    score = 0
    for i, item in enumerate(data):
        score += (i + 1) * item['bid']
    return score


def add_hand_types(data, is_joker = False):
    for item in data:
        occurences = {'J': 0}
        for character in item['hand']:
            if not character in occurences:
                occurences[character] = 0
            occurences[character] += 1
        num_pairs = 0
        num_three = 0
        num_four = 0
        num_five = 0
        for k, count in occurences.items():
            if is_joker and k == 'J':
                continue
            if count == 2:
                num_pairs += 1
            if count == 3:
                num_three += 1
            if count == 4:
                num_four += 1
            if count == 5:
                num_five += 1
        if is_joker and num_four == 1 and occurences['J'] == 1:
            num_five = 1
        if is_joker and num_three == 1:
            if occurences['J'] == 2:
                num_five = 1
            if occurences['J'] == 1:
                num_four = 1
        if is_joker and num_pairs > 0:
            if occurences['J'] == 3:
                num_five = 1
            if occurences['J'] == 2:
                num_four = 1
            if occurences['J'] == 1:
                num_three = 1
                num_pairs -= 1
        if is_joker and num_pairs == 0 and num_three == 0 and num_four == 0 and num_five == 0:
            if occurences['J'] == 1:
                num_pairs = 1
            if occurences['J'] == 2:
                num_three = 1
            if occurences['J'] == 3:
                num_four = 1
            if occurences['J'] == 4:
                num_five = 1
            if occurences['J'] == 5:
                num_five = 1
        if num_five > 0:
            item['type'] = {'score': 6, 'verbose': 'five_of_a_kind'}
            continue
        if num_four > 0:
            item['type'] = {'score': 5, 'verbose': 'four_of_a_kind'}
            continue
        if num_three > 0 and num_pairs > 0:
            item['type'] = {'score': 4, 'verbose': 'full_house'}
            continue
        if num_three > 0 and num_pairs == 0:
            item['type'] = {'score': 3, 'verbose': 'three_of_a_kind'}
            continue
        if num_pairs == 2:
            item['type'] = {'score': 2, 'verbose': 'two_pair'}
            continue
        if num_pairs == 1:
            item['type'] = {'score': 1, 'verbose': 'one_pair'}
            continue
        item['type'] = {'score': 0, 'verbose': 'high_card'}

    return data



def custom_compare(item1, item2):
    if item1['type']['score'] > item2['type']['score']:
        return 1
    if item1['type']['score'] < item2['type']['score']:
        return -1
    
    for i in range(len(item1['hand'])):
        if CARD_SCORES[item1['hand'][i]] > CARD_SCORES[item2['hand'][i]]:
            return 1
        if CARD_SCORES[item1['hand'][i]] < CARD_SCORES[item2['hand'][i]]:
            return -1
    
    return 0


def parse_input(input_text):
    lines = input_text.split('\n')
    data = []
    for line in lines:
        tokens = line.split(' ')
        data.append({'hand': tokens[0], 'bid': int(tokens[1])})
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