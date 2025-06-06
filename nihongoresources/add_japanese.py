import sqlite3

txt_path = "giongo.txt"
db_path = "combined_dictionary.db"

# Зчитування рядків з файлу
with open(txt_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

entries = []
skipped = []

for i, line in enumerate(lines[1:], start=2):
    parts = line.strip().split("\t")
    if len(parts) >= 3:
        hiragana = parts[0].strip()
        katakana = parts[1].strip()
        definition = parts[2].strip()
        # Все після третього елемента — це category
        category = " ".join(parts[3:]).strip()
        entries.append((hiragana, katakana, definition, category))
    else:
        skipped.append((i, line.strip()))

# Запис в базу
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Створення таблиці
cursor.execute("""
CREATE TABLE IF NOT EXISTS japanese_onomatopoeia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hiragana TEXT,
    katakana TEXT,
    definition TEXT,
    category TEXT
)
""")

cursor.executemany("""
INSERT INTO japanese_onomatopoeia (hiragana, katakana, definition, category)
VALUES (?, ?, ?, ?)
""", entries)

conn.commit()
conn.close()

print(f"Імпортовано {len(entries)} рядків у таблицю japanese_onomatopoeia.")
if skipped:
    print(f"Пропущено {len(skipped)} рядків.")
