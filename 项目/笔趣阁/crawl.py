# -*- coding: utf-8 -*-

from lxml import etree
import aiohttp
import asyncio
import time


def printt(msg):
    nowt = time.strftime("%H:%M:%S", time.localtime())
    for line in msg.split("\n"):
        print(f"[{nowt}] {line}")


async def fetch(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            html_text = await response.text()
            tree = etree.HTML(html_text)
            chapter = url.split('/')[-1].split('.')[0]
            content = tree.xpath('//div[@id="chaptercontent"]//text()')
            with open(file='fiction.txt', mode='a', encoding='utf-8') as f:
                printt(f"Chapter: {chapter}")
                f.write('\n'.join(content) + '\n')


async def main():
    url_list = [f'https://www.biqg.cc/book/11567/{chapter}.html' for chapter in range(1, 65)]
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())

