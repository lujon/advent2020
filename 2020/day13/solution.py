import fileinput
from functools import reduce

input_rows = [line.rstrip() for line in fileinput.input('input.txt')]
earliest_timestamp = int(input_rows[0])
buses = [bus for bus in input_rows[1].split(',')]
buses_in_service = [int(bus) for bus in buses if bus != 'x']

# Part 1

timestamp = earliest_timestamp

while not (arriving_buses := [bus for bus in buses_in_service if timestamp % bus == 0]):
    timestamp += 1

print(arriving_buses[0] * (timestamp - earliest_timestamp))


# Part 2

def buses_arrive_sequentially(buses, timestamp):
    return all([bus == 'x' or (timestamp + i) % int(bus) == 0 for i, bus in enumerate(buses)])


def chinese_remainder(n, a):
    s = 0
    prod = reduce(lambda a, b: a*b, n)

    for n_i, a_i in zip(n, a):
        p = prod//n_i
        s += a_i * mul_inv(p, n_i)*p

    return s % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1
    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1


remainders = [int(bus)-i for i, bus in enumerate(buses) if bus != 'x']
print(chinese_remainder(buses_in_service, remainders))
