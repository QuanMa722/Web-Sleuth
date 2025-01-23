# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tabulate import tabulate
from bertopic import BERTopic
from datetime import datetime
from hdbscan import HDBSCAN
from lxml import etree
from umap import UMAP
import requests
import warnings
import logging
import jieba
import time
import json
import sys
import re
import os

# Suppress warnings and set logging level for jieba
warnings.filterwarnings("ignore")
jieba.setLogLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # logging.FileHandler('scraper.log', 'a', 'utf-8'),
        logging.StreamHandler()
    ]
)

cookies = {
    'bid': '1gMxgR_xU5U',
    'll': '"118282"',
    'Hm_lvt_19fc7b106453f97b6a84d64302f21a04': '1733372099',
    '_ga_PRH9EWN86K': 'GS1.2.1733372100.1.0.1733372100.0.0.0',
    '_pk_id.100001.4cf6': '024b110d1382e475.1733372159.',
    '__yadk_uid': 'qBGjSnLZknbXZA3ugKLSpQd9RbCSfoz1',
    '_vwo_uuid_v2': 'D8DB7696A3F6AD5AF442F89BBAA685C83|ba3269f7a883157ff71737fd00d2c8c0',
    'push_noty_num': '0',
    'push_doumail_num': '0',
    'dbcl2': '"224267170:dxEUEjAsXKc"',
    '_ga': 'GA1.1.857826835.1733372040',
    '_ga_Y4GN1R87RG': 'GS1.1.1735141304.2.1.1735141359.0.0.0',
    'ck': 'X8kM',
    '_pk_ref.100001.4cf6': '%5B%22%22%2C%22%22%2C1735269501%2C%22https%3A%2F%2Fm.douban.com%2F%22%5D',
    '_pk_ses.100001.4cf6': '1',
    'ap_v': '0,6.0',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}


def get_movie(movie_search):
    try:
        url = f'https://search.douban.com/movie/subject_search?search_text={movie_search}'
        response = requests.get(url, headers=headers, cookies=cookies)
        response_text = response.text

        pattern = r'"id":\s*(\d+).*?"title":\s*"([^"]+)"'
        matches = re.findall(pattern, response_text)

        result = {int(match[0]): match[1].encode().decode('unicode_escape') for match in matches}
        return result

    except requests.RequestException as e:
        logging.error(f"Error fetching: {e}")


def fetch(movie_id):
    try:
        all_comments = []

        for page in range(0, 381, 20):  # This can be adjusted if you want to limit the number of pages

            url = f'https://movie.douban.com/subject/{movie_id}/comments?start={page}&limit=20&&sort=new_score&status=P'
            response = requests.get(url, headers=headers, cookies=cookies)
            response_text = response.text

            time.sleep(1)

            logging.info(f'Fetched page {page + 20}')
            all_comments.extend(parse(response_text))
        pipline(all_comments)

    except requests.RequestException as e:
        logging.error(f"Error fetching: {e}")


def parse(response_text):
    # parse data
    tree = etree.HTML(response_text)
    comment_list = tree.xpath('//div[@class="comment-item "]')
    comments_list = []

    for comment_div in comment_list:
        name = comment_div.xpath('.//span[@class="comment-info"]/a/text()')
        name = name[0].strip() if name else ''

        comment = comment_div.xpath('.//p[@class=" comment-content"]/span/text()')
        comment = comment[0].strip() if comment else ''

        upvote = comment_div.xpath('.//span[@class="votes vote-count"]/text()')
        upvote = upvote[0].strip() if upvote else '0'

        comment_time = comment_div.xpath('.//span[@class="comment-time "]/@title')
        comment_time = comment_time[0] if comment_time else ''

        star_attribute = comment_div.xpath('.//span[contains(@class,"rating")]/@class')
        stars = 0
        if star_attribute:
            stars = int(re.search(r'\d+', star_attribute[0]).group())

        comment_data = {
            'name': name,
            'comment': comment,
            'upvote': upvote,
            'time': comment_time,
            'stars': stars
        }
        comments_list.append(comment_data)

    return comments_list


def pipline(comments_list):
    # store data
    try:

        with open('comments.json', 'a', encoding='utf-8') as file:
            json.dump(comments_list, file, ensure_ascii=False, indent=4)
            logging.info(f'Successfully saved {len(comments_list)} comments.')

    except Exception as e:
        logging.error(f'Error saving data: {e}')


