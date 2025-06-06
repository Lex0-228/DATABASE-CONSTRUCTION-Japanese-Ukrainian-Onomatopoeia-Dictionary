import sqlite3
import string
from fugashi import Tagger
from pykakasi import kakasi

# Створення аналізатора
tagger = Tagger()

def kana_to_romaji(text):
    result = []
    for word in tagger(text):
        surface = word.surface
        if surface in string.punctuation or surface.isspace():
            result.append(surface)
        else:
            result.append(word.feature.kana or surface)
    
    kks = kakasi()
    kks.setMode("H", "a")
    kks.setMode("K", "a")
    kks.setMode("J", "a")
    kks.setMode("r", "Hepburn")  # Hepburn Romanization
    conv = kks.getConverter()
    romaji = conv.do("".join(result))
    return romaji

# Підключення до бази
conn = sqlite3.connect("combined_dictionary.db")
cursor = conn.cursor()

tables = ["SFX_japanese_onomatopoeia_merged", "jp_onomatopoeia"]

for table in tables:
    cursor.execute(f"SELECT rowid, hiragana FROM {table}")
    rows = cursor.fetchall()

    for rowid, hiragana in rows:
        if isinstance(hiragana, str) and hiragana.strip():
            romaji = kana_to_romaji(hiragana)
            cursor.execute(
                f"UPDATE {table} SET romaji = ? WHERE rowid = ?",
                (romaji, rowid)
            )

# Зберігання змін
conn.commit()
conn.close()
print("Транскрипція romaji додана успішно.")

# Хіраґана та відповідна катакана
def hira_to_kata(text):
    result = ""
    for char in text:
        code = ord(char)
        if 0x3041 <= code <= 0x3096:
            result += chr(code + 0x60)
        else:
            result += char
    return result

# Підключення до бази
conn = sqlite3.connect("combined_dictionary.db")
cursor = conn.cursor()

# Зчитування хіраґани
cursor.execute("SELECT rowid, hiragana FROM jp_onomatopoeia")
rows = cursor.fetchall()

# Конвертація в катакану
for rowid, hira in rows:
    if isinstance(hira, str) and hira.strip():
        kata = hira_to_kata(hira)
        cursor.execute(
            "UPDATE jp_onomatopoeia SET katakana = ? WHERE rowid = ?",
            (kata, rowid)
        )

conn.commit()
conn.close()
print("Катакана оновлена.")
