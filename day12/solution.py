import fileinput

input_rows = [line.rstrip() for line in fileinput.input('input.txt')]

instructions = [(row[:1], int(row[1:])) for row in input_rows]


# Part 1

def update_coordinates(x, y, direction, distance):
    if direction == 'N':
        y += distance
    elif direction == 'S':
        y -= distance
    elif direction == 'E':
        x += distance
    elif direction == 'W':
        x -= distance
    return x, y


direction_angle = 0
x, y = 0, 0

for instruction, param in instructions:
    if instruction == 'L':
        direction_angle = (direction_angle - param) % 360
    elif instruction == 'R':
        direction_angle = (direction_angle + param) % 360
    elif instruction == 'F':
        forward_direction = {0: 'E', 90: 'S', 180: 'W', 270: 'N'}[direction_angle]
        x, y = update_coordinates(x, y, forward_direction, param)
    else:
        x, y = update_coordinates(x, y, instruction, param)

print(abs(x) + abs(y))


# Part 2

def rotate_waypoint(ship_x, ship_y, waypoint_x, waypoint_y, rotations):
    x = waypoint_x - ship_x
    y = waypoint_y - ship_y

    for _ in range(0, rotations):
        x, y = y, -x

    waypoint_x = x + ship_x
    waypoint_y = y + ship_y

    return waypoint_x, waypoint_y


ship_x, ship_y = 0, 0
waypoint_x, waypoint_y = 10, 1

for instruction, param in instructions:
    if instruction == 'L':
        rotations = (-param // 90) % 4
        waypoint_x, waypoint_y = rotate_waypoint(ship_x, ship_y, waypoint_x, waypoint_y, rotations)
    elif instruction == 'R':
        rotations = (param // 90) % 4
        waypoint_x, waypoint_y = rotate_waypoint(ship_x, ship_y, waypoint_x, waypoint_y, rotations)
    elif instruction == 'F':
        delta_x = (waypoint_x - ship_x) * param
        delta_y = (waypoint_y - ship_y) * param

        ship_x += delta_x
        ship_y += delta_y

        waypoint_x += delta_x
        waypoint_y += delta_y
    else:
        waypoint_x, waypoint_y = update_coordinates(waypoint_x, waypoint_y, instruction, param)

print(abs(ship_x) + abs(ship_y))
