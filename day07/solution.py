import fileinput
import re

lines = [line.rstrip() for line in fileinput.input('input.txt')]

parent_pattern = re.compile(r'^[a-z]+ [a-z]+')
child_pattern = re.compile(r'[0-9]+ [a-z]+ [a-z]+')

bags = dict()

for line in lines:
    parent = parent_pattern.search(line).group(0)
    children = []
    for child_string in child_pattern.findall(line):
        number, color = child_string.split(' ', 1)
        children.append((int(number), color))
    bags[parent] = children

# Part 1


def bag_contains_gold(parent_color):
    children = bags[parent_color]

    if not children:
        return False

    for number, color in children:
        if color == 'shiny gold' or bag_contains_gold(color):
            return True
    return False


bags_containing_gold = [parent for parent in bags.keys() if bag_contains_gold(parent)]

print(len(bags_containing_gold))

# Part 2


def count_bags(parent_color):
    children = bags[parent_color]

    if not children:
        return 1

    return 1 + sum(number*count_bags(color) for number, color in children)


print(count_bags('shiny gold') - 1)
