# -*- coding: utf-8 -*-

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from tabulate import tabulate
from lxml import etree
import jieba.analyse
import requests
import warnings
import logging
import jieba
import re

logging.getLogger('jieba').setLevel(logging.ERROR)
warnings.filterwarnings("ignore")


class News:
    def __init__(self, url):
        self.url: str = url
        self.stopwords_list: list[str] = self.read_file("stopwords.txt")

    @staticmethod
    def read_file(file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            return file.read().splitlines()

    def run(self):
        extracted_content = self.extract_domain(self.url)
        supported_domains = {'news.cctv.com', 'news.sina.com.cn', 'www.thepaper.cn'}

        if extracted_content in supported_domains:
            title, paragraphs = self.fetch()
            full_text = ' '.join(paragraphs)
            self.extract_keywords(full_text)
        else:
            print('Domain not supported or still updating.')

    @staticmethod
    def extract_domain(url):
        pattern = r'//(.*?)/'
        match = re.search(pattern, url)
        return match.group(1) if match else None

    def fetch(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            response.encoding = "utf-8"
            html_content = response.text
            title, paragraphs = self.parse_html(html_content)

            print(title)
            return title, paragraphs
        except requests.RequestException as e:
            print(f"Error fetching the news: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def parse_html(html_content):
        html_tree = etree.HTML(html_content)
        title = html_tree.xpath('//h1/text()')[0] if html_tree.xpath('//h1/text()') else 'No title found'
        paragraphs = html_tree.xpath('//p/text()')
        return title, paragraphs

    def extract_keywords(self, text_str):
        tfidf_keywords = self.tfidf_result(text_str)
        textrank_keywords = self.textrank_result(text_str)
        lda_keywords = self.lda_result(text_str)

        keywords = {
            "TF-IDF": [word for word, _ in tfidf_keywords],
            "TextRank": [word for word, _ in textrank_keywords],
            "LDA": lda_keywords
        }

        table_data = [
            [keywords["TF-IDF"][i], keywords["TextRank"][i], keywords["LDA"][i]]
            for i in range(10)
        ]

        print(tabulate(table_data, headers=["TF-IDF", "TextRank", "LDA"], tablefmt="grid", stralign='center'))

    def tfidf_result(self, text_str):
        tfidf_vectorizer = TfidfVectorizer(tokenizer=lambda x: jieba.lcut(x), stop_words=self.stopwords_list)
        tfidf_matrix = tfidf_vectorizer.fit_transform([text_str])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        tfidf_array = tfidf_matrix.toarray()
        tfidf_dict = {
            feature_names[i]: tfidf_array[0][i]
            for i in range(len(feature_names))
            if feature_names[i].strip()
        }
        sorted_tfidf_list = sorted(tfidf_dict.items(), key=lambda item: item[1], reverse=True)[:10]
        return sorted_tfidf_list

    @staticmethod
    def textrank_result(text_str):
        jieba.analyse.set_stop_words("stopwords.txt")
        top_keywords = jieba.analyse.textrank(text_str, topK=10, withWeight=True)
        return top_keywords

    def lda_result(self, resp_text):
        documents = [resp_text]

        def preprocess_text(doc):
            return " ".join(jieba.cut(doc))

        preprocessed_docs = [preprocess_text(doc) for doc in documents]
        stop_words = self.stopwords_list
        vectorizer = CountVectorizer(stop_words=stop_words)
        word_matrix = vectorizer.fit_transform(preprocessed_docs)
        lda = LatentDirichletAllocation(n_components=1, random_state=42)
        lda.fit(word_matrix)
        feature_names = vectorizer.get_feature_names_out()
        n_top_words = 10
        topic_keywords = lda.components_[0].argsort()[-n_top_words:][::-1]
        keywords = [feature_names[i] for i in topic_keywords]
        return keywords


if __name__ == '__main__':
    news_url = 'https://news.sina.com.cn/w/2024-10-17/doc-incsvfqp3066425.shtml'
    news = News(news_url)
    news.run()
