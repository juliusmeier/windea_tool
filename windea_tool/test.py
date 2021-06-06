def print_hello():
    print('Hello World')

# https://stackoverflow.com/questions/3975376/understanding-dict-copy-shallow-or-deep/3975388#3975388
class A:
    def __init__(self,name):
        self.name = name
import copy
A = A("A")
print(A.name)
B = copy.copy(A)
print(B.name)
B.name = "B"
print(B.name)
print(A.name)