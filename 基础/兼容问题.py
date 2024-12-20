# -*- coding: utf-8 -*-

import requests

url = "https://www.baidu.com"

response = requests.get(url=url)

# 乱码
print(response.text)

# 方法 1
print(response.content.decode())

# 方法 2
response.encoding = "utf-8"
print(response.text)

# 方法 3
response.encoding = response.apparent_encoding
print(response.text)
