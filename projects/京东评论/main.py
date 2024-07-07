# -*- coding: utf-8 -*-

from duplicate import CSVDuplicatesRemover
from crawl import CommentFetcher
import asyncio
import time

# product_id = '100066896356'
# comment_fetcher = CommentFetcher(product_id)
# asyncio.run(comment_fetcher.main())

# goods list
file_path = 'comments.csv'
product_id_list: list = ['100015381842', '100039032489', '100112475212', '100047641695', '100097484090']

for product_id in product_id_list:
    comment_fetcher = CommentFetcher(file_path, product_id)
    asyncio.run(comment_fetcher.main())
    time.sleep(5)

remover = CSVDuplicatesRemover(file_path)
remover.remove_duplicates()
