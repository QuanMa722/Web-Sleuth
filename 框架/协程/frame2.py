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
            logging.info(f"Fetched {url}, status code {response.status}")
            await get_info(resp_text)  # Process the fetched text

    except Exception as e:
        logging.error(f"Error fetching {url}: {e}")


async def get_info(resp_text):
    """Process the fetched response text."""
    await write_file(resp_text)  # Call async write_file


async def write_file(content):
    """Asynchronously write the fetched content to a file."""
    async with aiofiles.open('output.txt', mode='a', encoding='utf-8') as file:
        await file.write(content + '\n')


async def main():
    """Main coroutine to manage concurrent fetch operations."""
    url_list = ['https://www.baidu.com/'] * 50

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in url_list]
        await asyncio.gather(*tasks)
        # await asyncio.sleep(1)

if __name__ == '__main__':
    start_time = time.time()
    try:
        asyncio.run(main())
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")
    except Exception as error:
        logging.error(f"An error occurred: {error}.")






