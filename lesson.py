expression = input()

tokens = []
i = 0
while i < len(expression):
    if expression[i] == ' ':
        i += 1
        continue
    if expression[i] in '+-*/()':
        tokens.append(expression[i])
        i += 1
    elif expression[i].isdigit():
        num = ''
        while i < len(expression) and expression[i].isdigit():
            num += expression[i]
            i += 1
        tokens.append(int(num))

index = 0

def parse_expression():
    global index
    value = parse_term()
    while index < len(tokens) and tokens[index] in ('+', '-'):
        op = tokens[index]
        index += 1
        if op == '+':
            value += parse_term()
        else:
            value -= parse_term()
    return value

def parse_term():
    global index
    value = parse_factor()
    while index < len(tokens) and tokens[index] in ('*', '/'):
        op = tokens[index]
        index += 1
        if op == '*':
            value *= parse_factor()
        else:
            value /= parse_factor()
    return value

def parse_factor():
    global index
    token = tokens[index]
    if token == '(':
        index += 1
        value = parse_expression()
        index += 1
        return value
    else:
        index += 1
        return token

print(parse_expression())