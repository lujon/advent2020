import fileinput
import re

lines = [line.split() for line in fileinput.input("input.txt")]

passports = []

passport = dict()
for i, line in enumerate(lines):
    for field in line:
        key, value = field.split(':')
        passport[key] = value
    if not line or i == len(lines)-1:
        passports.append(passport)
        passport = dict()

# Part 1


def has_required_fields(passport):
    required_fields = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}

    return required_fields.issubset(set(passport.keys()))


valid_passports = [passport for passport in passports if has_required_fields(passport)]
print(len(valid_passports))

# Part 2


def field_is_valid(field):

    key, value = field

    year_pattern = re.compile(r'^([0-9]{4}$)')

    if key == 'byr':
        return year_pattern.match(value) and 1920 <= int(value) <= 2002
    elif key == 'iyr':
        return year_pattern.match(value) and 2010 <= int(value) <= 2020
    elif key == 'eyr':
        return year_pattern.match(value) and 2020 <= int(value) <= 2030
    elif key == 'hgt':
        match = re.compile(r'^(?P<height>[0-9]*)(?P<unit>cm|in)$').match(value)

        if not match:
            return False

        height = int(match.groupdict()['height'])
        unit = match.groupdict()['unit']

        if unit == 'cm':
            return 150 <= height <= 193
        else:
            return 59 <= height <= 76
    elif key == 'hcl':
        return re.compile(r'^#[0-9a-f]{6}$').match(value)
    elif key == 'ecl':
        return value in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')
    elif key == 'pid':
        return re.compile(r'^[0-9]{9}$').match(value)
    else:
        return True


valid_passports = [p for p in passports if has_required_fields(p) and all(list(map(field_is_valid, p.items())))]

print(len(valid_passports))
