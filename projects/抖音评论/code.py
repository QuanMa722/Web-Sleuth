# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import aiohttp
import asyncio
import json


async def get_urls(session, index):
    url = f"https://www.douyin.com/aweme/v1/web/comment/list?"
    cookie = ()
    aweme_id = ()

    params = {
        "aid": 6383,
        "cursor": index,
        "aweme_id": aweme_id,
        "count": 20,
    }

    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "cookie": cookie,
    }

    async with session.get(url, params=params, headers=headers) as response:
        if response.status == 200:

            html_text = await response.text()
            json_data = json.loads(html_text)

            for comment in json_data["comments"]:
                data_dict = {
                    "用户id": comment["user"]["uid"].strip(),
                    "用户名": comment["user"]["nickname"].strip(),
                    "评论时间": comment["create_time"],
                    "IP属地": comment["ip_label"],
                    "点赞数量": comment["digg_count"],
                    "评论内容": comment["text"].strip().replace('\n', ""),
                }

                print(data_dict)


async def main():
    index_list: list = [20, 40, 60]

    async with aiohttp.ClientSession() as session:
        tasks = [get_urls(session, index) for index in index_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
