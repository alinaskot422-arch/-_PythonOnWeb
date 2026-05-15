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
        print("Неверный оператор!")

calc()









  
