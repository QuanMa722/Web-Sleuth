# -*- coding: utf-8 -*-

from crawl import CSVDuplicatesRemover
from crawl import CommentFetcher
import asyncio
import time

# Individual Product Review Collection
# product_id = '100066896356'
# file_path = 'comments.csv'
# comment_fetcher = CommentFetcher(file_path, product_id)
# asyncio.run(comment_fetcher.main())

# data storage address
file_path = 'comments.csv'
# Product ID List
product_id_list: list = ['100015381842', '100039032489', '100112475212', '100047641695', '100097484090']

for product_id in product_id_list:
    comment_fetcher = CommentFetcher(file_path, product_id)
    asyncio.run(comment_fetcher.main())
    time.sleep(5)

# Removal of duplicate data.
remover = CSVDuplicatesRemover(file_path)
remover.remove_duplicates()
