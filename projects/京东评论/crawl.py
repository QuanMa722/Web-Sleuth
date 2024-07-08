# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from aiohttp import ClientTimeout
import pandas as pd
import asyncio
import aiohttp
import csv
import os


class CommentFetcher:

    def __init__(self, file_path, product_id):
        self.file_path = file_path
        self.product_id = product_id
        self.url = 'https://club.jd.com/comment/productPageComments.action'
        self.timeout = ClientTimeout(total=10)

    async def fetch(self, session, page, score):
        params = {
            'productId': self.product_id,
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
            async with session.get(self.url, headers=headers, params=params, timeout=self.timeout) as response:
                return await response.json()

        except asyncio.TimeoutError:
            print(f"Timeout fetching page {page} for score {score}")
            return {'comments': []}

        except aiohttp.ClientResponseError as e:
            print(f"Error fetching page {page} for score {score}: {e}")
            return {'comments': []}

    async def write_to_csv(self, data_list, filename):
        try:
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
                        print(f"Added unique entry: {entry}")
                    else:
                        print(f"Skipped duplicate entry: {entry}")

        except FileNotFoundError:
            print(f"File '{filename}' not found.")

    async def main(self):
        async with aiohttp.ClientSession() as session:

            score_list = range(6)
            page_list = range(1, 101)
            data_to_write = []

            tasks = []
            for score in score_list:
                for page in page_list:
                    task = self.fetch(session, page, score)
                    tasks.append(task)

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

            filename = self.file_path
            await self.write_to_csv(data_to_write, filename)
            print("Done")


class CSVDuplicatesRemover:

    def __init__(self, file_path):
        self.file_path = file_path

    def remove_duplicates(self):
        df = pd.read_csv(self.file_path, encoding='utf-8-sig')
        df_deduped = df.drop_duplicates()
        df_deduped.to_csv(self.file_path, index=False, encoding='utf-8-sig')
        print(f"Deduplicated data saved to {self.file_path}")


if __name__ == '__main__':
    file_path = 'comments.csv'
    product_id = '100066896356'
    comment_fetcher = CommentFetcher(file_path, product_id)
    asyncio.run(comment_fetcher.main())

