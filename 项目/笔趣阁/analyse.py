# -*- coding: utf-8 -*-

from sklearn.metrics.pairwise import cosine_similarity
from transformers import BertTokenizer, BertModel
from sklearn.decomposition import PCA
from itertools import combinations
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import jieba
import torch

plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False


# 读取文本和停用词
def read_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        return file.read()


text = read_file('fiction_process.txt')
stopwords_list = read_file("stopwords.txt").splitlines()

# 处理文本
corpus = jieba.lcut(text)
corpus = [word for word in corpus if word not in stopwords_list and word.strip()]

word_counts = Counter(corpus)
filtered_word_counts = {word: count for word, count in word_counts.items() if word.strip()}


# 输出词频
def print_word_counts(word_counts, top_n=20):
    for word, count in word_counts.most_common(top_n):
        print(f'{word}: {count}')


print_word_counts(word_counts)

# 定义数据
words = [
    "皇帝", "张居正", "万历", "文官", "申时行", "李贽", "官员", "海瑞",
    "历史", "戚继光", "本朝", "中国", "社会", "道德", "首辅", "事情",
    "大学士", "宦官", "发生", "国家"
]
frequencies = [
    635, 297, 262, 204, 193, 177, 146, 128,
    122, 117, 108, 98, 94, 92, 87, 80,
    80, 79, 75, 74
]


# 绘制词频散点图
def plot_word_frequency(words, frequencies):
    plt.figure(figsize=(10, 6))
    plt.scatter(words, frequencies, color='k')
    plt.xlabel('词语', fontsize=12)
    plt.ylabel('频率', fontsize=12)
    plt.title('词频散点图', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.show()


plot_word_frequency(words, frequencies)

# 加载BERT模型和tokenizer
model_name = "thenlper/gte-base-zh"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)


def get_embedding(text):
    tokens = tokenizer(text, return_tensors='pt')
    with torch.no_grad():
        outputs = model(**tokens)
    embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    return embedding


def compute_similarity(word_list):
    embeddings = {word: get_embedding(word) for word in word_list}
    similarities = {}
    for word1, word2 in combinations(word_list, 2):
        emb1 = embeddings.get(word1)
        emb2 = embeddings.get(word2)
        if emb1 is not None and emb2 is not None:
            sim = cosine_similarity([emb1], [emb2])[0][0]
            similarities[(word1, word2)] = sim
    return similarities


# 计算相似度
sample_words = words[:21]  # 只取前21个词
similarity_results = compute_similarity(sample_words)


# 创建相似度矩阵
def create_similarity_matrix(similarity_results, words):
    similarity_matrix = pd.DataFrame(index=words, columns=words)
    for (word1, word2), sim in similarity_results.items():
        similarity_matrix.loc[word1, word2] = sim
        similarity_matrix.loc[word2, word1] = sim
    similarity_matrix = similarity_matrix.astype(float)
    return similarity_matrix


similarity_matrix = create_similarity_matrix(similarity_results, sample_words)


# 绘制热力图
def plot_heatmap(matrix):
    plt.figure(figsize=(12, 10))
    sns.heatmap(matrix, annot=True, cmap='Blues', fmt='.2f', vmin=0, vmax=1)
    plt.title('词汇相似度热力图', fontsize=14)
    plt.yticks(rotation=0)
    plt.show()


plot_heatmap(similarity_matrix)


# 计算嵌入向量并降维
def plot_pca_embeddings(corpus, num_words=100):
    embeddings = {word: get_embedding(word) for word in corpus[:num_words]}
    pca = PCA(n_components=2)
    reduced_embeddings = pca.fit_transform(list(embeddings.values()))

    plt.figure(figsize=(12, 10))
    plt.scatter(reduced_embeddings[:, 0], reduced_embeddings[:, 1])

    for i, word in enumerate(corpus[:88]):
        plt.text(reduced_embeddings[i, 0], reduced_embeddings[i, 1], word, fontsize=10)

    plt.title('词汇离散图', fontsize=14)
    plt.xlabel('PCA1', fontsize=12)
    plt.ylabel('PCA2', fontsize=12)
    plt.grid(False)
    plt.show()


plot_pca_embeddings(corpus)
