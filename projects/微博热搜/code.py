# -*- coding: utf-8 -*-
# https://weibo.com/ajax/side/hotSearch

from fake_useragent import UserAgent
import wordcloud
import requests
import jieba
import json


def get_resp() -> requests.Response:
    """
    发送请求
    :return: response
    """

    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    url = "https://weibo.com/ajax/side/hotSearch"

    response = requests.get(url=url, headers=headers)

    status_code = response.status_code
    if status_code != 200:
        print("An error with response.")

    return response


def get_data() -> None:
    """
    获取数据
    :return: None
    """

    response = get_resp()

    try:
        with open(file="search.txt", mode="a", encoding="utf-8") as f:

            search_json = json.loads(response.text)
            search_top: str = search_json["data"]["hotgovs"][0]["note"]
            f.write(search_top + "\n")
            print(f"The top hot search :{search_top}")

            for num in range(0, 50):
                search: str = search_json["data"]["realtime"][num]["note"]
                f.write(search + "\n")
                print(f"The hot search :{search}")

    except Exception as e:
        print(f"An error occurred: {e}")

    return None


def search_wordcloud() -> None:
    """
    绘制词云图
    :return: None
    """

    with open("stopwords.txt", mode="r", encoding="utf-8") as stop_file:
        stopwords: list = stop_file.readlines()
    stopwords = [word.strip() for word in stopwords]

    word_delete: list = []
    stopwords.extend(word_delete)

    with open("search.txt", "r", encoding="utf-8") as search_file:
        search_file_read = search_file.read()

    ls = jieba.lcut(search_file_read)
    ls = [word for word in ls if word not in stopwords]
    txt = " ".join(ls)

    word_cloud = wordcloud.WordCloud(
        font_path="msyh.ttc",
        width=1000,
        height=700,
        background_color="white",
                           )
    word_cloud.generate(txt)

    word_cloud.to_file("search_wordcloud.png")

    return None


def main():

    try:
        # 获取数据并写入txt文件中
        get_data()

        # 词云图
        # search_wordcloud()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()






