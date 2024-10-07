# -*- coding: utf-8 -*-

import ast

with open('news.txt', 'r', encoding='utf-8') as f:
    news_list = f.readlines()

# kind_list = ['world', 'china', 'business', 'lens', 'technology', 'science', 'health', 'education', 'culture', 'style', 'travel', 'real-estate', 'opinion'
china_news = []
for news in news_list:
    try:
        news = news.strip()
        news_dict = ast.literal_eval(news)
        if news_dict['kind'] == 'china':
            china_news.append(news_dict)

    except Exception as e:
        print(news)
        print(f"Error parsing news: {e}")
        continue

china_news_sorted = sorted(china_news, key=lambda x: x['date'], reverse=True)

for news in china_news_sorted:
    print(news)
