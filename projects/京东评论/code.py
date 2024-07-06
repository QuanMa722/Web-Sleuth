# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import aiohttp
import asyncio
import csv


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
            return html_text['comments']


async def write_to_csv(data_list, filename):

    with open(file=filename, mode='a', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['Nickname', 'Creation Time', 'Location', 'Content']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if csvfile.tell() == 0:
            writer.writeheader()
        for entry in data_list:
            writer.writerow(entry)


async def main():
    async with aiohttp.ClientSession() as session:
        page_list = list(range(1, 10))

        tasks = [fetch(session, page) for page in page_list]
        results = await asyncio.gather(*tasks)

        data_to_write = []
        for comments in results:
            for comment in comments:
                nickname = comment['nickname']
                time = comment['creationTime']
                location = comment['location']
                content = comment['content']

                data_to_write.append({
                    'Nickname': nickname,
                    'Creation Time': time,
                    'Location': location,
                    'Content': content
                })

        filename = 'comments.csv'
        await write_to_csv(data_to_write, filename)
        print("Done")

if __name__ == '__main__':
    asyncio.run(main())
