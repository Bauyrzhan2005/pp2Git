#1
class Person:
   def __init__(self, name, age):
      self.name = name
      self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)

#2
class Person:
   pass

p1 = Person()
p1.name = "Tobias"
p1.age = 25

print(p1.name)
print(p1.age)

#3
class Person:
   def __init__(self, name, age):
      self.name = name
      self.age = age

p1 = Person("Linus", 28)

print(p1.name)
print(p1.age)

#4
class Person:
   def __init__(self, name, age, city, country):
      self.name = name
      self.age = age
      self.city = city
      self.country = country

p1 = Person("Linus", 30, "Oslo", "Norway")

print(p1.name)
print(p1.age)
print(p1.city)
print(p1.country)