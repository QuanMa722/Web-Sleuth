# -*- coding: utf-8 -*-

import asyncio


async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return None


async def main():

    print("start")

    task1 = asyncio.create_task(func())
    task2 = asyncio.create_task(func())

    print("complete")

    result1 = await task1
    result2 = await task2

    print(result1, result2)


asyncio.run(main())