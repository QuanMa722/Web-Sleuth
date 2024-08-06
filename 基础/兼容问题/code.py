# -*- coding: utf-8 -*-

import requests

url = "https://www.baidu.com"

response = requests.get(url=url)

# the 基础
# It will be garbled.
print(response.text)

# the solution1
print(response.content.decode())

# the solution2
response.encoding = "utf-8"
print(response.text)

# the solution3
response.encoding = response.apparent_encoding
print(response.text)
