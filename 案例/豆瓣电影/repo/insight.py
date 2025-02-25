# -*- coding: utf-8 -*-

from collections import Counter, defaultdict
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from datetime import datetime
import jieba
import json


class Insight:

    def __init__(self, movie_id):
        self.movie_id = movie_id

        with open(f'{movie_id}/comments.json', 'r', encoding='utf-8') as file:
            self.comments = json.load(file)

    def comments_statistic(self):
        star_counter = Counter(comment['stars'] for comment in self.comments)

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
        year_counter = defaultdict(int)
        for comment in self.comments:
            time_str = comment['time']
            year = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S').year
            year_counter[year] += 1

        years = sorted(year_counter.keys())
        year_counts = [year_counter[year] for year in years]

        fig, axs = plt.subplots(1, 2, figsize=(14, 6))

        axs[0].bar(levels, counts, color='skyblue', edgecolor='black')
        axs[0].set_title('Star Level Distribution', fontweight='bold')
        axs[0].set_xlabel('Star Level', fontweight='bold')
        axs[0].set_ylabel('Number of Comments', fontweight='bold')
        axs[0].grid(True)
        axs[0].axvline(x=average_star_level, color='red', linestyle='--',
                       label=f'Average Level: {average_star_level:.2f}')
        axs[0].legend()

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

        plt.tight_layout()
        plt.savefig(f'{self.movie_id}/distribution.png', dpi=300, bbox_inches='tight')
        # plt.show()

    def comments_wordcloud(self):

        comments_list = [comment['comment'] for comment in self.comments]

        segmented_text = " ".join([" ".join(jieba.cut(comment)) for comment in comments_list])

        with open('stopwords.txt', 'r', encoding='utf-8') as file:
            stopwords = set(file.read().splitlines())

        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            font_path='simhei.ttf',
            stopwords=stopwords
        ).generate(segmented_text)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(f'{self.movie_id}/wordcloud.png', dpi=300, bbox_inches='tight')
        # plt.show()
