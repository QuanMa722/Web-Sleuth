# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
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


def infor(home_url):
    resp = requests.get(url=home_url, headers=headers)
    resp.encoding = "utf-8"
    soup = BeautifulSoup(resp.text, 'html.parser')

    url_infor = []
    for index, li in enumerate(soup.find_all('li'), start=1):
        a_tag = li.find('a')
        if a_tag:
            href = a_tag['href']
            if len(href) > 15:
                title = a_tag.get_text(strip=True)
                url_infor.append((index - 9, title, href))

    return url_infor


async def fetch(session, file_name, url_info):
    try:
        async with session.get(f"http://www.hxlib.cn/{url_info[2]}", headers=headers) as response:
            response.raise_for_status()
            resp_text = await response.text()
            await parse(file_name, url_info, resp_text)

    except Exception as e:
        logging.error(f"Error fetching {url_info}: {e}")


async def parse(file_name, url_info, resp_text):
    soup = BeautifulSoup(resp_text, 'html.parser')
    for p in soup.find_all('p'):
        text = p.get_text(strip=True)
        if len(text) > 100:
            await pipline(file_name, url_info[0], url_info[1], text)


async def pipline(file_name, index, title, text):
    filename = os.path.join(file_name, f"{index}_{title[1:]}.txt")
    async with aiofiles.open(filename, mode="a", encoding="utf-8") as f:
        await f.write(text + '\n')
    logging.info(f"Fetched: {title}")


async def main():
    file_name = '《明史纪事本末》'
    os.makedirs(file_name, exist_ok=False)

    book_code = 'b3fcec1ad41c275e58a83d09141d9ba2'

    home_url = f'http://www.hxlib.cn/book/{book_code}.html'
    url_infor = infor(home_url)

    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(url):
        async with semaphore:
            await fetch(session, file_name, url)

    async with aiohttp.ClientSession() as session:
        tasks = [sem_fetch(url) for url in url_infor]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")
    except FileExistsError as error:
        logging.error(f"An error occurred: {error}.")
