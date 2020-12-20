import fileinput
import re
from itertools import groupby

input_rows = [line.rstrip() for line in fileinput.input('input.txt')]

rule_rows, messages = [list(rows) for k, rows in groupby(input_rows, bool) if k]
rules = dict()

for row in rule_rows:
    key, rule = row.split(': ')
    rules[int(key)] = rule.strip('\"')


def get_pattern(rule):
    if not any(c.isdigit() for c in rule):
        return rule

    rule_groups = [''.join(get_pattern(rules[int(r)]) for r in group.split()) for group in rule.split(' | ')]

    return '(' + '|'.join(rule_groups) + ')'


# Part 1

regex_pattern_1 = re.compile(r'^' + get_pattern(rules[0]) + '$')

print(len([message for message in messages if regex_pattern_1.match(message)]))

# Part 2

r_42 = get_pattern(rules[42])
r_31 = get_pattern(rules[31])

rules[8] = '(' + r_42 + ')+'

# yolo
rules[11] = f'({r_42}{r_31}' \
            f'|{r_42}{r_42}{r_31}{r_31}' \
            f'|{r_42}{r_42}{r_42}{r_31}{r_31}{r_31}' \
            f'|{r_42}{r_42}{r_42}{r_42}{r_31}{r_31}{r_31}{r_31}' \
            f'|{r_42}{r_42}{r_42}{r_42}{r_42}{r_31}{r_31}{r_31}{r_31}{r_31})'

regex_pattern_2 = re.compile(r'^' + get_pattern(rules[0]) + '$')

print(len([message for message in messages if regex_pattern_2.match(message)]))
