import fileinput


def get_seat_id(boarding_pass):
    row = binary_partitioning(boarding_pass[:7], 0, 127)
    column = binary_partitioning(boarding_pass[7:], 0, 7)
    return row * 8 + column


def binary_partitioning(seq, low, high):
    for step in seq:
        if step in ('F', 'L'):
            high = high - (high-low+1)//2
        else:
            low = low + (high-low+1)//2
    return low


boarding_passes = [line.rstrip() for line in fileinput.input('input.txt')]

# PART 1
taken_ids = list(map(get_seat_id, boarding_passes))
print(max(taken_ids))

# PART 2
all_ids = set(range(min(taken_ids), max(taken_ids)))
print(list(all_ids.difference(taken_ids))[0])
