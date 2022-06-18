from struct import pack

print(repr(pack("3i", 1, 2, 3)))
print(repr(pack("5s", bytes("hello", "utf-8"))))
print(repr(pack("5s", bytes("a longer string", "utf-8"))))
