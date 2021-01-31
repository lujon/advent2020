import fileinput


def transform_subject_number(subject_number, loop_size):
    value = 1

    for _ in range(0, loop_size):
        value *= subject_number
        value %= 20201227

    return value


def find_loop_size(subject_number, target_number):
    value = 1
    loop_size = 0

    while value != target_number:
        value *= subject_number
        value %= 20201227
        loop_size += 1

    return loop_size


card_public_key, door_public_key = [int(line.rstrip()) for line in fileinput.input('input.txt')]

card_loop_size = find_loop_size(7, card_public_key)

door_loop_size = find_loop_size(7, door_public_key)

print(card_loop_size, door_loop_size)

encryption_key = transform_subject_number(door_public_key, card_loop_size)
print(encryption_key)

