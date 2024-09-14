# -*- coding: utf-8 -*-

import aiohttp
import asyncio


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            html_text = await response.text()
            # locate information
            print('Done')


async def main():
    # your task list
    url_list: list = [
        "https://www.baidu.com",
        "https://www.baidu.com",
        "https://www.baidu.com",
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in url_list]
        await asyncio.gather(*tasks)
        await asyncio.sleep(1)


if __name__ == '__main__':
    asyncio.run(main())
