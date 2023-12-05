import sys
import re

def main():
    if not validate_run():
        print("Aborting...")
        exit()
    input_text = read_input(sys.argv[1])
    data = parse_input(input_text)

    print("Problem 1:", solve_problem_1(data))
    print('Problem 2:', solve_problem_2(data))


def solve_problem_1(data):
    locations = []
    mappings = build_mappings(data)
    for _, mapping in mappings.items():
        locations.append(mapping['location'])
    locations.sort()
    return locations[0]


def solve_problem_2(data):
    soils = []
    fertilizers = []
    waters = []
    lights = []
    temperatures = []
    humidities = []
    locations = []

    data = fill_missing_data(data)

    for seed_range in data['seed_ranges']:
        soils += find_destination_range(data, 'seed', 'soil', seed_range['start'], seed_range['range'])
    for soil in soils:
        fertilizers += find_destination_range(data, 'soil', 'fertilizer', soil['dst_start'], soil['range'])
    for fertilizer in fertilizers:
        waters += find_destination_range(data, 'fertilizer', 'water', fertilizer['dst_start'], fertilizer['range'])
    for water in waters:
        lights += find_destination_range(data, 'water', 'light', water['dst_start'], water['range'])
    for light in lights:
        temperatures += find_destination_range(data, 'light', 'temperature', light['dst_start'], light['range'])
    for temperature in temperatures:
        humidities += find_destination_range(data, 'temperature', 'humidity', temperature['dst_start'], temperature['range'])
    for humidity in humidities:
        locations += find_destination_range(data, 'humidity', 'location', humidity['dst_start'], humidity['range'])
    
    locations.sort(key=lambda x: x['dst_start'])
    return locations[0]['dst_start']


def fill_missing_data(data):
    for pair in [('seed', 'soil'), ('soil', 'fertilizer'), ('fertilizer', 'water'), ('water', 'light'), ('light', 'temperature'), ('temperature', 'humidity'), ('humidity', 'location')]:
        data[pair] = fill_missing_data_ranges(data[pair])
    return data

def fill_missing_data_ranges(ranges):
    ranges.sort(key=lambda x: x['src_start'])
    if ranges[0]['src_start'] != 0:
        ranges.insert(0, {'dst_start': 0, 'src_start': 0, 'range': ranges[0]['src_start']})
    i = 0
    while i < len(ranges) - 1:
        end = ranges[i]['src_start'] + ranges[i]['range']
        if end < ranges[i+1]['src_start']:
            ranges.insert(i, {
                'src_start': end,
                'dst_start': end,
                'range': ranges[i+1]['src_start'] - end
            })
            i += 1
        i += 1
    return ranges


def find_destination_range(data, src, dst, src_start, irange):
    '''Returns a list of source ranges mapped to destination ranges.
    [
        {'src_start': 1000, 'dst_start': 900, 'range': 50},
        {'src_start': 1050, 'dst_start': 120, 'range': 25}
    ]'''

    mappings = []
    for entry in data[(src, dst)]:
        if src_start >= entry['src_start'] and src_start < entry['src_start'] + entry['range']:
            # ok, the start is in here, now let's see how much of it is in here.

            # easy case: all range fits.
            if src_start + irange < entry['src_start'] + entry['range']:
                mappings.append({'src_start': src_start,
                                 'dst_start': entry['dst_start'] + src_start - entry['src_start'],
                                 'range': irange})
                continue

            # range doesn't fit; we save what fits and do the rest recursively.
            range_solved = entry['src_start'] + entry['range'] - src_start
            mappings.append({'src_start': src_start,
                            'dst_start': entry['dst_start'] + src_start - entry['src_start'],
                            'range': range_solved})
            mappings += find_destination_range(data, src, dst, src_start + range_solved, irange - range_solved)

    if not mappings and irange > 0:
        # given that we backfilled the ranges, this means that our source is greater than any range in the list.
        mappings = [{'src_start': src_start, 'dst_start': src_start, 'range': irange}]
    return mappings


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
            seeds_list = list(map(int, re.findall(r'\d+', section.split(': ')[1]))) # eg [79, 14, 55, 13]
            # for problem 1, just a list of seeds:
            data['seeds'] = seeds_list
            # for problem 2, a list of seed starts with ranges:
            data['seed_ranges'] = []
            for i in range(0, len(seeds_list), 2):
                data['seed_ranges'].append({'start': seeds_list[i], 'range': seeds_list[i+1]})
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