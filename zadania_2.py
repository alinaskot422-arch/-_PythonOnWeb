# 1
price = 1200
discount = price * 0.15
price2 = price - discount
s = price2 * 0.20
result = price2 + s
print(result)

# 2
sec = 3665
hours = sec // 3600
r = sec % 3600
min = r // 60
sec_left = r % 60
print(f"{hours}:{min}:{sec_left}")

# 3
weight = int(input("Введите вес "))
height_cm = int(input("Введите рост "))
height_m = height_cm / 100
imt = weight / (height_m ** 2)
print(round(imt, 1))

# 4
num = int(input("Введите трехзначное число "))
a = num // 100
b = (num // 10) % 10
c = num % 10
sum = a + b + c
product = a * b * c
magic = product - sum
print(magic)

# 5
d = 90.5
dollars = 50
commis = 0.025
rub = (dollars * d) * (1 + commis)
print(rub)