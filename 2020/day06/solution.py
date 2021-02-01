import fileinput

group_answers = [line.rstrip() for line in fileinput.input('input.txt')]

# PART 1
i = 0
seen = set()
for index, person in enumerate(group_answers):
    seen.update(person)
    if not person or index == len(group_answers)-1:
        i += len(seen)
        seen = set()

print(i)

# PART 2
i = 0
answers = []
for index, person in enumerate(group_answers):
    if person:
        answers.append(set(person))
    if not person or index == len(group_answers)-1:
        i += len(set.intersection(*answers))
        answers = []

print(i)
