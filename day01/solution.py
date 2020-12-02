import fileinput
from itertools import combinations

expenses = [int(line) for line in fileinput.input("input.txt")]

# Part 1

seen = set()

for x in expenses:
    if abs(2020 - x) in seen:
        print(x * abs(x - 2020))
        break
    seen.add(x)

# Part 2

expenses_combinations = combinations(expenses, 3)

for x, y, z in expenses_combinations:
    if x + y + z == 2020:
        print(x * y * z)
        break
