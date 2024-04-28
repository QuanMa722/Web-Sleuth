from asyncio import Task
from asyncio.tasks import _T
from typing import List

# -*- coding: utf-8 -*-

import aiohttp
import asyncio


async def fetch(session, url):
    print("start", url)
    async with session.get(url, verify_ssl=False) as response:
        content = await response.content.read()
        file_name = url.rsplit("-")[-1]

        with open(file_name, mode="wb") as file_object:
            file_object.write(content)

        print("complete")


async def main():
    async with aiohttp.ClientSession() as session:
        url_list = [

            "https://images.hdqwalls.com/wallpapers/python-logo-4k-i6.jpg",
            "https://images.hdqwalls.com/wallpapers/python-logo-4k-i6.jpg",
            "https://images.hdqwalls.com/wallpapers/python-logo-4k-i6.jpg",

        ]
        tasks: list[Task[_T] | Task[_T] | Task[_T]] = [asyncio.create_task(fetch(session, url)) for url in url_list]

        await asyncio.wait(tasks)


if __name__ == '__main__':

    asyncio.run(main())
