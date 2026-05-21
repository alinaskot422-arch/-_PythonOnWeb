# 1
def calc():
    print("Калькулятор: +, -, *, /")
    a = int(input("Число 1: "))
    op = input("Оператор: ")
    b = int(input("Число 2: "))

    if op == '+':
        print(a + b)
    elif op == '-':
        print(a - b)
    elif op == '*':
        print(a * b)
    elif op == '/':
        print(a / b)
    else:
        print("Неверный оператор")

calc()

# 2
def calc():
    print("Калькулятор: +, -, *, /")
    a = int(input("Число 1: "))
    op = input("Оператор: ")
    b = int(input("Число 2: "))

    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else "Ошибка: деление на ноль"
    }

    if op in operations:
        result = operations[op](a, b)
        print(f"Результат: {result}")
    else:
        print("Неверный оператор")

calc()









  
