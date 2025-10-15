import random

def rand_exclude(a: int, b: int, c: int) -> int:
    if c < a or c > b:
        return random.randint(a, b)

    count = (b - a + 1) - 1
    r = random.randint(0, count - 1)
    if r >= (c - a):
        r += 1
    return a + r
