import fileinput


def evaluate(expression, precedences):
    postfix_expression = to_postfix(expression, precedences)
    return evaluate_postfix(postfix_expression)


def to_postfix(infix_expression, precedences):
    operands = list()
    output = list()
    infix_expression = infix_expression.replace('(', '( ').replace(')', ' )')
    tokens = infix_expression.split(' ')

    for token in tokens:
        if token.isnumeric():
            output.append(token)
        elif token == '(':
            operands.append(token)
        elif token == ')':
            while (op := operands.pop()) != '(':
                output.append(op)
        else:
            while operands and operands[-1] != '(' and precedences[token] <= precedences[operands[-1]]:
                output.append(operands.pop())
            operands.append(token)

    while operands:
        output.append(operands.pop())

    return output


def evaluate_postfix(postfix_expression):
    operands = list()

    for token in postfix_expression:
        if token.isnumeric():
            operands.append(int(token))
        else:
            o1 = operands.pop()
            o2 = operands.pop()

            if token == '*':
                operands.append(o1 * o2)
            else:
                operands.append(o1 + o2)

    return operands.pop()


input_rows = [line.rstrip() for line in fileinput.input('input.txt')]

# Part 1

print(sum(evaluate(row, {'*': 1, '+': 1}) for row in input_rows))

# Part 2

print(sum(evaluate(row, {'*': 1, '+': 2}) for row in input_rows))