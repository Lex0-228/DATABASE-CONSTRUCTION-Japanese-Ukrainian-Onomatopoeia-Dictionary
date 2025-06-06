import sqlite3

text_path = "reordered_cleaned_text.txt"
db_path = "combined_dictionary.db"

# Зчитування рядків з текстового файлу
with open(text_path, "r", encoding="utf-8") as file:
    lines = [line.strip() for line in file if line.strip()]

# Підключення до бази даних
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Створення таблиці
cursor.execute("""
CREATE TABLE IF NOT EXISTS jp_onomatopoeia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    definition TEXT,
    examples TEXT,
    examples_translation TEXT,
    similar TEXT,
    category TEXT
);
""")

# Обробка  рядків: word, definition, examples, examples_translation, similar
i = 0
while i + 3 < len(lines):
    word = lines[i]
    definition = lines[i + 1]
    examples = lines[i + 2]
    examples_translation = lines[i + 3]
    similar = None

    # Якщо п'ятий рядок існує і починається на "Близьк", додаємо його
    if i + 4 < len(lines) and lines[i + 4].startswith("Близьк"):
        similar = lines[i + 4]
        i += 5
    else:
        i += 4

    # Вставка до таблиці
    cursor.execute("""
        INSERT INTO jp_onomatopoeia (word, definition, examples, examples_translation, similar)
        VALUES (?, ?, ?, ?, ?)
    """, (word, definition, examples, examples_translation, similar))

# Завершення роботи
conn.commit()
conn.close()

print("Дані додано до таблиці jp_onomatopoeia.")
