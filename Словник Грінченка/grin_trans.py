import sqlite3
import pandas as pd
import openai
import time

openai.api_key = "api-key"  # Власний ключ OpenAI вилучено з коду

db_file = "hrinchenko_mezh1.db"  # база даних
table_name = "dictionary"        # початкова таблиця
new_table = "dictionary_translated"  # нова таблиця з перекладом

# Завантаження з бази
conn = sqlite3.connect(db_file)
df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

# Функція перекладу через OpenAI
def translate_openai(text, source_lang="російської", target_lang="українську"):
    prompt = f"Переклади з {source_lang} на {target_lang} наступний словниковий фрагмент:\n\n{text}\n\nПереклад:"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Помилка перекладу: {e}")
        return text

# Переклад кожного визначення
translated = []

for i, row in df.iterrows():
    original = row['definition']
    print(f"Переклад {i + 1}/{len(df)}")
    translation = translate_openai(original)
    translated.append(translation)
    time.sleep(1.2)

df['definition_ukr'] = translated

# апис у нову таблицю
cursor = conn.cursor()
cursor.execute(f"DROP TABLE IF EXISTS {new_table}")
cursor.execute(f"""
CREATE TABLE {new_table} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT,
    definition TEXT,
    definition_ukr TEXT,
    examples TEXT
)
""")

for _, row in df.iterrows():
    cursor.execute(f"""
    INSERT INTO {new_table} (word, definition, definition_ukr, examples)
    VALUES (?, ?, ?, ?)
    """, (row['word'], row['definition'], row['definition_ukr'], row['examples']))

conn.commit()
conn.close()

print(f"Перекладено {len(df)} записів і збережено у таблицю '{new_table}' у базі '{db_file}'")
