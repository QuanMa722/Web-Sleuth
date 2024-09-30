# -*- coding: utf-8 -*-

from collections import Counter
import matplotlib.pyplot as plt
import jieba


plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False


def read_file(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        return file.read()


text = read_file('万历十五年.txt')
stopwords_list = read_file("stopwords.txt").splitlines()

corpus = jieba.lcut(text)
corpus = [word for word in corpus if word not in stopwords_list and word.strip()]

word_counts = Counter(corpus)
filtered_word_counts = {word: count for word, count in word_counts.items() if word.strip()}


def print_word_counts(word_counts, top_n=20):
    for word, count in word_counts.most_common(top_n):
        print(f'{word}: {count}')


def plot_word_counts(word_counts, top_n=20):
    most_common_words = word_counts.most_common(top_n)
    words, counts = zip(*most_common_words)
    plt.figure(figsize=(12, 6))
    plt.scatter(words, counts, marker='o', c='k')
    # plt.title(f'Top {top_n} Words Frequency', fontsize=14)
    # plt.xlabel('Words', fontsize=12)
    # plt.ylabel('Frequency', fontsize=12)
    # plt.xticks(rotation=45)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.grid(False)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    try:
        print_word_counts(word_counts)
        plot_word_counts(word_counts)

    except Exception as error:
        print(f"An error occurred: {error}.")
