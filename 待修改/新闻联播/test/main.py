# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import logging
import json
import time
import re

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


async def fetch(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            resp_text = await response.text()
            match = re.search(r'(\d{4})年(\d{1,2})月(\d{1,2})日', url)
            formatted_date = f"{match.group(1)}{match.group(2).zfill(2)}{match.group(3).zfill(2)}"
            logging.info(f"Fetched {url}, status code {response.status}")
            await parse(resp_text, formatted_date)

    except Exception as e:
        with open('Failed.txt', mode='a', encoding='utf-8') as f:
            f.write(f'{url}\n')
        logging.error(f"Error fetching {url}: {e}")


async def parse(resp_text, formatted_date):
    soup = BeautifulSoup(resp_text, 'html.parser')
    paragraphs = soup.find_all('p')
    news_items = []
    current_title = None
    current_content = []

    for para in paragraphs:
        strong_tag = para.find('strong')

        if strong_tag and strong_tag.text.strip():
            if current_title:
                news_items.append({
                    'title': current_title,
                    'content': "\n".join(current_content)
                })

            current_title = strong_tag.get_text(strip=True)
            current_content = []
        else:
            current_content.append(para.get_text(strip=True))

    if current_title:
        news_items.append({
            'title': current_title,
            'content': "\n".join(current_content)
        })

    filtered_news_items = [
        news for news in news_items[1:]
        if news['title'] not in ['国内联播快讯', '国际联播快讯', '联播快讯', '网站：http://mrxwlb.com/', '微信搜索：mrxwlb 关注我们！']
    ]
    await pipline(filtered_news_items, formatted_date)


async def pipline(filtered_news_items, formatted_date):
    with open(f'{formatted_date}.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_news_items, f, ensure_ascii=False, indent=4)


async def main():
    with open('201806.txt', mode='r', encoding='utf-8') as f:
        url_list = f.readlines()
        semaphore = asyncio.Semaphore(10)

        async def sem_fetch(url):
            async with semaphore:
                await fetch(session, url)
                await asyncio.sleep(10)

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
