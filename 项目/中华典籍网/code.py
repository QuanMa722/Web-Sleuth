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
headers = {'User-Agent': ua.random}


async def fetch(session, book_name, url):
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            resp_text = await response.text()
            await info(book_name, url, resp_text)

    except (aiohttp.ClientError, AttributeError) as e:
        logging.error(f"Error fetching {url}: {e}")


async def info(book_name, url, resp_text):
    soup = BeautifulSoup(resp_text, 'html.parser')
    index = re.search(r"/(\d+)\.html$", url).group(1)
    title = soup.find('h1').get_text().strip()
    filename = os.path.join(book_name, f"{index}_{title}.txt")
    text = soup.find('div', {'id': 'content', 'class': 'panel-body'}).get_text().strip()
    logging.info(f"Fetched: {title}")
    await file(filename, text)


async def file(filename, content):
    async with aiofiles.open(filename, mode='a', encoding='utf-8') as f:
        await f.write(content + '\n')


async def main():
    book_name = 'mingshi'
    os.makedirs(book_name, exist_ok=False)

    page_list = range(4380, 4713)
    url_list = [f"https://www.zhonghuadiancang.com/lishizhuanji/{book_name}/{page}.html" for page in page_list]

    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(url):
        async with semaphore:
            await fetch(session, book_name, url)

    async with aiohttp.ClientSession() as session:
        tasks = [sem_fetch(url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    try:
        asyncio.run(main())
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")
    except FileExistsError as error:
        logging.error(f"An error occurred: {error}.")
