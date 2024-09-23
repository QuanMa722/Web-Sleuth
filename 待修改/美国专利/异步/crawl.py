# -*- coding: utf-8 -*-

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import asyncio
import httpx
import csv
import os


async def fetch(client, patent_num):
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random
    }

    url = 'https://patents.google.com/patent/' + patent_num

    try:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            patent_title = soup.find(itemprop="title").text.strip()
            pub_num = soup.find(itemprop="publicationNumber").text.strip()
            abstract = soup.find(class_="abstract").text.strip()
            img_list = [img['src'] for img in soup.find_all(itemprop="thumbnail")]
            inventor = [i.get_text(strip=True) for i in soup.find_all(itemprop="inventor")]
            current_assignee = [i.get_text(strip=True) for i in soup.find_all(itemprop="assigneeCurrent")]

            events_dict = {}
            titles = soup.find_all(itemprop="title")
            dates = soup.find_all(itemprop="date")
            for i in range(min(len(titles), len(dates))):
                event = titles[i].text.strip()
                time = dates[i].text.strip()
                if event:
                    if event == 'Anticipated expiration' or event == 'Adjusted expiration':
                        events_dict[time] = event
                        break
                    events_dict[time] = event

            classifications_code = [i.get_text(strip=True) for i in soup.find_all(itemprop="Code")]
            classifications = [i.get_text(strip=True) for i in soup.find_all(itemprop="classifications")]

            infor_list = []
            for num in range(1, 10):
                infor = soup.find(num=f"000{num}")
                if infor:
                    infor_list.append(infor.text.strip())
            for num in range(10, 100):
                infor = soup.find(num=f"00{num}")
                if infor:
                    infor_list.append(infor.text.strip())
                else:
                    break
            for num in range(100, 200):
                infor = soup.find(num=f"0{num}")
                if infor:
                    infor_list.append(infor.text.strip())

            # 写入CSV文件
            file_exists = os.path.isfile('patent_data.csv')
            with open('patent_data.csv', mode='a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(
                        ['Patent Title', 'Publication Number', 'Abstract', 'Images', 'Inventors',
                         'Current Assignees',
                         'Events', 'Classifications Code', 'Classifications', 'Information']
                    )
                writer.writerow([
                    patent_title,
                    pub_num,
                    abstract,
                    ', '.join(img_list),
                    ', '.join(inventor),
                    ', '.join(current_assignee),
                    ', '.join(f"{time}: {event}" for time, event in events_dict.items()),
                    ', '.join(classifications_code),
                    ', '.join(classifications),
                    ', '.join(infor_list),
                ])

        else:
            print(f"Failed to fetch {url}. Status code: {response.status_code}")

    except Exception as e:
        print(e)
        print(f"Error fetching {url}")


async def main():
    async with httpx.AsyncClient() as client:

        with open(file='output_10000.txt', mode='r', encoding='utf-8') as f:
            patent = f.read()

        patent_list = patent.split(',')

        # 将列表切分为每 20 个元素一组
        chunk_size = 20
        chunks = [patent_list[i:i + chunk_size] for i in range(0, len(patent_list), chunk_size)]

        for i, chunk in enumerate(chunks):
            print(f"Chunk {i + 1}")
            tasks = [fetch(client, patent_num) for patent_num in chunk]
            await asyncio.gather(*tasks)
            await asyncio.sleep(60)

if __name__ == '__main__':
    asyncio.run(main())
