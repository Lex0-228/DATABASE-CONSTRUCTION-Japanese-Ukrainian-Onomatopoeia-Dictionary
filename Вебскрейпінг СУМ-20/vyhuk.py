import aiohttp
import asyncio
from bs4 import BeautifulSoup

output_file = "entries_with_vyg_async1.txt"
semaphore = asyncio.Semaphore(40)

headers = {
    "User-Agent": "Mozilla/5.0"
}

# запис в файл (асинхронно)
async def write_entry(entry_html):
    async with aiofiles.open(output_file, "a", encoding="utf-8") as f:
        await f.write(entry_html)
        await f.write("\n\n---\n\n")

# функція для однієї сторінки
async def fetch_and_parse(session, url):
    async with semaphore:
        try:
            async with session.get(url, headers=headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, "html.parser")

                entry = soup.find("div", class_="ENTRY")
                if entry and entry.find("i", string="виг."):
                    outer_div = entry.find_parent("div")
                    if outer_div:
                        await write_entry(str(outer_div))
                        print(f"Знайдено виг. у {url}")
                else:
                    print(f"… {url} без виг.")
        except Exception as e:
            print(f"Помилка на {url}: {e}")

# асинхронний обхід усіх URL
async def main():
    # зчитування URL
    with open("sum20ua_links_cleaned.txt", "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    # очищення результату
    with open(output_file, "w", encoding="utf-8") as f:
        pass

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_and_parse(session, url) for url in urls]
        await asyncio.gather(*tasks)

# запуск
import aiofiles
asyncio.run(main())


