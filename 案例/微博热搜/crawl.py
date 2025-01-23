# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests


def fetch():
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    url = "https://weibo.com/ajax/side/hotSearch"

    while True:
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            parse(response.json())
            break
        except requests.HTTPError:
            fetch()
            break


def parse(data: dict):
    try:
        searches = data["data"]["realtime"]
        with open("search.txt", "a", encoding="utf-8") as f:
            for search in searches:
                note = search["note"]
                f.write(note + "\n")
                print(f"hot search: {note}")
    except KeyError as e:
        print(f"Missing expected key in response data: {e}")


def main():
    fetch()


if __name__ == '__main__':
    main()