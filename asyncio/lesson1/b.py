
# -*- coding: utf-8 -*-

def func_a():

    yield 1
    yield from func_b()
    yield 2


def func_b():

    yield 3
    yield 4


f = func_a()
for item in f:
    print(item)

