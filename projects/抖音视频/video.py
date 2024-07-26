# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests
import json
import re

with open(file='config.json', mode='r') as f:
    configs = json.load(f)

url = configs['url']
video_url = configs['video_url']
cookie = configs['cookie']

user_id = re.findall(r'/user/([A-Za-z0-9_-]+)', url)[0]
ua = UserAgent()
headers = {
    'referer': f'https://www.douyin.com/user/{user_id}',
    'cookie': cookie,
    'User-Agent': ua.random,
}

video = requests.get(video_url, headers=headers)
with open("video.mp4", 'wb') as f:
    f.write(video.content)

print("已完成该视频的下载。")
