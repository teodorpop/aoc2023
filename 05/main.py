import sys
import pprint
import re

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    data = parse_input(input_text)

    print("Problem 1:", solve_problem_1(data))
    solve_problem_2()


def solve_problem_1(data):
    locations = []
    mappings = build_mappings(data)
    for _, mapping in mappings.items():
        locations.append(mapping['location'])
    locations.sort()
    return locations[0]


def solve_problem_2():
    return 0


def find_destination(data, src, dst, src_num):
    dst_num = src_num
    for entry in data[(src, dst)]:
        if src_num >= entry['src_start'] and src_num < entry['src_start'] + entry['range']:
            dst_num = entry['dst_start'] + src_num - entry['src_start']
    return dst_num


def build_mappings(data):
    mappings = {}
    for seed in data['seeds']:
        soil = find_destination(data, 'seed', 'soil', seed)
        fertilizer = find_destination(data, 'soil', 'fertilizer', soil)
        water = find_destination(data, 'fertilizer', 'water', fertilizer)
        light = find_destination(data, 'water', 'light', water)
        temperature = find_destination(data, 'light', 'temperature', light)
        humidity = find_destination(data, 'temperature', 'humidity', temperature)
        location = find_destination(data, 'humidity', 'location', humidity)
        mappings[seed] = {
            'soil': soil,
            'fertilizer': fertilizer,
            'water': water,
            'light': light,
            'temperature': temperature,
            'humidity': humidity,
            'location': location,
        }
    return mappings


def parse_input(input_text):
    sections = input_text.split('\n\n')
    data = {}
    for section in sections:
        if "seeds:" in section:
            data["seeds"] = list(map(int, re.findall(r'\d+', section.split(': ')[1]))) # eg [79, 14, 55, 13]
            continue
        map_lines = re.split(r' map:\n|\n', section) # eg: ['seed-to-soil', '50 98 2', '52 50 48']
        map_key_strings = map_lines[0].split('-to-')
        map_data = []
        for line in map_lines[1:]:
            line_data = list(map(int, line.split(' '))) # eg [50, 98, 2]
            map_data.append({
                'src_start': line_data[1],
                'dst_start': line_data[0],
                'range': line_data[2]
            }) 
        data[(map_key_strings[0], map_key_strings[1])] = map_data # eg: {('seed', 'soil'): [{'src_start': 50, 'dst_start': 98, 'range': 2}, ...]}

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