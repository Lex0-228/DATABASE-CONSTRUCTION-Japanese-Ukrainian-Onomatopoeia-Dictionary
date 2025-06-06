input_file = "Perun_slovnyk.txt"
output_file = "Perun_interjections.txt"
encoding = "utf-8"

# Зчитування вхідного тексту
with open(input_file, "r", encoding=encoding) as f:
    content = f.read()

# Розбиття на словникові статті
articles = content.strip().split('\n\n')

# Відбір лише тих, що містять "виг."
interjections = [entry.strip() for entry in articles if "виг." in entry]

# Запис результатів у файл
with open(output_file, "w", encoding="utf-8") as f:
    for article in interjections:
        f.write(article + "\n\n")

print(f"Збережено {len(interjections)} словникових статей із 'виг.' у файл: {output_file}")
