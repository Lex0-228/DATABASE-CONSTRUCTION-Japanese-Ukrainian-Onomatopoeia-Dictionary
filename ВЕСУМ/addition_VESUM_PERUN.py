import sqlite3

# Шляхи до файлів і бази
db_path = "combined_dictionary.db"
file_sources = {
    "Perun_interjections_edited.txt": "Великий тлумачний словник сучасної української мови вид. «Перун»",
    "not_found_VESUM_intj.txt": "Великий електронний словник української мови (ВЕСУМ)",
}

# Збір усіх записів
new_entries = []

for file, source in file_sources.items():
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Роздільник
            if "\t" in line:
                parts = line.split("\t", 1)
            elif " - " in line:
                parts = line.split(" - ", 1)
            else:
                continue  # пропустити, якщо немає жодного з роздільників

            word = parts[0].strip()
            definition = parts[1].strip()
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

print(f"Успішно додано {len(new_entries)} нових записів до бази '{db_path}'")
