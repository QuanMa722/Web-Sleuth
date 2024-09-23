# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import aiohttp
import asyncio
import time

# Construct request headers
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


# Time log
def printt(msg):
    nowt = time.strftime("%H:%M:%S", time.localtime())
    for line in str(msg).split("\n"):
        print(f"[{nowt}] {line}")


async def fetch(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html_text = await response.text()
                printt(f"Fetched {url}, status code {response.status}")

            else:
                printt(f"Failed to fetch {url}, status code: {response.status}")
    except Exception as e:
        printt(f"Error fetching {url}: {e}")


async def main():
    url_list = ['https://www.baidu.com/'] * 50
    semaphore = asyncio.Semaphore(10)  # 限制并发限制

    async def sem_fetch(url):
        async with semaphore:
            await fetch(session, url)
            # await asyncio.sleep(1)

    async with aiohttp.ClientSession() as session:
        tasks = [sem_fetch(url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    time_start = time.time()
    asyncio.run(main())
    printt(f"Time cost: {round((time.time() - time_start), 2)}s")

