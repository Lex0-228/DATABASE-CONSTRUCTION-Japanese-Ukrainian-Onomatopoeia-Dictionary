import sqlite3
import re

input_file = "Hrinchenko_mezh_filtered.txt"  # текстовий файл зі словником
db_file = "hrinchenko_mezh.db"                # назва бази даних

# Зчитування вмісту файлу
with open(input_file, "r", encoding="utf-8") as f:
    content = f.read()

# Розбиття на словникові статті
entries = content.split("\n\n")

processed_data = []

for entry in entries:
    if 'меж.' not in entry:
        continue

    match = re.match(r"^(.*?)\s*меж\.\s*(.*)", entry.strip())
    if not match:
        continue

    word = match.group(1).strip()
    rest = match.group(2).strip()

    # Витягнення визначень
    definition = ""
    examples = ""
    def_match = re.match(r"(.+?[.!])(\s+(2\)|3\)|4\)|5\)|6\))?.*)", rest)

    if def_match:
        definition = def_match.group(1).strip()
        tail = def_match.group(2).strip()
        # якщо є ще кілька визначень, додаємо їх
        if re.match(r"^(2\)|3\)|4\)|5\)|6\))", tail):
            definition += " " + tail
            examples = rest[len(definition):].strip()
        else:
            examples = tail
    else:
        definition = rest
        examples = ""

    processed_data.append((word, definition, examples))

# Збереження базу
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

for word, definition, examples in processed_data:
    cursor.execute("INSERT INTO dictionary (word, definition, examples) VALUES (?, ?, ?)", (word, definition, examples))

conn.commit()
conn.close()

print(f"Успішно збережено {len(processed_data)} словникових записів у базу '{db_file}'")
