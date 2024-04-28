
# -*- coding: utf-8 -*-

import asyncio


async def func_a():
    print(1)
    await asyncio.sleep(1)  # 遇到阻塞时会自动切换
    print(2)


async def func_b():
    print(3)
    await asyncio.sleep(1)
    print(4)


async def main():
    tasks = [
        asyncio.create_task(func_a()),
        asyncio.create_task(func_b())
    ]
    await asyncio.gather(*tasks)


asyncio.run(main())

