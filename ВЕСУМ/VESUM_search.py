import sqlite3
import re

txt_path = "VESUM_intj.txt"
db_path = "combined_dictionary.db"

# Завантаження слів з текстового файлу
def normalize_input_word(word):
    word = word.lower().strip()
    if '-' in word:
        parts = word.split('-')
        if len(parts) == 2 and parts[0] == parts[1]:
            return parts[0]
    return word

with open(txt_path, "r", encoding="utf-8") as f:
    raw_words = [line.strip() for line in f if line.strip()]
    target_words = set(normalize_input_word(w) for w in raw_words)

# Підключення до бази даних
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Завантажуємо значення з колонки word
cursor.execute("SELECT word FROM dictionary")
db_words_raw = cursor.fetchall()

# Функція для токенізації слова з бази
def tokenize(word_field):
    word_field = word_field.lower()
    cleaned = re.sub(r"[()/,;]| +", " ", word_field)
    tokens = [w.strip() for w in cleaned.split() if w.strip()]
    return set(tokens)

# Множини всіх токенів з бази
db_token_set = set()
for row in db_words_raw:
    db_token_set.update(tokenize(row[0]))

# Пошук
found = sorted([w for w in target_words if w in db_token_set])
not_found = sorted([w for w in target_words if w not in db_token_set])

# Вивід
print(f"Знайдено ({len(found)}):")
for w in found:
    print("  -", w)

print(f"\nНе знайдено ({len(not_found)}):")
for w in not_found:
    print("  -", w)

# Збереження незнайдених слів
with open("not_found_VESUM_intj.txt", "w", encoding="utf-8") as f:
    for w in not_found:
        f.write(w + "\n")
