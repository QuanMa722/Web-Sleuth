# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import time
import os

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


def printt(msg):
    nowt = time.strftime("%H:%M:%S", time.localtime())
    for line in str(msg).split("\n"):
        print(f"[{nowt}] {line}")


async def fetch(session, book_name, url):
    try:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')

                title: str = soup.find('h1').get_text().strip()
                text: str = soup.find('div', {'id': 'content', 'class': 'panel-body'}).get_text().strip()

                filename = os.path.join(book_name, str(title) + '.txt')

                printt(title)
                with open(filename, mode="w", encoding="utf-8") as f:
                    f.write(text)

            else:
                printt(f"Failed to fetch {url}, status code: {response.status}")

    except aiohttp.ClientError as e:
        printt(f"Error fetching {url}: {e}")


async def main():
    book_name = 'mingshi'
    os.makedirs(book_name, exist_ok=False)

    page_list = range(4380, 4713)
    url_list = [f"https://www.zhonghuadiancang.com/lishizhuanji/{book_name}/{page}.html" for page in page_list]

    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(url):
        async with semaphore:
            await fetch(session, book_name, url)
            # await asyncio.sleep(1)

    async with aiohttp.ClientSession() as session:
        tasks = [sem_fetch(url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        time_start = time.time()
        asyncio.run(main())
        printt(f"Time cost: {round((time.time() - time_start), 2)}s")

    except FileExistsError as error:
        printt(f"An error occurred: {error}.")
