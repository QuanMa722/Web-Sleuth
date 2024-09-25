# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import aiofiles
import aiohttp
import asyncio
import logging
import time

# Setting up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)

# Construct request headers
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


async def fetch(session, url):
    """Fetch content from a URL asynchronously."""
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            resp_text = await response.text()
            # resp_json = await response.json()
            logging.info(f"Fetched {url}, status code {response.status}")
            await info(resp_text)  # Process the fetched text

    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")


async def info(resp_text):
    """Process the fetched response text."""
    text = resp_text
    ...
    await file(text)  # Call async write_file


async def file(text):
    """Asynchronously write the fetched content to a file."""
    ...
    async with aiofiles.open('output.txt', mode='a', encoding='utf-8') as f:
        await f.write(text + '\n')


async def main():
    """Main coroutine to manage concurrent fetch operations."""
    ...
    url_list = ['https://www.baidu.com/'] * 10
    semaphore = asyncio.Semaphore(10)  # Limiting concurrency

    async def sem_fetch(url):
        async with semaphore:
            await fetch(session, url)
            # await asyncio.sleep(1)

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
