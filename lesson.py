def tokenize(expression):
    tokens = []
    i = 0
    while i < len(expression):
        char = expression[i]
        if char.isspace():
            i += 1
            continue
        if char in "+-*/()":
            tokens.append(char)
            i += 1
        elif char.isdigit() or char == '.':
            num_str = ""
            while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                num_str += expression[i]
                i += 1
            tokens.append(float(num_str))
        else:
            raise ValueError(f"Некоректний символ: {char}")
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current_token(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse(self):
        result = self.expr()
        if self.pos < len(self.tokens):
            raise ValueError("Некоректна синтаксична структура")
        return result

    # Додавання та віднімання (найнижчий пріоритет)
    def expr(self):
        result = self.term()
        while self.current_token() in ('+', '-'):
            op = self.current_token()
            self.pos += 1
            if op == '+':
                result += self.term()
            elif op == '-':
                result -= self.term()
        return result

    # Множення та ділення (вищий пріоритет)
    def term(self):
        result = self.factor()
        while self.current_token() in ('*', '/'):
            op = self.current_token()
            self.pos += 1
            if op == '*':
                result *= self.factor()
            elif op == '/':
                divisor = self.factor()
                if divisor == 0:
                    raise ZeroDivisionError("Ділення на нуль неможливе")
                result /= divisor
        return result

    # Числа, дужки та унарні знаки (найвищий пріоритет)
    def factor(self):
        token = self.current_token()
        if token == '-':
            self.pos += 1
            return -self.factor()
        elif token == '+':
            self.pos += 1
            return self.factor()
        elif isinstance(token, float):
            self.pos += 1
            return token
        elif token == '(':
            self.pos += 1
            result = self.expr()
            if self.current_token() != ')':
                raise ValueError("Пропущено закриваючу дужку ')'")
            self.pos += 1
            return result
        else:
            raise ValueError("Очікувалось число або дужка")

def evaluate(expression):
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Порожній вираз")
    parser = Parser(tokens)
    return parser.parse()

if __name__ == "__main__":
    expr = input("Введіть математичний вираз: ")
    try:
        res = evaluate(expr)
        if res.is_integer():
            res = int(res)
        print(f"Результат: {res}")
    except Exception as e:
        print(f"Помилка: {e}")