import sqlite3
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from tqdm import tqdm
import re

# Завантаження моделі
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Підключення до бази даних
conn = sqlite3.connect("combined_dictionary.db")
cursor = conn.cursor()

# Отримання унікальних категорій, що присутні в обох таблицях
cursor.execute("SELECT DISTINCT category FROM merged_ukrainian_onomatopoeia")
ukr_categories = set(row[0] for row in cursor.fetchall())

cursor.execute("SELECT DISTINCT category FROM merged_onomatopoeia")
jap_categories = set(row[0] for row in cursor.fetchall())

common_categories = sorted(ukr_categories & jap_categories)

# Створення таблиці для результатів
cursor.execute("DROP TABLE IF EXISTS semantic_similarity")
cursor.execute("""
    CREATE TABLE semantic_similarity (
        ukr_word TEXT,
        ukr_definition TEXT,
        jap_definition TEXT,
        category TEXT,
        similarity REAL
    )
""")

# По кожній спільній категорії
for category in tqdm(common_categories, desc="Processing categories"):
    # Дані з української таблиці
    ukr_df = pd.read_sql_query("""
        SELECT word, definition FROM merged_ukrainian_onomatopoeia
        WHERE category = ?
    """, conn, params=(category,))

    # Визначення з японської таблиці
    jap_df = pd.read_sql_query("""
        SELECT definition FROM merged_onomatopoeia
        WHERE category = ?
    """, conn, params=(category,))

    # Пропуск категорій без пар
    if ukr_df.empty or jap_df.empty:
        continue

    # Обчислення векторів
    ukr_sentences = (ukr_df['word'] + " " + ukr_df['definition']).tolist()
    jap_sentences = jap_df['definition'].tolist()

    ukr_embeddings = model.encode(ukr_sentences, convert_to_tensor=True, show_progress_bar=False)
    jap_embeddings = model.encode(jap_sentences, convert_to_tensor=True, show_progress_bar=False)

    # Обчислення косинусної подіості
    similarities = util.pytorch_cos_sim(ukr_embeddings, jap_embeddings)

    # Збирання даних до запису
    data_to_insert = []
    for i, ukr_row in ukr_df.iterrows():
        for j, jap_def in enumerate(jap_df['definition']):
            similarity_score = float(similarities[i][j])
            data_to_insert.append((
                ukr_row['word'], ukr_row['definition'], jap_def, category, similarity_score
            ))

    # Запис у базу
    cursor.executemany("""
        INSERT INTO semantic_similarity (ukr_word, ukr_definition, jap_definition, category, similarity)
        VALUES (?, ?, ?, ?, ?)
    """, data_to_insert)

    conn.commit()

print("Дані записано у таблицю 'semantic_similarity'.")


# Таблицю для кешу
cursor.execute("DROP TABLE IF EXISTS jp_embeddings")
cursor.execute("""
CREATE TABLE jp_embeddings (
    query_form TEXT PRIMARY KEY,
    embedding BLOB
)
""")

# Додати відсутні ембединги до таблиці
jp_rows = pd.read_sql_query("""
    SELECT hiragana, katakana, romaji FROM merged_onomatopoeia
""", conn)

added = 0
for _, row in jp_rows.iterrows():
    for col in ['hiragana', 'katakana', 'romaji']:
        val = row[col]
        if val:
            for part in re.split(r'[/\s]', val.strip().lower()):
                if part:
                    cursor.execute("SELECT 1 FROM jp_embeddings WHERE query_form = ?", (part,))
                    if not cursor.fetchone():
                        emb = model.encode(part)
                        emb_blob = emb.astype('float32').tobytes()
                        cursor.execute("INSERT INTO jp_embeddings (query_form, embedding) VALUES (?, ?)", (part, emb_blob))
                        added += 1

conn.commit()
print(f"Додано {added} ембедингів до кешу")

conn.close()




