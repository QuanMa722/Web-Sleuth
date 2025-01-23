# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import aiofiles
import aiohttp
import asyncio
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)


async def fetch(session, url):
    try:
        ua = UserAgent()
        headers = {
            'User-Agent': ua.random
        }
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            resp_text = await response.text()
            logging.info(f"Successfully fetched {url}, status code: {response.status}")
            await parse(resp_text)

    except Exception as e:
        with open('Failed.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{url}\n')

        logging.error(f"Error fetching {url}: {e}")


async def parse(resp_text):
    text = resp_text
    await pipeline(text)


async def pipeline(text):
    async with aiofiles.open('output.txt', mode='w', encoding='utf-8') as f:
        await f.write(text + '\n')


def task():
    url_list = ['https://www.baidu.com/'] * 1000
    return url_list


async def main():
    url_list = task()
    semaphore = asyncio.Semaphore(10)

    async def sem_fetch(url):
        async with semaphore:
            await fetch(session, url)

    async with aiohttp.ClientSession() as session:
        tasks = [sem_fetch(url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    start_time = time.time()
    try:
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.run(main())
        print(f"Total time: {round((time.time() - start_time), 2)}s")
    except Exception as error:
        logging.error(f"An error occurred: {error}.")