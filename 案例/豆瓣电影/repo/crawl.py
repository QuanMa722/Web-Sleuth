# -*- coding: utf-8 -*-

from hconfig import HeadCook
from lxml import etree
import requests
import logging
import time
import json
import re
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)


class Crawl:

    def __init__(self):
        self.headers = HeadCook.headers
        self.cookies = HeadCook.cookies

    def fetch(self, movie_id):
        try:
            os.makedirs(movie_id, exist_ok=False)

            all_comments = []

            for page in range(0, 381, 20):
                url = f'https://movie.douban.com/subject/{movie_id}/comments?start={page}&limit=20&&sort=new_score&status=P'
                response = requests.get(url, headers=self.headers, cookies=self.cookies)
                response_text = response.text

                time.sleep(1)

                logging.info(f'Fetched page {page + 20}')
                all_comments.extend(self.parse(response_text))
            self.pipline(all_comments, movie_id)

        except requests.RequestException as e:
            logging.error(f"Error fetching: {e}")

        except FileExistsError:
            print(f'File {movie_id} already exists.')

    @staticmethod
    def parse(response_text):

        tree = etree.HTML(response_text)
        comment_list = tree.xpath('//div[@class="comment-item "]')
        comments_list = []

        for comment_div in comment_list:
            name = comment_div.xpath('.//span[@class="comment-info"]/a/text()')
            name = name[0].strip() if name else ''

            comment = comment_div.xpath('.//p[@class=" comment-content"]/span/text()')
            comment = comment[0].strip() if comment else ''

            upvote = comment_div.xpath('.//span[@class="votes vote-count"]/text()')
            upvote = upvote[0].strip() if upvote else '0'

            comment_time = comment_div.xpath('.//span[@class="comment-time "]/@title')
            comment_time = comment_time[0] if comment_time else ''

            star_attribute = comment_div.xpath('.//span[contains(@class,"rating")]/@class')
            stars = 0
            if star_attribute:
                stars = int(re.search(r'\d+', star_attribute[0]).group())

            comment_data = {
                'name': name,
                'comment': comment,
                'upvote': upvote,
                'time': comment_time,
                'stars': stars
            }
            comments_list.append(comment_data)

        return comments_list

    @staticmethod
    def pipline(comments_list, movie_id):
        try:
            with open(f'{movie_id}/comments.json', 'a', encoding='utf-8') as file:
                json.dump(comments_list, file, ensure_ascii=False, indent=4)
                logging.info(f'Successfully saved {len(comments_list)} comments.')

        except Exception as e:
            logging.error(f'Error saving data: {e}')



