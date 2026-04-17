# #1
# N = int(input("Введите число N: "))
# for i in range(1, N + 1):
#     print(i)

# #2
# N = int(input("Введите число N: "))
# while N >= 1:
#     print(N)
#     N -= 1

# 3
# for i in range(2,21):
#     if i%2 == 0:
#      print(i)

# 4
# a =0
# while True:
#     n=int(input("Введите число: "))
#     a+=n
#     if n ==0:
#         print(a)
#         break

# 5
# for i in range(1,11):
#     for j in range(1,11):
#         print(f"{i}*{j}={i*j}")

# 6
# num = 42
# a = 0
# while True:
#     b = int(input("Угадайте число: "))
#     a += 1
#     if b < num:
#         print("Больше")
#     elif b > num:
#         print("Меньше")
#     else:
#         print("Победа!")
#         break

# print("Количество попыток:", a)

# 7
# text = input("Введите строку: ")
# c = "aeiouyаеёиоуыэюя"
# count = 0
# for i in text:
#     if i in c:
#         count += 1
# print("Количество гласных:", count)

# 8
# N = int(input("Введите N: "))
# factorial = 1
# for i in range(1, N + 1):
#     factorial *= i
# print(f"{N}! = {factorial}")

# 9
# numbers = [12, -5, 0, 44, 23]
# max = numbers[0]
# for i in numbers:
#     if i > max :
#          max= i
# print("Максимальный элемент:", max)

# 10
N = int(input("Введите N: "))
a, b = 0, 1
count = 0
while count < N:
    print(a)
    a, b = b, a + b
    count += 1