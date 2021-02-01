import fileinput
from collections import defaultdict
from operator import add


def parse_line(line):
    steps = []

    while line:
        if line[:1] in ('e', 'w'):
            steps.append(line[:1])
            line = line[1:]
        elif line[:2] in ('se', 'sw', 'nw', 'ne'):
            steps.append(line[:2])
            line = line[2:]

    return steps


input_rows = [line.rstrip() for line in fileinput.input('input.txt')]
steps_list = [parse_line(line) for line in input_rows]

directions_even = {
    'e': (1, 0),
    'se': (1, 1),
    'sw': (0, 1),
    'w': (-1, 0),
    'nw': (0, -1),
    'ne': (1, -1),
}

directions_uneven = {
    'e': (1, 0),
    'se': (0, 1),
    'sw': (-1, 1),
    'w': (-1, 0),
    'nw': (-1, -1),
    'ne': (0, -1),
}

flipped_coordinates = set()

for steps in steps_list:
    coordinates = (0, 0)

    for s in steps:
        direction = directions_even[s] if coordinates[1] % 2 == 0 else directions_uneven[s]
        coordinates = tuple(map(add, coordinates, direction))

    if coordinates in flipped_coordinates:
        flipped_coordinates.remove(coordinates)
    else:
        flipped_coordinates.add(coordinates)

# Part 1

print(len(flipped_coordinates))

# Part 2

adjacent_even = tuple(directions_even.values())
adjacent_uneven = tuple(directions_uneven.values())

for _ in range(0, 100):
    adjacent_count = defaultdict(int)

    for flipped_coordinate in flipped_coordinates:
        if flipped_coordinate[1] % 2 == 0:
            adjacent = adjacent_even
        else:
            adjacent = adjacent_uneven

        for adjacent_coordinate in adjacent:
            adjacent_count[tuple(map(add, flipped_coordinate, adjacent_coordinate))] += 1

        if flipped_coordinate not in adjacent_count:
            adjacent_count[flipped_coordinate] = 0

    for coordinate, flipped_neighbours in adjacent_count.items():
        if coordinate in flipped_coordinates and (flipped_neighbours == 0 or flipped_neighbours > 2):
            flipped_coordinates.remove(coordinate)
        elif coordinate not in flipped_coordinates and flipped_neighbours == 2:
            flipped_coordinates.add(coordinate)

print(len(flipped_coordinates))

