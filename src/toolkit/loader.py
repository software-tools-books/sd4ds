import sys
from importlib import import_module

name = sys.argv[1]
loaded = import_module(name)
print(loaded)
loaded.f(3)
