# 1
year = int(input("Введите год "))
if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
    print("Високосный")
else:
    print("Не високосный")

# 2
x = float(input("Введите X "))
y = float(input("Введите Y "))
if x == 0 and y == 0:
    print("Начало координат")
elif x == 0:
    print("На оси Y")
elif y == 0:
    print("На оси X")
elif x > 0 and y > 0:
    print("1")
elif x < 0 and y > 0:
    print("2")
elif x < 0 and y < 0:
    print("3")
else:
    print("4")

# 3
A = int(input("Введите A "))
B = int(input("Введите B "))
K = int(input("Введите K "))
count = 0
min = None
max = None
for num in range(A, B + 1):
    temp = num
    product = 1
    if temp == 0:
        product = 0
    else:
        while temp > 0:
            d = temp % 10
            if d != 0:
                product *= d
            temp //= 10
    
    if product == K:
        count += 1
        if min is None or num < min:
            min = num
        if max is None or num > max:
            max = num

if count == 0:
    print("Нет подходящих чисел")
else:
    print(count)
    print(min)
    print(max)