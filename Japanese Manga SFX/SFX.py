import csv
from itertools import islice
import dataclasses
from typing import Optional
import re
from collections import defaultdict
import json

@dataclasses.dataclass()
class RawEntry:
    katakana: str
    english: str
    details: Optional[str]

def compile_japanese_manga_sfx_sheet(entries: list[RawEntry]):
        with open("SFX/JapaneseMangaSFX-Sheet1.csv", encoding="utf-8") as f:
            rows = list(csv.reader(f))
            katakana_columns = []
            for index, cell in enumerate(rows[1]):
                if cell == "Japanese":
                    katakana_columns.append(index)

            new_entries = []
            for index in katakana_columns:
                katakana, english, details = None, "", ""
                for row_index, row in islice(enumerate(rows), 2, None):
                    if row[index + 1].strip():
                        if katakana is not None:
                            new_entries.append(RawEntry(katakana, english, details))
                            english, details = "", ""
                        katakana = row[index].removesuffix(",")

                    english += row[index + 2] + " "
                    details += row[index + 3] + " "

                if katakana is not None:
                    new_entries.append(RawEntry(katakana, english, details))

            for entry in new_entries:
                english = entry.english
                english = re.sub(r"\s+", " ", english.strip())

                details = entry.details
                details = details.replace("More »", "")
                details = re.sub(r"\s+", " ", details.strip())

                english_split = re.split(r"\((\d+)\)", english)
                if len(english_split) == 1:
                    entries.append(RawEntry(entry.katakana, english, details or None))
                    continue

                details_items = {}
                details_split = re.split(r"\((\d+)\)", details)
                for index, string in enumerate(details_split):
                    if string.isdigit():
                        value = details_split[index + 1]
                        value = value.strip().removesuffix(";")
                        details_items[int(string)] = value

                for index, string in enumerate(english_split):
                    if string.isdigit():
                        english = english_split[index + 1]
                        english = english.strip().removesuffix(";")
                        details = details_items.get(int(string), None)
                        entries.append(RawEntry(entry.katakana, english, details))


def compile_raw_entries() -> list[RawEntry]:
    entries = []
    compile_japanese_manga_sfx_sheet(entries)
    return entries


def compile_entries(raw_entries: list[RawEntry]):
    entries = defaultdict(list)
    for entry in raw_entries:
        entries[entry.katakana].append({
            "english": entry.english,
            "details": entry.details,
        })
    return entries


def main():
    raw_entries = compile_raw_entries()
    entries = compile_entries(raw_entries)
    with open("onomatopoeia1.json", "w") as f:
        json.dump(entries, f, indent=2)


if __name__ == '__main__':
    main()
