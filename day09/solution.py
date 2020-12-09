import fileinput
from itertools import combinations

numbers = [int(line) for line in fileinput.input('input.txt')]

# Part 1

preamble_length = 25

weak_number = -1

for i in range(preamble_length + 1, len(numbers)):
    number = numbers[i]
    combos = combinations(numbers[i - (preamble_length + 1):i], 2)

    if not any(x + y == number for x, y in combos):
        weak_number = number
        break

print(weak_number)

# Part 2

max_range = []

for i in range(0, len(numbers)):
    j = i + 1

    while sum(numbers[i:j+1]) < weak_number:
        j += 1

    if sum(numbers[i:j+1]) == weak_number and j - i > len(max_range):
        max_range = numbers[i:j+1]

print(min(max_range) + max(max_range))
