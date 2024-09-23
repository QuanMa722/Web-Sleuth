# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import aiohttp
import asyncio
import time
import logging

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
            logging.info(f"Fetched {url}, status code {response.status}")

    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")


async def main():
    url_list = ['https://www.baidu.com/'] * 50

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in url_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    time_start = time.time()
    asyncio.run(main())
    time_cost = round((time.time() - time_start), 2)
    logging.info(f"Time cost: {time_cost}s")  # Record running time
