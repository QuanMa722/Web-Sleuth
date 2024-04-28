
# -*- coding: utf-8 -*-

import asyncio


async def others():
    print("start")
    response = await asyncio.sleep(2)  # wait
    print("complete", response)


async def func():

    print("start")

    response1 = await others()

    print("complete", response1)

    response2 = await others()

    print("complete", response2)


asyncio.run(func())

# 7
