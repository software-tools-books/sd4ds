import sys
from importlib import import_module

extra = sys.argv[1]
name = sys.argv[2]

sys.path.insert(0, extra)
loaded = import_module(name)
sys.path = sys.path[1:]
print(loaded)
