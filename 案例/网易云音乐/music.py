# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests
import re
import os

# 飙升榜 19723756
# 新歌榜 3779629
# 原创榜 2884035
# 热歌榜 3778678

# 输入榜单ID
type_id = '19723756'

# 输入要下载的歌曲数量
num_songs = 5

# os.makedirs(type_id)

url = f"https://music.163.com/discover/toplist?id={type_id}"

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}

response = requests.get(url=url, headers=headers)

# 使用正则表达式提取歌曲信息
html_data = re.findall(r'<li><a href="/song\?id=(\d+)">(.*?)</a>', response.text)[:num_songs]

print(html_data)

for song_id, title in html_data:
    # 构建音乐播放地址
    music_url = f"http://music.163.com/song/media/outer/url?id={song_id}.mp3"

    print()

    # 请求音乐播放地址并下载音乐
    music_content = requests.get(url=music_url, headers=headers).content

    # 清理文件名中的特殊字符
    cleaned_title = re.sub(r'[\\/*?:"<>|]', '', title)

    with open(f"{cleaned_title}.mp3", 'wb') as file:
        file.write(music_content)

