# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import aiohttp
import asyncio


async def fetch(session, page):

    url = 'https://club.jd.com/comment/productPageComments.action'

    param = {
        'productId': '100087971262',
        'score': '3',
        'sortType': '5',
        'page': page,
        'pageSize': '10',
        'isShadowSku': '0',
        'fold': '1',
    }

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    async with session.get(url=url, headers=headers, params=param) as response:
        if response.status == 200:
            html_text = await response.json()

            for index in html_text['comments']:
                content = index['content']
                print(content)


async def main():
    async with aiohttp.ClientSession() as session:

        page_list: list = list(range(1, 10))

        tasks = [fetch(session, page) for page in page_list]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())











