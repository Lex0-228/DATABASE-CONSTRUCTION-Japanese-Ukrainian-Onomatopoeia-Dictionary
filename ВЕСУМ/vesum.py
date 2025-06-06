input_file = "dict_corp_vis.txt"
output_file = "VESUM_intj.txt"
encoding = "utf-8"

filtered_lines = []

with open(input_file, "r", encoding=encoding) as f:
    for line in f:
        if "intj" in line:
            cleaned_line = line.replace("intj", "").strip()
            filtered_lines.append(cleaned_line)

#Запис результату у файл
with open(output_file, "w", encoding=encoding) as f:
    for line in filtered_lines:
        f.write(line + "\n")

print(f"Збережено {len(filtered_lines)} рядків без 'intj' у файл '{output_file}'")
