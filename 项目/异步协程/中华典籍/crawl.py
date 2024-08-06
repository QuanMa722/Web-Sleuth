# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import aiohttp
import asyncio
import time
import os

ua = UserAgent()
headers = {
    'User-Agent': ua.random
}


def printt(msg):
    nowt = time.strftime("%H:%M:%S", time.localtime(int(time.time())))
    msgs = msg.split("\n")
    for word in msgs:
        print("[" + nowt + "] " + str(word))


async def fetch(session, url):
    try:
        async with session.get(url=url, headers=headers) as response:
            if response.status == 200:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')

                title: str = soup.find('h1').get_text().strip()
                text: str = soup.find('div', {'id': 'content', 'class': 'panel-body'}).get_text().strip()
                printt(title)

                os.makedirs("ming", exist_ok=True)
                filename = os.path.join("ming", str(title) + '.txt')
                with open(filename, mode="w", encoding="utf-8") as f:
                    f.write(text)
            else:
                print(f"Failed to fetch {url}, status code: {response.status}")

    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")


async def main():
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        page_list = range(4380, 4713)
        split_pages = [list(page_list)[i:i + 20] for i in range(0, len(page_list), 20)]

        for pages in split_pages:
            await asyncio.sleep(10)
            tasks = []
            for page in pages:
                # Change the url and directory of the file to be captured.
                url = f"https://www.zhonghuadiancang.com/lishizhuanji/mingshi/{page}.html"
                task = fetch(session, url)
                tasks.append(task)

            await asyncio.gather(*tasks)

    end_time = time.time()
    total_time = round((end_time - start_time), 2)
    printt(f"Total running time: {total_time} seconds")

if __name__ == '__main__':
    asyncio.run(main())
