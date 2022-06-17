"""Docstring for module"""

def f(x):
    print(f"before {x}")
    locals()["x"] = 9
    print(f"after {x}")

if __name__ == '__main__':
    f(3)
