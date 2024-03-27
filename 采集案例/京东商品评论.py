
# -*- coding: utf-8 -*-
# https://club.jd.com/comment/productPageComments.action

from fake_useragent import UserAgent
import requests


def get_comment():

    url = 'https://club.jd.com/comment/productPageComments.action'

    param = {
        'productId': '100087971262',
        'score': '3',
        'sortType': '5',
        'page': 1,
        'pageSize': '10',
        'isShadowSku': '0',
        'fold': '1',
    }

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    response = requests.get(url=url, headers=headers, params=param)

    for index in response.json()['comments']:
        content = index['content']
        print(content)


if __name__ == '__main__':
    get_comment()
