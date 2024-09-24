# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from aiohttp import ClientTimeout
import logging
import asyncio
import aiohttp
import time
import csv
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('scraper.log', 'a', 'utf-8'),
              logging.StreamHandler()]
)

url = 'https://club.jd.com/comment/productPageComments.action'
timeout = ClientTimeout(total=10)


async def fetch(session, product_id, page, score):
    params = {
        'productId': product_id,
        'score': score,
        'sortType': '5',
        'page': page,
        'pageSize': '10',
        'isShadowSku': '0',
        'fold': '1',
    }

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    try:
        async with session.get(url, headers=headers, params=params, timeout=timeout) as response:
            response.raise_for_status()
            return await response.json()

    except asyncio.TimeoutError:
        logging.warning(f"Timeout fetching page {page} for score {score}")
        return {'comments': []}

    except aiohttp.ClientResponseError as e:
        logging.error(f"Error fetching page {page} for score {score}: {e}")
        return {'comments': []}


async def write_to_csv(data_list, filename):
    try:
        if os.path.isfile(filename):
            raise FileExistsError(f"The file '{filename}' already exists")

        file_exists = os.path.isfile(filename)
        with open(filename, mode='a', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['Nickname', 'Time', 'Location', 'Content', 'Goods', 'Score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists or os.stat(filename).st_size == 0:
                writer.writeheader()

            existing_entries = set()
            for entry in data_list:
                entry_tuple = tuple(entry.values())
                if entry_tuple not in existing_entries:
                    writer.writerow(entry)
                    existing_entries.add(entry_tuple)
                    logging.info(f"Added unique entry: {entry}")
                else:
                    logging.info(f"Skipped duplicate entry: {entry}")

    except FileNotFoundError:
        logging.error(f"File '{filename}' not found.")


async def main(file_path, product_id):
    async with aiohttp.ClientSession() as session:
        score_list = list(range(6))
        page_list = list(range(101))
        data_to_write = []

        tasks = []
        for score in score_list:
            for page in page_list:
                tasks.append(fetch(session, product_id, page, score))

        results = await asyncio.gather(*tasks)

        for score, comments in enumerate(results):
            for comment in comments.get('comments', []):
                data_to_write.append({
                    'Nickname': comment['nickname'],
                    'Time': comment['creationTime'],
                    'Location': comment.get('location', '未知'),
                    'Content': comment['content'],
                    'Goods': comment['referenceName'],
                    'Score': comment['score']
                })

        await write_to_csv(data_to_write, file_path)


if __name__ == '__main__':
    start_time = time.time()
    try:
        file_path = 'comments.csv'
        product_id = '100066896356'
        asyncio.run(main(file_path, product_id))
        logging.info(f"Time cost: {round((time.time() - start_time), 2)}s")
    except FileExistsError as error:
        logging.error(f"An error occurred: {error}.")
