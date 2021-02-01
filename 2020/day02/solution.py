import fileinput
import re

input_pattern = re.compile(r'(?P<min>[0-9]+)\-(?P<max>[0-9]+) (?P<char>[a-z]): (?P<password>[a-z]+)')

policies_and_passwords = [re.match(input_pattern, line).groupdict() for line in fileinput.input("input.txt")]

# Part 1

allowed_passwords = [p for p in policies_and_passwords
                     if int(p['min']) <= p['password'].count(p['char']) <= int(p['max'])]

print(len(allowed_passwords))

# Part 2

allowed_passwords = [p for p in policies_and_passwords
                     if (p['password'][int(p['min'])-1] == p['char']) ^ (p['password'][int(p['max'])-1] == p['char'])]

print(len(allowed_passwords))
