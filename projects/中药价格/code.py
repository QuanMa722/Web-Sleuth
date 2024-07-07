# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import aiohttp
import asyncio
import json
import re


async def fetch(session, index):
    url = "https://www.yt1998.com/price/nowDayPriceQ!getPriceList.do"

    params = {
        'random': '0.35934104418089574',
        'ycnam': '',
        'market': '1',
        'leibie': '',
        'istoday': '0',
        'spices': '',
        'tea': '',
        'logo_flg': '',
        'paramName': '',
        'paramValue': '',
        'pageIndex': index,
        'pageSize': '20',
    }

    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
    }

    async with session.get(url, params=params, headers=headers) as response:
        if response.status == 200:

            html_text = await response.text()

            resp_dict = json.loads(html_text)["ming"]
            item = resp_dict[0]

            data_dict = {
                "品名": item["ycnam"],
                "规格": item["guige"],
                "产地": item["chandi"],
                "价格（元/kg）": item["pri"],
                "走势": item["zoushi"],
                "昨日对比": re.search(r'>(.*?)<', item["yesterday"]).group(1),
                "周对比": re.search(r'>(.*?)<', item["zhouduibi"]).group(1),
                "月对比": re.search(r'>(.*?)<', item["yueduibi"]).group(1),
                "季度对比": re.search(r'>(.*?)<', item["jiduibi"]).group(1),
                "年对比": re.search(r'>(.*?)<', item["nianduibi"]).group(1),
                "日期": item["dtm"],
            }

            print(data_dict)


async def main():

    index_list: list = list(range(30))

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, index) for index in index_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
