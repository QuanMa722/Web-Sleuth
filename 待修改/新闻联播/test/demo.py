# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import json

# Initialize a fake user agent for headers
ua = UserAgent()
headers = {
    'User-Agent': ua.random  # Use a random user agent to prevent blocking
}

# Define the target URL
url = 'http://mrxwlb.com/2015/12/28/2015%e5%b9%b412%e6%9c%8828%e6%97%a5%e6%96%b0%e9%97%bb%e8%81%94%e6%92%ad%e6%96%87%e5%ad%97%e7%89%88/'

# Send GET request to the URL
response = requests.get(url, headers=headers)
response.raise_for_status()  # Raise an error if the request fails

# Parse the HTML content of the page using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all paragraph elements on the page
paragraphs = soup.find_all('p')

# List to store news items
news_items = []
current_title = None  # To store the title of the current news item
current_content = []  # To store the content of the current news item

# Iterate over all paragraph elements to extract titles and content
for para in paragraphs:
    strong_tag = para.find('strong')  # Check if there is a title (strong tag)

    if strong_tag and strong_tag.text.strip():  # If strong_tag has content
        if current_title:  # If there's already a title and content, append the previous item
            news_items.append({
                'title': current_title,
                'content': "\n".join(current_content)  # Join the paragraphs for the content
            })

        current_title = strong_tag.get_text(strip=True)  # Extract the title text
        current_content = []  # Reset content for the new item
    else:
        current_content.append(para.get_text(strip=True))  # Append content to the current item

# Append the last news item after finishing the loop
if current_title:
    news_items.append({
        'title': current_title,
        'content': "\n".join(current_content)
    })

# Filter out news items with unwanted titles (e.g., '国内联播快讯', '国际联播快讯')
filtered_news_items = [
    news for news in news_items[1:]
    if news['title'] not in ['国内联播快讯', '国际联播快讯', '联播快讯']
]

# Print the filtered news items to the console
for news in filtered_news_items:
    print(f"Title: {news['title']}")
    print(f"Content: {news['content']}")
    print()

# Save the filtered news items to a JSON file
with open('20181214.json', 'w', encoding='utf-8') as f:
    json.dump(filtered_news_items, f, ensure_ascii=False, indent=4)  # Write in JSON format
