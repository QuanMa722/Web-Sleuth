# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

url = "https://www.baidu.com"

response = requests.get(url=url)

# 乱码
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
link = soup.find('a', {'name': 'tj_briicon'})
print("eg:", link.get_text())

# 方法 1
html_content = response.content.decode()
soup = BeautifulSoup(html_content, 'html.parser')
link = soup.find('a', {'name': 'tj_briicon'})
print("eg:", link.get_text())

# 方法 2
response.encoding = "utf-8"
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
link = soup.find('a', {'name': 'tj_briicon'})
print("eg:", link.get_text())

# 方法 3
response.encoding = response.apparent_encoding
html_content = response.text
soup = BeautifulSoup(html_content, 'html.parser')
link = soup.find('a', {'name': 'tj_briicon'})
print("eg:", link.get_text())

