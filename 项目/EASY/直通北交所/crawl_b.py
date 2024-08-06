# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import aiohttp
import asyncio
import json
import re


async def fetch(session, page):

    url = r"https://www.tobse.cn/specialized/enterprise/"

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    data = {
        "p": page,
        "key": "",
        "level": 0,
        "cat": "",
        "prov": 0,
        "city": 0,
        "ipo": 0,
        "licence_status": "",
    }

    async with session.post(url=url, headers=headers, data=data) as response:
        if response.status == 200:

            await asyncio.sleep(1)

            html_text = await response.text()
            text_json = json.loads(html_text)["pageView"]

            find_text = re.findall(r'<td>(.*?)</td>', text_json)
            elements = find_text[1:]
            filtered_elements = [el for el in elements if not re.match(r'<.*?>', el)]

            num = int(len(filtered_elements) / 6)
            count = 0
            for _ in range(num):
                infor = filtered_elements[count:count + 6]

                print(infor)
                count += 6


async def main():
    async with aiohttp.ClientSession() as session:

        page_list: list = list(range(1, 11))

        tasks = [fetch(session, page) for page in page_list]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())











