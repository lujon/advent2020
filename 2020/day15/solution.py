import fileinput

input_rows = [line.rstrip() for line in fileinput.input('input.txt')]

# Part 1

start_numbers = [int(number) for number in input_rows[0].split(',')]


def get_nth_number(n):
    seen_number_positions = dict()

    for i, number in enumerate(start_numbers[:-1]):
        seen_number_positions[number] = i+1

    current_number = start_numbers[-1]

    for i in range(len(start_numbers), n):
        if current_number in seen_number_positions:
            last_seen = seen_number_positions[current_number]
            seen_number_positions[current_number] = i
            current_number = i - last_seen
        else:
            seen_number_positions[current_number] = i
            current_number = 0
    return current_number


# Part 1
print(get_nth_number(2020))

# Part 2
print(get_nth_number(30000000))
