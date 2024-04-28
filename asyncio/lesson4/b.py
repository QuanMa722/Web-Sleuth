# -*- coding: utf-8 -*-

import asyncio


async def func():
    print(1)
    await asyncio.sleep(2)
    print(2)
    return None


async def main():

    print("start")

    task_list = [
        asyncio.create_task(func(), name="n1"),
        asyncio.create_task(func(), name="n2"),
    ]

    print("complete")

    done, pending = await asyncio.wait(task_list, timeout=None)

    print(done)


asyncio.run(main())