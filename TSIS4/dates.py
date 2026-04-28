# #1
import datetime

x = datetime.datetime.now()

print(x)

# #2
import datetime

x = datetime.datetime.now()

print(x.year)
print(x.strftime("%A"))

#3
import datetime

x = datetime.datetime(2005, 3, 11)

print(x)

#4
import datetime

x = datetime.datetime(1983, 8, 1)

print(x.strftime("%B"))