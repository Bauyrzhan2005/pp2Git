# creating a function
def my_function():
   print("Hello from a function")

# calling a function
#1
def my_function():
   print("Hello from a function")
   
my_function()

#2
def my_function():
   print("Hello from a function")

my_function()
my_function()
my_function()

# function names
#calculate_sum()
#_private_function()
#myFunction2()

#3
temp1 = 77
celsius1 = (temp1 - 32) * 5 / 9
print(celsius1)

temp2 = 95
celsius2 = (temp2 - 32) * 5 / 9
print(celsius2)

temp3 = 50
celsius3 = (temp3 - 32) * 5 / 9
print(celsius3)

#4
def fahrenheit_to_celsius(fahrenheit):
   return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))

#5
def get_greeting():
   return "Hello from a function"

message = get_greeting()
print(message)

#6
def get_greeting():
   return "Hello from a function"

print(get_greeting())

#7
def my_function():
   pass