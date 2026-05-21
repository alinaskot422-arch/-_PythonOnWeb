# 1
number = int(input("Введите целое число "))
if number % 2 == 0:
    print("Число четное")
else:
    print("Число нечетное")

# 2
height = float(input("Введите свой рост "))
if height > 120:
    print("Добро пожаловать")
else:
    print("Извините, вы слишком малы")

# 3
num = float(input("Введите число "))
if num > 0:
    print("Положительное")
elif num < 0:
    print("Отрицательное")
else:
    print("Это ноль")

# 4
password = "secret123"
ans = input("Введите пароль ")
if ans == password:
    print("Доступ разрешен")
else:
    print("Неверный пароль")

# 5
amount = float(input("Введите сумму покупки "))
if amount > 1000:
    discount = amount * 0.10
    result = amount - discount
    print(result)
else:
    print(amount)