def calculator():
    try:
        num1 = float(input("Введіть перше число: "))
        operation = input("Введіть операцію (+, -, *, /): ").strip()
        num2 = float(input("Введіть друге число: "))

        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 == 0:
                print("Помилка: ділення на нуль неможливе!")
                return
            result = num1 / num2
        else:
            print("Помилка: невідома операція!")
            return

        if result.is_integer():
            result = int(result)

        print(f"Результат: {result}")

    except ValueError:
        print("Помилка: введено некоректні дані! Потрібно вводити числа.")

if __name__ == "__main__":
    calculator()