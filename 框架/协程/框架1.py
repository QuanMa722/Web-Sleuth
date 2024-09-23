# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import logging
import aiohttp
import asyncio
import time

# Setting Up Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('scraper.log', 'a', 'utf-8'),
              logging.StreamHandler()]
)

# Construct request headers
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


async def fetch(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            html_text = await response.text()
            message = f"Fetched {url}, status code {response.status}"
            logging.info(message)  # 记录日志

    except Exception as e:
        error_message = f"Error fetching {url}: {e}"
        logging.error(error_message)  # 记录错误日志


async def main():
    url_list = ['https://www.baidu.com/'] * 50
    semaphore = asyncio.Semaphore(10)  # 限制并发限制

    async def sem_fetch(url):
        async with semaphore:
            await fetch(session, url)

    async with aiohttp.ClientSession() as session:
        tasks = [sem_fetch(url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    time_start = time.time()
    asyncio.run(main())
    time_cost = round((time.time() - time_start), 2)
    logging.info(f"Time cost: {time_cost}s")  # Record running time
