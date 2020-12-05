import fileinput
boarding_passes = []
with fileinput.input('input.txt') as f:
    for line in f:
        boarding_passes.append(line.rstrip())


def seat(boarding_pass):
    row_list = list(range(0, 128))
    col_list = list(range(0, 8))
    row_seq = boarding_pass[:7]
    col_seq = boarding_pass[7:]
    for letter in row_seq:
        if letter == "F":
            row_list = row_list[0:int(len(row_list)/2)]
        else:
            row_list = row_list[int(len(row_list)/2):]
    for letter in col_seq:
        if letter == "L":
            col_list = col_list[0:int(len(col_list)/2)]
        else:
            col_list = col_list[int(len(col_list)/2):]
    return row_list[0]*8 + col_list[0]


# PART 1
ids = list(map(seat, boarding_passes))
print(max(ids))
# PART 2
sorted_ids = sorted(ids)
all_ids = set(range(min(sorted_ids), max(sorted_ids)))
print(list(all_ids.difference(sorted_ids))[0])