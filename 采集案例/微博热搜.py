
# -*- coding: utf-8 -*-
# 采集微博热搜数据

# 导入需要的第三方库
from fake_useragent import UserAgent  # 用于生成随机的User-Agent
import wordcloud  # 用于生成词云图
import requests  # 用于发送HTTP请求
import jieba  # 用于中文分词
import json  # 用于解析JSON格式数据


def get_reap() -> requests.Response:
    """
    发送请求并获取响应数据
    """
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random  # 随机生成一个User-Agent
    }
    url = "https://weibo.com/ajax/side/hotSearch"  # 微博热搜的API接口

    response = requests.get(url=url, headers=headers)  # 发送GET请求
    # print(response.status_code)  # 打印响应状态码
    return response


def get_infor(response: requests.Response) -> None:
    """
    解析响应数据并保存到本地文件中
    """
    infor = json.loads(response.text)  # 将响应数据转换为Python字典类型
    with open("hotSearch.txt", "a") as f:
        hotSearch_top_data = infor["data"]["hotgovs"][0]["note"]  # 获取置顶热搜
        f.write(hotSearch_top_data + "\n")  # 将置顶热搜保存到文件中
        for num in range(0, 50):
            hotSearch_data = infor["data"]["realtime"][num]["note"]  # 获取实时热搜
            f.write(str(hotSearch_data) + "\n")  # 将实时热搜保存到文件中

    return None


def get_wordcloud() -> None:
    """
    生成词云图并保存到本地文件中
    """
    with open("hotSearch.txt", "r", encoding="gbk") as f:
        words_list = jieba.lcut(f.read())  # 对文本进行中文分词
        words_list_new = []
        words_delete = []  # 需要过滤掉的无用词语
        stopwords = set()
        # 获取停用词表
        with open("cn_stopwords.txt", "r", encoding="utf-8") as file:
            for line in file:
                word = line.strip()
                stopwords.add(word)
        for words in words_list:
            if words in words_delete or words in stopwords:
                continue
            else:
                words_list_new.append(words)  # 将有用的词语添加到列表中
        txt = " ".join(words_list_new)  # 将词语列表转换为字符串
        # 根据需求调整词云图
        wordcloud_photo = wordcloud.WordCloud(font_path="msyh.ttc",  # 设置字体
                                              background_color="white",  # 设置背景颜色
                                              width=1000,  # 设置宽度
                                              height=700  # 设置高度
                                              )
        wordcloud_photo.generate(txt)  # 生成词云图
        wordcloud_photo.to_file("hotSearch.png")  # 将词云图保存到文件中

    return None


def main():
    """
    主函数，用于控制整个程序流程
    """
    response = get_reap()  # 获取响应数据
    get_infor(response)  # 解析数据并保存到文件中
    get_wordcloud()  # 生成词云图


if __name__ == '__main__':
    main()


