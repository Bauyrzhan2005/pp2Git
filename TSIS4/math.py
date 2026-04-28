#1
import math

degree = float(input("Input degree: "))
radian = degree * (math.pi / 180)

print("Output radian:", round(radian, 6))

#2 trapezoid
height = float(input("Height: "))
base1 = float(input("Base, a: "))
base2 = float(input("Base, b: "))

area = ((base1 + base2) / 2) * height

print("Expected Output:", area)

#3 polygon
import math

n = int(input("Input number of sides: "))
s = float(input("Input the length of a side: "))

area = (n * s * s) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", round(area))

#4 parallelogram
base = float(input("Base: "))
height = float(input("Height: "))

area = base * height

print("Expected Output:", area)