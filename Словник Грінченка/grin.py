import re

input_file = "Hrinchenko_slovnyk.txt"
output_file = "Hrinchenko_mezh_filtered.txt"
encoding = "utf-8"

with open(input_file, "r", encoding=encoding) as f:
    lines = f.readlines()

articles = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Рядок починається з великої літери і містить 'меж.'
    if re.match(r'^[А-ЯҐЄІЇA-Z]', line) and 'меж.' in line:
        current_article = [line.strip()]
        i += 1
        # Додаємо наступні рядки, поки вони не починаються з великої літери
        while i < len(lines):
            next_line = lines[i]
            if re.match(r'^[А-ЯҐЄІЇA-Z]', next_line) and 'меж.' not in next_line:
                break
            current_article.append(next_line.strip())
            i += 1
        articles.append(" ".join(current_article))
    else:
        i += 1

# берігання у файл
with open(output_file, "w", encoding="utf-8") as f:
    for article in articles:
        f.write(article + "\n\n")

print(f"Знайдено {len(articles)} фрагментів з 'меж.' та збережено у файл: {output_file}")
