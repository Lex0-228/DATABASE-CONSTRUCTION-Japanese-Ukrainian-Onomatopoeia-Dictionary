import requests
from bs4 import BeautifulSoup

base_url = "https://sum20ua.com"
start_wordid = 70788
start_page = 2233
total_pages = 28
output_file = "sum20ua_all_word_links.txt"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Створення файлу
with open(output_file, "w", encoding="utf-8") as f:
    pass

for i in range(total_pages):
    wordid = start_wordid + i * 30
    page = start_page + i
    url = f"{base_url}/?wordid={wordid}&page={page}"
    
    print(f"[{i+1}/{total_pages}] Завантаження: {url}")
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        ul = soup.find('ul')
        if ul:
            links_to_write = []
            for li in ul.find_all('li'):
                a = li.find('a', href=True)
                if a and '/?wordid=' in a['href']:
                    full_link = base_url + a['href'].split('#')[0]
                    links_to_write.append(full_link)

            # Запис у файл
            with open(output_file, "a", encoding="utf-8") as f:
                for link in links_to_write:
                    f.write(link + "\n")

    except Exception as e:
        print(f"Помилка на сторінці {url}: {e}")
        continue

print(f"\nУспішно завершено. Дані збережено в {output_file}")
