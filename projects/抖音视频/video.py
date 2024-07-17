# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from time import localtime, strftime, time
from urllib.parse import unquote, quote
from requests import get, head, post
from fake_useragent import UserAgent
from json import loads, dump
from os import mkdir, path
from re import findall
import lxml.html
import uuid
import json
import csv
import os
import re

etree = lxml.html.etree
def get_tt():
    url = "https://ttwid.bytedance.com/ttwid/union/register/"
    json = {"region": "cn", "aid": 1768, "needFid": "false", "service": "www.ixigua.com",
            "migrate_info": {"ticket": "", "source": "node"}, "cbUrlProtocol": "https", "union": "true"}
    response = post(url, json=json)
    tt = response.cookies.get_dict()['ttwid']
    return tt

def get_aweme(aweme_id):

    time_1 = int(time())
    # 转换成localtime
    time_2 = localtime(time_1)
    # 转换成新的时间格式
    file = strftime("%Y-%m-%d", time_2)

    ua = UserAgent()
    headers = {
        "referer": "https://www.douyin.com/",
        "user-agent": ua.random,
        "cookie": "ttwid=" + get_tt()
    }

    url = f"https://www.iesdouyin.com/share/video/{aweme_id}"
    resp = get(url=url, headers=headers).text.encode('gbk', errors='ignore').decode('gbk')

    print(resp)
    tree = etree.HTML(resp)
    print("-" * 30)
    # 使用XPath表达式提取<head>和<body>之间的内容
    # 注意：这个表达式假定<head>标签后面紧跟<body>标签
    content_to_extract = tree.xpath('/html/head/following-sibling::*[1]')

    # 打印提取的内容
    for element in content_to_extract:
        print(etree.tostring(element, pretty_print=True, encoding='unicode'))

    # resp = json.loads(resp)
    #
    # print(resp)
    #
    # resp = unquote(resp).encode('gbk', errors='ignore').decode('gbk')
    # resp = json.loads(resp)
    # desc = resp["app"]["videoInfoRes"]["item_list"][0]["statistics"]
    # desc['收藏'] = desc.pop('collect_count')
    # desc['评论'] = desc.pop('comment_count')
    # desc['点赞'] = desc.pop('digg_count')
    # desc['分享'] = desc.pop('share_count')
    # desc['格式'] = "video"
    # desc.pop("play_count")
    # desc['作品id'] = str(resp["app"]["videoInfoRes"]["item_list"][0]["aweme_id"])
    # time_1 = int(resp["app"]["videoInfoRes"]["item_list"][0]["create_time"])
    # time_2 = localtime(time_1)
    # # 转换成新的时间格式
    # desc['时间'] = strftime("%Y-%m-%d %H:%M:%S", time_2)
    # desc['标题'] = resp["app"]["videoInfoRes"]["item_list"][0]['desc']
    # list_titles = ["作品id", "时间", "标题", "格式", "收藏", "评论", "点赞", "分享"]
    # values_tuple = ()
    # iiia = ""
    # for iii in list_titles:
    #     iiia = iiia + iii + ":" + str(desc[iii]) + "\n"
    #     values_tuple += (str(desc[iii]),)
    # # table.insert('', 0, values=values_tuple)
    # video_url = resp["app"]["videoInfoRes"]["item_list"][0]["video"]["play_addr"]["url_list"][
    #     0].replace("playwm", "play").replace("720p", "1080p")
    # content = get(video_url).content
    # with open(f"{file}/{desc['作品id']}.mp4", "wb") as f:
    #     f.write(content)


    # if "note" in url:
    #     url = url.replace("=", "")
    #     aweme_id = findall('note/(\d+)', url)[0]
    #     url = f"https://www.iesdouyin.com/share/note/{aweme_id}"
    #     resp = get(url, headers=headers).text.encode('gbk', errors='ignore').decode('gbk')
    #     html = etree.HTML(resp)
    #     resp = html.xpath('/html/body/script[@id="RENDER_DATA"]/text()')[0]
    #     resp = unquote(resp).encode('gbk', errors='ignore').decode('gbk')
    #     resp = json.loads(resp)
    #     desc = resp["app"]["videoInfoRes"]["item_list"][0]["statistics"]
    #     desc['收藏'] = desc.pop('collect_count')
    #     desc['评论'] = desc.pop('comment_count')
    #     desc['点赞'] = desc.pop('digg_count')
    #     desc['分享'] = desc.pop('share_count')
    #     desc['格式'] = "note"
    #     desc.pop("play_count")
    #     desc['作品id'] = str(resp["app"]["videoInfoRes"]["item_list"][0]["aweme_id"])
    #     time_1 = int(resp["app"]["videoInfoRes"]["item_list"][0]["create_time"])
    #     time_2 = localtime(time_1)
    #     # 转换成新的时间格式
    #     desc['时间'] = strftime("%Y-%m-%d %H:%M:%S", time_2)
    #     desc['标题'] = resp["app"]["videoInfoRes"]["item_list"][0]['desc']
    #     list_titles = ["作品id", "时间", "标题", "格式", "收藏", "评论", "点赞", "分享"]
    #     values_tuple = ()
    #     iiia = ""
    #     for iii in list_titles:
    #         iiia = iiia + iii + ":" + str(desc[iii]) + "\n"
    #         values_tuple += (str(desc[iii]),)
    #     # table.insert('', 0, values=values_tuple)
    #     s = 0
    #     for i in resp["app"]["videoInfoRes"]["item_list"][0]["images"]:
    #         s += 1
    #         image_url = i["url_list"][-1]
    #         content = get(image_url).content
    #         with open(f"{file}/{desc['作品id']}_{str(s)}.jpeg", "wb") as f:
    #             f.write(content)


if __name__ == '__main__':

    url = "https://www.douyin.com/search/%E5%85%AB%E4%BD%B0%E6%8B%8D%E6%91%84%E8%8A%B1%E7%B5%AE?aid=cf483fff-f3ef-4348-bbae-d709e01ab0c2&modal_id=7320819656267189531&type=general&ug_source=microsoft_mz01"

    aweme_id = re.findall(r'modal_id=(\d+)', url)[0]


    get_aweme(aweme_id)
