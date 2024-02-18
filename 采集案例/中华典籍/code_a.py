
# -*- coding: utf-8 -*-
# https://www.zhonghuadiancang.com/lishizhuanji/mingshi

from bs4 import BeautifulSoup
from urllib import request


def get_data():

    url = "https://www.zhonghuadiancang.com/lishizhuanji/mingshi/4380.html"
    response = request.urlopen(url)

    html = response.read().decode("utf-8")
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('h1').get_text().strip()
    text = soup.find('div', {'id': 'content', 'class': 'panel-body'}).get_text().strip()

    print(title)
    print(text)


if __name__ == '__main__':
    try:
        get_data()
    except Exception as e:
        print(f"An error occurred: {e}")


