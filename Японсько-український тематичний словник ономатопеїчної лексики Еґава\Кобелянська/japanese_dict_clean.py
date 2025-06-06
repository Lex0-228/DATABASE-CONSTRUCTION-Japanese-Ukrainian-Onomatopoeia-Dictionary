import re

# Зчитування тексту
with open("Yaponsko-ukrainskyi_tematychnyi_slovnyk_onomatopeichnoi_leksyky.txt", "r", encoding="utf-8") as file:
    text = file.read()

# Базове очищення
text = re.sub(r"\n{2,}", "\n", text)  # Подвійні переноси
text = re.sub(r"", "", text)  # Незрозумілі символи
text = re.sub(r"\n\d{2,3}\n", "\n", text)  # Номери сторінок
text = re.sub(
    r'(?<=[а-яА-ЯіІїЇєЄґҐ,\.;:\-\)\(…!?])\n(?=[а-яА-ЯіІїЇєЄґҐ\(/)])',
    ' ', text)  # Злиття українських речень
text = re.sub(
    r'(?<=[一-龯ぁ-んァ-ン])\n(?=[ー])', '', text)  # Японські з ー не переносяться

# 3. Об'єднання рядків для подальшої обробки
lines = text.splitlines()
i = 0
joined_lines = []

while i < len(lines):
    current = lines[i]

    # Умова для злиття "Близькі за значенням:" + "、" + "、"
    if ("Близькі за значенням:" in current and "、" in current and
            i + 1 < len(lines) and "、" in lines[i + 1]):
        current = current.rstrip() + " " + lines[i + 1].lstrip()
        i += 1

    joined_lines.append(current)
    i += 1

# Подальша обробка
result_lines = []
i = 0

while i < len(joined_lines):
    line = joined_lines[i]

    # ❌ Видалення рядків, що містять символ "～"
    if "～" in line:
        i += 1
        continue

    if "。" in line:
        # 🔁 Видалення рядків фуріґани
        j = len(result_lines) - 1
        while j >= 0:
            prev = result_lines[j]
            if re.search(r'[一-龯]', prev) or re.search(r'[а-яА-ЯіІїЇєЄґҐ]', prev):
                break
            elif re.fullmatch(r'[ぁ-んァ-ンー ]+', prev):
                result_lines.pop(j)
            j -= 1

        # Видалення рядків без канджі між "." і "。"
        j = len(result_lines) - 1
        while j >= 0:
            if result_lines[j].strip().endswith("."):
                break
            elif not re.search(r'[一-龯]', result_lines[j]):
                result_lines.pop(j)
            j -= 1

        # Злиття з попереднім
        if result_lines:
            result_lines[-1] = result_lines[-1].rstrip() + line.lstrip()
        else:
            result_lines.append(line)
    else:
        result_lines.append(line)

    i += 1

# 5. Збереження
with open("cleaned_step2_final_all_filtered.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(result_lines))

print("Очистка завершена.")
