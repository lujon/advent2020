import fileinput
from collections import defaultdict

ratings = sorted([int(line) for line in fileinput.input('input.txt')])

ratings.insert(0, 0)

max_rating = ratings[-1] + 3

ratings.append(max_rating)

# Part 1

diffs = []

for i, rating in enumerate(ratings[:len(ratings)-1]):
    diffs.append(ratings[i+1] - rating)

print(diffs.count(1) * diffs.count(3))

# Part 2

paths = defaultdict(int)

paths[0] = 1

for i, rating in enumerate(ratings):
    j = i+1
    while j < len(ratings) and ratings[j] - rating <= 3:
        paths[ratings[j]] += paths[rating]
        j += 1

print(paths[max_rating])
