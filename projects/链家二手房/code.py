# -*- coding: utf-8 -*-

from lxml import etree
import aiohttp
import asyncio
import time
import re


async def get_urls(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            html_text = await response.text()
            re_find = '<a class="" href="(.*?)" target="_blank"'
            url_list = re.findall(re_find, html_text)

            async with aiohttp.ClientSession() as session:
                tasks = [get_data(session, url) for url in url_list]
                await asyncio.gather(*tasks)


async def get_data(session, url):
    async with session.get(url) as response:
        if response.status == 200:

            await asyncio.sleep(1)  # quite significant

            html_content = await response.text()
            resp_text = etree.HTML(html_content)

            # find information
            price = resp_text.xpath("//div[@class='overview']//div/span/text()")[2]
            unit_price = resp_text.xpath("//div[@class='overview']//div/span/text()")[3]

            place = (resp_text.xpath("//div[@class='overview']//div/span/a/text()")[0] + " " +
                     resp_text.xpath("//div[@class='overview']//div/span/a/text()")[1] +
                     resp_text.xpath("//div[@class='overview']//div/span/text()")[8]).replace('\xa0', ' ')

            name = resp_text.xpath("//div[@class='overview']//div[@class='communityName']/a/text()")[0]

            house_url = url

            base_key = resp_text.xpath("//div[@class='base']//span/text()")[0:12]
            base_value = resp_text.xpath("//div[@class='base']//li/text()")
            text_list = [value.strip() for value in base_value if value.strip()]
            base_dict = {k: v for k, v in zip(base_key, text_list)}

            transaction_key = resp_text.xpath("//div[@class='transaction']//span[1]/text()")
            transaction_value = resp_text.xpath("//div[@class='transaction']//span[2]/text()")
            transaction_dict = {k: v.strip() for k, v in zip(transaction_key, transaction_value)}

            house_dict = {
                "名称": name,
                "地区": place,
                "总价": price,
                "单价": unit_price,
                "网址": house_url,
            }

            house_dict.update(base_dict)
            house_dict.update(transaction_dict)

            with open(file="data.txt", mode="a", encoding="utf-8") as f:
                f.writelines(str(house_dict) + "\n")

            print(house_dict)


async def main():
    # eg: price: [1, 100], page: [1, 25] total, total: 750 pcs

    for num in [1, 6, 11, 16, 21]:  # test

        start_record = time.time()

        url_list = [f"https://wh.lianjia.com/ershoufang/pg{page}bp1ep100" for page in range(num, num + 5)]

        # For stability considerations, it can be increased as the task increases.
        time.sleep(3)

        async with aiohttp.ClientSession() as session:
            tasks = [get_urls(session, url) for url in url_list]
            await asyncio.gather(*tasks)

        end_record = time.time()

        print("-" * 20)
        speed = round(((len(url_list) * 30) / (end_record - start_record - 3)) * 60)
        print(f"speed: {speed} pcs/min")
        print("-" * 20)


if __name__ == '__main__':
    asyncio.run(main())
