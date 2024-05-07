# -*- coding: utf-8 -*-

from greenlet import greenlet


def func_a():

    print(1)
    gr_b.switch()
    print(2)
    gr_b.switch()


def func_b():

    print(3)
    gr_a.switch()
    print(4)


gr_a = greenlet(func_a)
gr_b = greenlet(func_b)

gr_a.switch()


