import fileinput
from collections import defaultdict
from itertools import groupby
from math import prod

input_rows = [line.rstrip() for line in fileinput.input('input.txt')]

rule_rows, your_ticket_rows, other_tickets_rows = [list(rows) for k, rows in groupby(input_rows, bool) if k]

rules = defaultdict(list)

for row in rule_rows:
    key, ranges = row.split(': ')
    for r in ranges.split(' or '):
        upper, lower = r.split('-')
        rules[key].append((int(upper), int(lower)))

your_ticket = list(map(int, your_ticket_rows[1].split(',')))
other_tickets = [list(map(int, (row.split(',')))) for row in other_tickets_rows[1:]]


# Part 1

def is_valid_for_some_rule(value):
    for ranges in rules.values():
        for lower, upper in ranges:
            if lower <= value <= upper:
                return True
    return False


invalid_values = []

for ticket in other_tickets:
    for value in ticket:
        if not is_valid_for_some_rule(value):
            invalid_values.append(value)

print(sum(invalid_values))

# Part 2

valid_tickets = [ticket for ticket in other_tickets
                 if all(is_valid_for_some_rule(value) for value in ticket)]


def is_valid_for_rule(value, rule):
    for lower, upper in rules[rule]:
        if lower <= value <= upper:
            return True
    return False


def is_valid_for_tickets(tickets, rule, field_index):
    for ticket in tickets:
        if not is_valid_for_rule(ticket[field_index], rule):
            return False
    return True


fields = list(rules.keys())

valid_indices_by_field = defaultdict(list)

for field in fields:
    for i in range(len(your_ticket)):
        if is_valid_for_tickets(valid_tickets, field, i):
            valid_indices_by_field[field].append(i)


def get_valid_path(fields, used_indices):
    field = fields[0]
    valid_indices = [index for index in valid_indices_by_field[field] if index not in used_indices]

    if len(fields) == 1:
        if len(valid_indices) == 1:
            return [list(valid_indices)[0]]
        else:
            return []
    else:
        for index in valid_indices:
            used_indices_copy = used_indices.copy()
            used_indices_copy.add(index)
            valid_path = get_valid_path(fields[1:], used_indices_copy)

            if valid_path:
                return [index] + valid_path
        return []


valid_path = get_valid_path(fields, set())

departure_indices = [index for i, index in enumerate(valid_path) if 'departure' in fields[i]]

print(prod(your_ticket[i] for i in departure_indices))
