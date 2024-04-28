
# -*- coding: utf-8 -*-

import requests


def download_image(url):

    print("start", url)

    response = requests.get(url)

    print("complete")

    file_name = url.rsplit("-")[-1]

    with open(file_name, mode="wb") as file_object:
        file_object.write(response.content)  #


if __name__ == '__main__':
    url_list = [

           "https://images.hdqwalls.com/wallpapers/python-logo-4k-i6.jpg",
           "https://images.hdqwalls.com/wallpapers/python-logo-4k-i6.jpg",
           "https://images.hdqwalls.com/wallpapers/python-logo-4k-i6.jpg",

        ]
    for url in url_list:
        download_image(url)