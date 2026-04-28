# with 1 argument
def my_function(fname):
   print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")

#2 The terms parameter and argument can be used for the same thing: information that are passed into a function.
def my_function(name): # name is a parameter
   print("Hello", name)

my_function("Emil") # "Emil" is an argument

#3 function expects 2 arguments, and gets 2 arguments
def my_function(fname, lname):
   print(fname + " " + lname)

my_function("Emil", "Refsnes")

#4 function expects 2 arguments, but gets only 1
def my_function(fname, lname):
   print(fname + " " + lname)

my_function("Emil")

#5
def my_function(name = "friend"):
   print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function()
my_function("Linus")

#6
def my_function(country = "Norway"):
   print("I am from", country)

my_function("Sweden")
my_function("India")
my_function()
my_function("Brazil")


#7 keywords arguments
def my_function(animal, name):
   print("I have a", animal)
   print("My", animal + "'s name is", name)

my_function(animal = "dog", name = "Buddy")

# order doesnt matter
def my_function(animal, name):
   print("I have a", animal)
   print("My", animal + "'s name is", name)

my_function(name = "Buddy", animal = "dog")

#9 positional arguments
def my_function(animal, name):
   print("I have a", animal)
   print("My", animal + "'s name is", name)

my_function("dog", "Buddy")

#10 Mixing Positional and Keyword Arguments
def my_function(animal, name, age):
   print("I have a", age, "year old", animal, "named", name)

my_function("dog", name = "Buddy", age = 5)

#11 Passing Different Data Types
def my_function(fruits):
   for fruit in fruits:
      print(fruit)

my_fruits = ["apple", "banana", "cherry"]
my_function(my_fruits)

#12
def my_function(person):
   print("Name:", person["name"])
   print("Age:", person["age"])

my_person = {"name": "Emil", "age": 25}
my_function(my_person)

#13 Positional-Only Arguments
def my_function(name, /):
   print("Hello", name)

my_function("Emil")

#14
def my_function(name):
   print("Hello", name)

my_function(name = "Emil")

#15
def my_function(*, name):
   print("Hello", name)

my_function(name = "Emil")

#16
def my_function(name):
   print("Hello", name)

my_function("Emil")

#17
def my_function(a, b, /, *, c, d):
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)