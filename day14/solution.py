import fileinput
import re
from itertools import product

input_rows = [line.rstrip() for line in fileinput.input('input.txt')]

# Part 1


def mask_1(mask, value):
    bits = list('{:036b}'.format(value))

    for i in range(0, len(bits)):
        if mask[i] != 'X':
            bits[i] = mask[i]
    return int(''.join(bits), 2)


memory = dict()
mask = 36 * 'X'

instruction_pattern = re.compile(r'^mem\[(?P<address>[0-9]+)] = (?P<value>[0-9]+)$')

for row in input_rows:
    if match := instruction_pattern.match(row):
        instruction = match.groupdict()
        memory[instruction['address']] = mask_1(mask, int(instruction['value']))
    else:
        mask = row.split(' = ')[1]

print(sum(memory.values()))


# Part 2

def mask_2(mask, value):
    bits = list('{:036b}'.format(value))

    for i in range(0, len(bits)):
        if mask[i] != '0':
            bits[i] = mask[i]
    return ''.join(bits)


def get_addresses(original_address, mask):
    address_with_floating = mask_2(mask, original_address)

    num_floating = address_with_floating.count('X')

    addresses = []

    for floating_replacements in product((0, 1), repeat=num_floating):
        address = address_with_floating

        for digit in floating_replacements:
            address = address.replace('X', str(digit), 1)

        addresses.append(int(address, 2))

    return addresses


memory = dict()
mask = 36 * '0'

for row in input_rows:
    if match := instruction_pattern.match(row):
        instruction = match.groupdict()
        for address in get_addresses(int(instruction['address']), mask):
            memory[address] = int(instruction['value'])
    else:
        mask = row.split(' = ')[1]

print(sum(memory.values()))
