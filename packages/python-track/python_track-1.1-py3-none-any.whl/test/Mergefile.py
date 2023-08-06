from operations import Operations
from Person import Person

no1 = int(input("Enter 1st number"))
no2 = int(input("Enter 2nd no"))
obj = Operations(no1, no2)
print(obj.add())
print(obj.sub())
print(obj.multi())

p = Person('Nikhil')
p.say_hi()
