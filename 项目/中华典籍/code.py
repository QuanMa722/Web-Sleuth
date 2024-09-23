# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import logging
import asyncio
import aiohttp
import time
import os
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('scraper.log', 'a', 'utf-8'),
              logging.StreamHandler()]
)

ua = UserAgent()
headers = {'User-Agent': ua.random}


async def fetch(session, book_name, url):
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()

            html_text = await response.text()
            title, text = parse_html(html_text)
            index = re.search(r"/(\d+)\.html$", url).group(1)
            filename = os.path.join(book_name, f"{index}_{title}.txt")

            with open(filename, mode="w", encoding="utf-8") as f:
                f.write(text)
            logging.info(f"Fetched: {title}")

    except (aiohttp.ClientError, AttributeError) as e:
        logging.error(f"Error fetching {url}: {e}")


def parse_html(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    title = soup.find('h1').get_text().strip()
    text = soup.find('div', {'id': 'content', 'class': 'panel-body'}).get_text().strip()
    return title, text


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
    start_time = time.time()
    try:
        asyncio.run(main())
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")
    except FileExistsError as error:
        logging.error(f"An error occurred: {error}.")
