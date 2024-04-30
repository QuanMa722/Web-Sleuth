# -*- coding: utf-8 -*-

import aiohttp
import asyncio


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            # locate information
            print(response.text)


async def main():
    async with aiohttp.ClientSession() as session:
        # your task list
        url_list: list = ["https://www.baidu.com"]

        tasks = [fetch(session, url) for url in url_list]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())











