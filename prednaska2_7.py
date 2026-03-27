import re

text = "Dnes je 27. 3. 2026. Cena produktu je 1 000 Kč a cena služby je 200 Kč. Což je celkem 1 200 Kč. Dnešní sleva je 20%"

pattern_price = r"[1-9][0-9]{0,2}(?: [0-9]{3})* Kč"
pattern_data = r"\d{1,2}\.\s\d{1,2}\.\s\d{4}"

matches = re.findall(pattern_price, text)
matches_data = re.findall(pattern_data, text)

print(re.sub(pattern_price, "XXX Kč", text))

print(matches_data)
print(matches)