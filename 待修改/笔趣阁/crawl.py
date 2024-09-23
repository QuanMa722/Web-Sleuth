# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from lxml import etree
import aiohttp
import asyncio
import time

# 构造请求头
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


# 时间日志
def printt(msg):
    nowt = time.strftime("%H:%M:%S", time.localtime())
    for line in msg.split("\n"):
        print(f"[{nowt}] {line}")


async def fetch(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html_text = await response.text()
                tree = etree.HTML(html_text)
                index = url.split('/')[-1].split('.')[0]
                content = tree.xpath('//div[@id="chaptercontent"]//text()')

                with open('fiction_raw.txt', mode='a', encoding='utf-8') as f:
                    printt(f"Index: {index}")
                    f.write('\n'.join(content) + '\n')
            else:
                printt(f"Failed to fetch {url}: Status code {response.status}")
    except Exception as e:
        printt(f"Error fetching {url}: {e}")


async def main():
    url_list = [f'https://www.biqg.cc/book/11567/{chapter}.html' for chapter in range(1, 64)]
    semaphore = asyncio.Semaphore(10)  # 限制并发限制

    async def sem_fetch(url):
        async with semaphore:
            await fetch(session, url)

    async with aiohttp.ClientSession() as session:
        tasks = [sem_fetch(url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(main())
    printt(f"Time: {round(time.time() - start_time, 2)} seconds")

    # 处理数据
    with open('fiction_raw.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()

    with open('fiction_process.txt', mode='a', encoding='utf-8') as f:
        for line in lines:
            if line.strip() not in {'『点此报错』', '『加入书签』',
                                    '请收藏本站：https://www.bigee.cc。笔趣阁手机版：https://m.bigee.cc'}:
                f.write(line)
