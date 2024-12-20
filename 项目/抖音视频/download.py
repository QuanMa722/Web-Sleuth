# -*- coding: utf-8 -*-

import requests
import json

# 打开并读取 JSON 文件
with open('video-id.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

video_url = data['video_url']

# 发送GET请求
response = requests.get(video_url, stream=True)

# 获取并保存视频
with open('downloaded_video.mp4', 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):  # 分块写入
        f.write(chunk)




