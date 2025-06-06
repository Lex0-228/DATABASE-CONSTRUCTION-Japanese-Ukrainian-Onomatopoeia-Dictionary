import sqlite3
import json

# Функція для конвертації катакани в хіраґану
def kata_to_hira(text):
    return ''.join(
        chr(ord(char) - 0x60) if 'ァ' <= char <= 'ン' else char
        for char in text
    )

# Завантаження JSON
with open("SFX/onomatopoeia.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Підготовка даних
entries = []
for katakana_word, meanings in data.items():
    for meaning in meanings:
        hiragana_word = kata_to_hira(katakana_word)
        english = meaning.get("english", "")
        details = meaning.get("details", "")
        entries.append((hiragana_word, katakana_word, english, details))

# Додавання до бази даних
conn = sqlite3.connect("SFX/combined_dictionary1.db")
cursor = conn.cursor()

# Створення таблиці
cursor.execute("""
    CREATE TABLE IF NOT EXISTS SFX_japanese_onomatopoeia (
        hiragana TEXT,
        katakana TEXT,
        definition TEXT,
        details TEXT
    )
""")

# Вставка даних
cursor.executemany("""
    INSERT INTO SFX_japanese_onomatopoeia (hiragana, katakana, definition, details)
    VALUES (?, ?, ?, ?)
""", entries)

conn.commit()
conn.close()

print("Дані додано до таблиці SFX_japanese_onomatopoeia.")
