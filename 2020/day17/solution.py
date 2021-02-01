import fileinput
from itertools import product


def run_cycle(active_positions):
    updated_active = active_positions.copy()

    for active_position in active_positions:
        active_neighbours = count_active_neighbours(active_positions, active_position)

        if active_neighbours not in (2, 3):
            updated_active.remove(active_position)

        neighbours = get_adjacent_positions(active_position)
        inactive_neighbours = [neighbour for neighbour in neighbours if neighbour not in active_positions]

        for neighbour in inactive_neighbours:
            if count_active_neighbours(active_positions, neighbour) == 3:
                updated_active.add(neighbour)

    return updated_active


def count_active_neighbours(active_positions, coordinates):
    neighbours = get_adjacent_positions(coordinates)
    return sum(neighbour in active_positions for neighbour in neighbours)


def get_adjacent_positions(coordinates):
    adjacent_deltas = list(product((-1, 0, 1), repeat=len(coordinates)))
    s = tuple([0] * len(coordinates))
    adjacent_deltas.remove(s)

    return [tuple(coordinates[i] + adjacent_delta[i] for i in range(len(coordinates)))
            for adjacent_delta in adjacent_deltas]


def get_active_cubes(initial_active_positions, dimensions, cycles):
    active_positions = {tuple([x, y] + [0]*(dimensions-2)) for x, y in initial_active_positions}

    for _ in range(cycles):
        active_positions = run_cycle(active_positions)

    return active_positions


input_rows = [line.rstrip() for line in fileinput.input('input.txt')]

initial_active_positions = []
for y, row in enumerate(input_rows):
    initial_active_positions.extend((x, y) for x, cell in enumerate(row) if cell == '#')

# Part 1
print(len(get_active_cubes(initial_active_positions, 3, 6)))

# Part 2
print(len(get_active_cubes(initial_active_positions, 4, 6)))
