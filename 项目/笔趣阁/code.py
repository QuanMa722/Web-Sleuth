# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from lxml import etree
import aiofiles
import aiohttp
import asyncio
import logging
import time
import os

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


async def fetch(session, url, book_name):
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            resp_text = await response.text()
            # logging.info(f"Fetched {url}, status code {response.status}")
            await info(url, resp_text, book_name)

    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")


async def info(url, resp_text, book_name):
    tree = etree.HTML(resp_text)
    index = url.split('/')[-1].split('.')[0]
    title = tree.xpath('//h1[@class="wap_none"]//text()')[0]
    text = tree.xpath('//div[@id="chaptercontent"]//text()')
    file_name = os.path.join(book_name, f"{index}_{title}.txt")
    logging.info(f"Fetched: {title}")
    await file(file_name, text)


async def file(file_name, text):
    async with aiofiles.open(file_name, mode="a", encoding="utf-8") as f:
        await f.write('\n'.join(text) + '\n')


async def main():
    book_name = '万历十五年'
    os.makedirs(book_name, exist_ok=False)

    book_index = 11567
    page_list = list(range(1, 64))

    url_list = [f'https://www.biqg.cc/book/{book_index}/{chapter}.html' for chapter in page_list]
    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(url):
        async with semaphore:
            await fetch(session, url, book_name)

    async with aiohttp.ClientSession() as session:
        tasks = [sem_fetch(url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    try:
        asyncio.run(main())
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")
    except Exception as error:
        logging.error(f"An error occurred: {error}.")