def comments_statistic(comments):
    star_counter = Counter(comment['stars'] for comment in comments)

    total_star_sum = 0
    total_comments = 0
    levels = []
    counts = []

    for stars, count in star_counter.items():
        if stars > 0:
            level = stars // 10
            levels.append(level)
            counts.append(count)
            total_star_sum += level * count
            total_comments += count

    average_star_level = total_star_sum / total_comments if total_comments > 0 else 0

    # 按年份统计评论数量
    year_counter = defaultdict(int)
    for comment in comments:
        time_str = comment['time']  # 假设时间字段为 'time'
        year = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').year  # 提取年份
        year_counter[year] += 1

    # 准备数据
    years = sorted(year_counter.keys())
    year_counts = [year_counter[year] for year in years]

    # 创建画布，设置为1行2列的子图
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    # 图1: 星级分布
    axs[0].bar(levels, counts, color='skyblue', edgecolor='black')
    axs[0].set_title('Star Level Distribution', fontweight='bold')
    axs[0].set_xlabel('Star Level', fontweight='bold')
    axs[0].set_ylabel('Number of Comments', fontweight='bold')
    axs[0].grid(True)
    axs[0].axvline(x=average_star_level, color='red', linestyle='--', label=f'Average Level: {average_star_level:.2f}')
    axs[0].legend()

    # 图2: 按年份统计评论数量
    axs[1].plot(years, year_counts, marker='o', linestyle='--', color='k', label='Comments Per Year')
    max_count = max(year_counts)
    max_year = years[year_counts.index(max_count)]
    axs[1].axvline(x=max_year, color='r', linestyle='--', label=f'Max Comments in {max_year}')
    axs[1].set_title('Comment Distribution by Year', fontweight='bold')
    axs[1].set_xlabel('Year', fontweight='bold')
    axs[1].set_ylabel('Number of Comments', fontweight='bold')
    axs[1].set_xticks(years)
    axs[1].set_xticklabels(years, rotation=45)
    axs[1].grid(True)
    axs[1].legend()

    # 显示图表
    plt.tight_layout()  # 自动调整子图布局
    plt.savefig('distribution.png', dpi=300, bbox_inches='tight')
    plt.show()


def comments_wordcloud(comments):
    # 假设 comments 是一个字典列表
    comments_list = [comment['comment'] for comment in comments]

    # 将评论列表中的每条评论进行中文分词
    segmented_text = " ".join([" ".join(jieba.cut(comment)) for comment in comments_list])

    # 加载停用词列表
    with open('stopwords.txt', 'r', encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())

    # 创建词云对象，设置停用词
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        font_path='simhei.ttf',
        stopwords=stopwords  # 设置停用词
    ).generate(segmented_text)

    # 绘制词云图
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')  # 关闭坐标轴
    plt.savefig('wordcloud.png', dpi=300, bbox_inches='tight')
    plt.show()


def comments_topic(comments):
    try:
        # Prepare data and stopwords
        comments_list = [comment['comment'] for comment in comments]

        # Load stopwords
        with open(file="stopwords.txt", mode="r", encoding="utf-8") as stop_file:
            stopwords_list = stop_file.read().splitlines()

        # Initialize embedding model
        embedding_model = SentenceTransformer(
            "thenlper/gte-base-zh"
        )

        # Preprocess and embed the comments
        corpus_list = []
        for sentence in comments_list:
            corpus = jieba.lcut(sentence)
            corpus = [word for word in corpus if word not in stopwords_list and word != '']
            corpus_list.append(" ".join(corpus))

        embeddings = embedding_model.encode(corpus_list, show_progress_bar=True)

        # Initialize UMAP and HDBSCAN models
        umap_model = UMAP(
            n_neighbors=15,
            n_components=5,
            min_dist=0.0,
            metric='cosine',
            random_state=30
        )

        hdbscan_model = HDBSCAN(
            min_cluster_size=15,
            min_samples=10,
            metric='euclidean'
        )

        vectorizer_model = CountVectorizer()

        # Initialize BERTopic model
        topic_model = BERTopic(
            embedding_model=embedding_model,
            vectorizer_model=vectorizer_model,
            umap_model=umap_model,
            hdbscan_model=hdbscan_model,
        )

        # Fit the BERTopic model
        topics, _ = topic_model.fit_transform(corpus_list, embeddings=embeddings)
        fig_barchart = topic_model.visualize_barchart()
        fig_barchart.show()

        reduced_embeddings = UMAP(n_neighbors=10, n_components=2, min_dist=0.0, metric='cosine').fit_transform(
            embeddings)
        fig_documents = topic_model.visualize_documents(corpus_list, reduced_embeddings=reduced_embeddings,
                                                        hide_document_hover=True)
        fig_documents.show()



    except Exception as e:
        print(f"Error: {e}")
        return []


def comments_analyse():
    with open('comments.json', 'r', encoding='utf-8') as file:
        comments = json.load(file)

    comments_statistic(comments)
    comments_wordcloud(comments)
    comments_topic(comments)


def main():
    if os.path.exists('comments.json'):
        logging.error('File already exists.')
        comments_analyse()
        sys.exit(1)

    # search by input word
    movie_search = input("Movie: ")

    if movie_search:
        movie_search_dict = get_movie(movie_search)
        # format the output
        table_data = [[index + 1, movie_id, movie_search_dict[movie_id]] for index, movie_id in
                      enumerate(movie_search_dict)]
        table_headers = ["Index", "Movie ID", "Movie Name"]
        print(tabulate(table_data, headers=table_headers, tablefmt="pretty"))

    movie_search_dict = get_movie(movie_search)

    # fetch comments by Movie ID
    movie_id = int(input("Movie ID: "))
    fetch(movie_id)

    if movie_search:
        movie_name = movie_search_dict[movie_id]
        print(movie_name)

    comments_analyse()


if __name__ == '__main__':
    main()
