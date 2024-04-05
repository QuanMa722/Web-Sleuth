
# -*- coding: utf-8 -*-
# https://weibo.com/ajax/side/hotSearch

from fake_useragent import UserAgent
import wordcloud
import requests
import jieba
import json


def get_resp() -> requests.Response:

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

    response = get_resp()

    try:
        with open("search.txt", "a", encoding="utf-8") as f:

            search_json = json.loads(response.text)
            search_top_str = search_json["data"]["hotgovs"][0]["note"]
            f.write(search_top_str + "\n")
            print(f"The top hot search :{search_top_str}")

            for num in range(0, 50):
                search_str = search_json["data"]["realtime"][num]["note"]
                f.write(search_str + "\n")
                print(f"The hot search :{search_str}")

    except Exception as e:
        print(f"An error occurred: {e}")

    return None


def search_wordcloud():

    with open("stopwords.txt", "r", encoding="utf-8") as stop_file:
        stopwords_list = stop_file.readlines()
    stopwords_list = [word.strip() for word in stopwords_list]

    word_delete = []
    stopwords_list.extend(word_delete)

    with open("search.txt", "r", encoding="utf-8") as search_file:
        search_file_read = search_file.read()

    ls = jieba.lcut(search_file_read)
    ls = [word for word in ls if word not in stopwords_list]
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


if __name__ == '__main__':

    try:
        get_data()
        # search_wordcloud()

    except Exception as e:
        print(f"An error occurred: {e}")




