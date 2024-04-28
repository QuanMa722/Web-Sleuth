# -*- coding: utf-8 -*-

import asyncio


async def main():

    loop = asyncio.get_event_loop()

    fut = loop.create_future()

    await fut

asyncio.run(main())
