# -*- coding: utf-8 -*-

from search import MovieSearch
from insight import Insight
from crawl import Crawl
import re


class Douban:

    def __init__(self, movie_str):
        self.movie_str = movie_str
        self.movie_id = None

    def run(self):

        pattern = r'^-?\d+(\.\d+)?$'
        comment_crawl = Crawl()

        if bool(re.match(pattern, self.movie_str)):
            comment_crawl.fetch(self.movie_str)
            self.movie_id = self.movie_str

        else:

            movie_search = MovieSearch()
            movie_search.movie_search(self.movie_str)

            movie_id = input('Movie ID: ')
            comment_crawl.fetch(movie_id)
            self.movie_id = movie_id

        # comments_analyse = Insight(self.movie_id)
        # comments_analyse.comments_statistic()
        # comments_analyse.comments_wordcloud()


if __name__ == '__main__':
    movie_input = input('Movie: ')
    douban = Douban(movie_input)
    douban.run()
