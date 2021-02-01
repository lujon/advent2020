import fileinput

instructions = []

with fileinput.input('input.txt') as f:
    for line in f:
        instruction, argument = line.rstrip().split()
        instructions.append((instruction, int(argument)))


def execute_instruction(acc, pc, instruction):
    code, arg = instruction

    if code == 'acc':
        acc += arg
        pc += 1
    elif code == 'jmp':
        pc += arg
    elif code == 'nop':
        pc += 1

    return acc, pc


def run_until_inf_loop_or_termination(instructions):
    pc = 0
    acc = 0
    executed_instructions = set()

    while pc not in executed_instructions and pc < len(instructions):
        executed_instructions.add(pc)
        acc, pc = execute_instruction(acc, pc, instructions[pc])

    return acc, pc


# Part 1

acc, pc = run_until_inf_loop_or_termination(instructions)

print(acc)

# Part 2

for i, instruction in enumerate(instructions):
    code, arg = instruction

    if code in ('nop', 'jmp'):
        instructions_copy = instructions.copy()
        new_code = 'nop' if code == 'jmp' else 'jmp'
        instructions_copy[i] = new_code, arg
        acc, pc = run_until_inf_loop_or_termination(instructions_copy)

        if pc == len(instructions):
            break

print(acc)
