import aiohttp
import asyncio


async def download_file(session, url):
    async with session.get(url) as response:
        if response.status == 200:
            file_name = url.rsplit("/")[-1]
            with open(file_name, mode="wb") as file:
                file.write(await response.read())


async def main():
    url_list = [
        "https://images.hdqwalls.com/wallpapers/python-logo-4k-i6.jpg"

    ]

    async with aiohttp.ClientSession() as session:
        tasks = [download_file(session, url) for url in url_list]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
