# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
import requests


def get_hot_searches() -> None:
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }
    url = "https://weibo.com/ajax/side/hotSearch"

    while True:
        try:
            response = requests.get(url=url, headers=headers)
            response.raise_for_status()
            process_search_data(response.json())
            break
        except requests.HTTPError as e:
            if response.status_code == 404:
                print("404 Not Found. Retrying...")
                get_hot_searches()
                break
            else:
                print(f"An error occurred while fetching data: {e}")
                break
        except requests.RequestException as e:
            print(f"An error occurred while fetching data: {e}")
            break


def process_search_data(data: dict) -> None:
    try:
        searches = data["data"]["realtime"]
        with open("search.txt", "a", encoding="utf-8") as f:
            for search in searches:
                note = search["note"]
                f.write(note + "\n")
                print(f"Hot search: {note}")
    except KeyError as e:
        print(f"Missing expected key in response data: {e}")


def main():
    get_hot_searches()


if __name__ == '__main__':
    main()
