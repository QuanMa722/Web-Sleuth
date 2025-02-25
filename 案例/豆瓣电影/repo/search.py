# -*- coding: utf-8 -*-

from hconfig import HeadCook
from tabulate import tabulate
import requests
import re

class MovieSearch:

    def __init__(self):
        self.headers = HeadCook.headers
        self.cookies = HeadCook.cookies

    def movie_search(self, movie_str):
        url = f'https://search.douban.com/movie/subject_search?search_text={movie_str}'
        response = requests.get(url, headers=self.headers, cookies=self.cookies)
        response_text = response.text

        pattern = r'"id":\s*(\d+).*?"title":\s*"([^"]+)"'
        matches = re.findall(pattern, response_text)

        result = {int(match[0]): match[1].encode().decode('unicode_escape') for match in matches}

        table_data = [[index + 1, movie_id, result[movie_id]] for index, movie_id in
                      enumerate(result)]
        table_headers = ["Index", "Movie ID", "Movie Name"]
        print(tabulate(table_data, headers=table_headers, tablefmt="pretty"))
