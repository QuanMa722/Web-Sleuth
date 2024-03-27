
# -*- coding: utf-8 -*-
# https://www.zhonghuadiancang.com/lishizhuanji/mingshi

from bs4 import BeautifulSoup
from urllib import request


def get_data():

    url = "https://www.zhonghuadiancang.com/lishizhuanji/mingshi/4380.html"
    response = request.urlopen(url)

    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')

    title_str = soup.find('h1').get_text().strip()
    text_str = soup.find('div', {'id': 'content', 'class': 'panel-body'}).get_text().strip()

    return title_str, text_str


if __name__ == '__main__':

    try:

        title_str, text_str = get_data()
        print(title_str)
        print(text_str)

    except Exception as e:

        print(f"An error occurred: {e}")


