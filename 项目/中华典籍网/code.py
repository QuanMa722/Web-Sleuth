# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import aiofiles
import asyncio
import aiohttp
import logging
import time
import os
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


async def fetch(session, file_name, url):
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            resp_text = await response.text()
            await parse(file_name, url, resp_text)

    except (aiohttp.ClientError, AttributeError) as e:
        logging.error(f"Error fetching {url}: {e}")


async def parse(file_name, url, resp_text):
    index = re.search(r"/(\d+)\.html$", url).group(1)
    soup = BeautifulSoup(resp_text, 'html.parser')
    title = soup.find('h1').get_text().strip()
    filename = os.path.join(file_name, f"{index}_{title}.txt")
    text = soup.find('div', {'id': 'content', 'class': 'panel-body'}).get_text().strip()
    logging.info(f"Fetched: {title}")
    await pipline(filename, text)


async def pipline(filename, content):
    async with aiofiles.open(filename, mode='a', encoding='utf-8') as f:
        await f.write(content + '\n')


async def main():
    file_name: str = '明史'
    os.makedirs(file_name, exist_ok=False)

    book_name: str = 'mingshi'
    page_start: int = 4380
    page_end: int = 4712

    page_list = list(range(page_start, page_end + 1))
    url_list = [f"https://www.zhonghuadiancang.com/lishizhuanji/{book_name}/{page}.html" for page in page_list]

    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(url):
        async with semaphore:
            await fetch(session, file_name, url)

    async with aiohttp.ClientSession() as session:
        tasks = [sem_fetch(url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")
    except FileExistsError as error:
        logging.error(f"An error occurred: {error}.")
