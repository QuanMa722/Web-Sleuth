# -*- coding: utf-8 -*-

from crawl import CSVDuplicatesRemover
from crawl import CommentFetcher
import asyncio
import time

# 单个商品评论采集
# product_id = '100066896356'
# file_path = 'comments.csv'
# comment_fetcher = CommentFetcher(file_path, product_id)
# asyncio.run(comment_fetcher.main())

# 数据存放地址
file_path = 'comments.csv'
# 商品ID列表
product_id_list: list = ['100015381842', '100039032489', '100112475212', '100047641695', '100097484090']

for product_id in product_id_list:
    comment_fetcher = CommentFetcher(file_path, product_id)
    asyncio.run(comment_fetcher.main())
    time.sleep(5)

# 去除重复数据
remover = CSVDuplicatesRemover(file_path)
remover.remove_duplicates()
