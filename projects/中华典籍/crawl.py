# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import aiohttp
import asyncio
import os


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                html_text = await response.text()
                soup = BeautifulSoup(html_text, 'html.parser')

                title: str = soup.find('h1').get_text().strip()
                text: str = soup.find('div', {'id': 'content', 'class': 'panel-body'}).get_text().strip()
                print(title)

                os.makedirs("ming", exist_ok=True)

                filename = os.path.join("ming", str(title) + '.txt')
                with open(filename, mode="w", encoding="utf-8") as f:
                    f.write(text)
            else:
                print(f"Failed to fetch {url}, status code: {response.status}")

    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")


async def main():
    async with aiohttp.ClientSession() as session:
        page_list = range(4380, 4713)
        split_pages = [list(page_list)[i:i + 20] for i in range(0, len(page_list), 20)]

        for pages in split_pages:
            await asyncio.sleep(10)
            tasks = []
            for page in pages:
                url = f"https://www.zhonghuadiancang.com/lishizhuanji/mingshi/{page}.html"
                task = fetch(session, url)
                tasks.append(task)

            await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
