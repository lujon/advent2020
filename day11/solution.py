import fileinput
from itertools import product


def update_seats(seat_matrix, occupied_counter, occupied_tolerance):
    x_max = len(seat_matrix[0])
    y_max = len(seat_matrix)

    updated_seats = []

    for y in range(0, y_max):
        row = list(seat_matrix[y])
        for x in range(0, x_max):
            row[x] = update_seat(x, y, seat_matrix, occupied_counter, occupied_tolerance)
        updated_seats.append(''.join(row))

    return updated_seats


def update_seat(x, y, seat_matrix, occupied_counter, occupied_tolerance):
    if seat_matrix[y][x] == 'L':
        return '#' if occupied_counter(x, y, seat_matrix) == 0 else 'L'
    elif seat_matrix[y][x] == '#':
        return 'L' if occupied_counter(x, y, seat_matrix) >= occupied_tolerance else '#'
    else:
        return '.'


# Part 1


def count_adjacent_occupied(x, y, seat_matrix):
    adjacent = [
        (x-1, y-1),
        (x, y-1),
        (x+1, y-1),
        (x-1, y),
        (x+1, y),
        (x-1, y+1),
        (x, y+1),
        (x+1, y+1),
    ]
    return sum([is_occupied(x, y, seat_matrix) for x, y in adjacent])


def is_occupied(x, y, seat_matrix):
    if x < 0 or y < 0 or x >= len(seat_matrix[0]) or y >= len(seat_matrix):
        return False
    else:
        return seat_matrix[y][x] == '#'


input_rows = [line.rstrip() for line in fileinput.input('input.txt')]

rows = input_rows.copy()

while (updated_rows := update_seats(rows, count_adjacent_occupied, 4)) != rows:
    rows = updated_rows

print(sum(row.count('#') for row in rows))

# Part 2


def count_occupied_in_sight(x, y, seat_matrix):
    directions = list(product((-1, 0, 1), repeat=2))
    directions.remove((0, 0))
    return sum([occupied_in_sight(x, y, x_step, y_step, seat_matrix) for x_step, y_step in directions])


def occupied_in_sight(x, y, x_step, y_step, seat_matrix):
    while 0 <= (x := (x+x_step)) < len(seat_matrix[0]) and 0 <= (y := (y+y_step)) < len(seat_matrix):
        if seat_matrix[y][x] == '#':
            return True
        elif seat_matrix[y][x] == 'L':
            return False
    return False


rows = input_rows.copy()

while (updated_rows := update_seats(rows, count_occupied_in_sight, 5)) != rows:
    rows = updated_rows

print(sum(row.count('#') for row in rows))
