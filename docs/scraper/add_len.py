def add_len(thing):
    if isinstance(thing, str):
        return len(thing)

    assert isinstance(thing, list)

    total = 0
    for item in thing:
        total += add_len(item)
    return total


print(add_len(["red", ["green", "blue"]]))
