# this is a mathematics operational python file for chatbot
from functools import reduce
from operator import sub, mul

from rich.console import Console

console = Console()


def add():
    args = list(map(float, input("Enter a multiple value: ").split()))
    if args:
        console.print("Addition of your values are", style='green bold')
        return sum(args)
    else:
        console.print(
            "Opps! invalid math operation the chat bot is designed for only perform (add,sub,div,mul) operations",
            style="red")
        return ""


def subtraction():
    args = list(map(float, input("Enter a multiple value: ").split()))
    if args:
        console.print("subtraction of your values are", style='green bold')
        return reduce(sub, args)
    else:
        console.print(
            "Opps! invalid math operation the chat bot is designed for only perform (add,sub,div,mul) operations",
            style="red")
        return ""


def multiplication():
    args = list(map(float, input("Enter a multiple value: ").split()))
    if args:
        console.print("Multiplication of your values are", style='green bold')
        return reduce(mul, args)
    else:
        console.print(
            "Opps! invalid math operation the chat bot is designed for only perform (add,sub,div,mul) operations",
            style="red")
        return ""


def division():
    args = list(map(float, input("Enter a multiple value: ").split()))
    if args:
        console.print("Division of your values are", style='green bold')
        return reduce(divmod, args)
    else:
        console.print(
            "Opps! invalid math operation the chat bot is designed for only perform (add,sub,div,mul) operations",
            style="red")
        return ""

# print(add("addition", 1, 1, 1))
# # print(sub("minus", 2, 2))
# print(subtraction("sub", 23, 21))
# print(multiplication('da', 10, 11, 11))
# print(division('div', 1000, 11))
# # response validation functions


# print(division())
# print("List of students: ", x)
# print(type(x))
#
#
# def sample(values):
#     return sum(values)
#
#
# print(sample(x))
# print(subtraction('sub', x))
