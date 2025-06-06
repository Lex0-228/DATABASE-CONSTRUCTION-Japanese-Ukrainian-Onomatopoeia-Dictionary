import sqlite3
from bs4 import BeautifulSoup

# Файли
input_file = "entries_with_vyg_async.txt"
db_file = "vyg_dictionary.db"

# Зчитування HTML
with open(input_file, "r", encoding="utf-8") as f:
    html = f.read()

# Парсинг файлу
soup = BeautifulSoup(html, "html.parser")
entries = soup.find_all("div", class_="ENTRY")

# Збір даних у список
records = []

for entry in entries:
    word_block = entry.find("div", class_="WORD")
    word = word_block.get_text(" ", strip=True) if word_block else ""

    formulas = entry.find_all("div", class_="FORMULA")
    definitions = [" ".join(f.stripped_strings) for f in formulas]
    definition = " | ".join(definitions)

    examples = []
    for ill in entry.find_all("div", class_="ILL"):
        illtxt = ill.find("div", class_="ILLTXT")
        illsrc = ill.find("div", class_="ILLSRC")
        parts = []
        if illtxt:
            parts.append(illtxt.get_text(" ", strip=True))
        if illsrc:
            parts.append(illsrc.get_text(" ", strip=True))
        if parts:
            examples.append(" ".join(parts))
    example_text = " || ".join(examples)

    records.append((word, definition, example_text))

# Сортування за словом
records.sort(key=lambda x: x[0].lower())

# Створення БД
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS dictionary")
cursor.execute("""
CREATE TABLE dictionary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    definition TEXT,
    examples TEXT
)
""")

# Вставка відсортованих записів
for word, definition, examples in records:
    cursor.execute("""
        INSERT INTO dictionary (word, definition, examples)
        VALUES (?, ?, ?)
    """, (word, definition, examples))

conn.commit()
conn.close()

print(f"Збережено {len(records)} записів у базу {db_file}, відсортованих за словом.")
