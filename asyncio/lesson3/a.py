
# -*- coding: utf-8 -*-

import asyncio


async def func():
    print("test")


result = func()

# loop = asyncio.get_event_loop()
# loop.run_until_complete("task")

asyncio.run(result)  # python 3.7

