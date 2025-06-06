import sqlite3

db_path = "combined_dictionary.db"
file_sources = {
    "from_blog.txt": "raphnana.livejournal.com",
    "from_NI.txt": "З напрацювань видавництва «Nasha Idea»."
}

# Збір усіх записів
new_entries = []

for file, source in file_sources.items():
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "	" not in line:
                continue
            word, definition = line.split("	", 1)
            word = word.strip()
            definition = definition.strip()
            new_entries.append((word, definition, "", source))

# Запис у базу
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Упевненитись, що колонка source існує
cursor.execute("PRAGMA table_info(dictionary)")
columns = [row[1] for row in cursor.fetchall()]
if "source" not in columns:
    cursor.execute("ALTER TABLE dictionary ADD COLUMN source TEXT")

# Додавання нових записів
cursor.executemany("""
    INSERT INTO onomatopoeia_dictionary (word, definition, examples, source)
    VALUES (?, ?, ?, ?)
""", new_entries)

conn.commit()
conn.close()

print(f"Успішно додано {len(new_entries)} нових записів до бази {db_path}")
