
# -*- coding: utf-8 -*-

import asyncio


async def others():
    print("start")
    response = await asyncio.sleep(2)
    print("complete", response)


async def func():

    print("start")

    response = await others()

    print("complete", response)


asyncio.run(func())
