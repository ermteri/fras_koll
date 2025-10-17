import sys
from collections import Counter
import re
import os

# Lista över vanliga svenska stoppord (småord)
stopwords = {
    'li', 'och', 'i', 'på', 'att', 'en', 'det', 'som', 'av', 'med', 'för', 'är', 'till', 'den', 'om', 'ett', 'har', 'inte',
    'vi', 'de', 'han', 'men', 'var', 'hon', 'så', 'sig', 'jag', 'från', 'ut', 'nu', 'eller', 'över', 'vid', 'efter',
    'under', 'mot', 'genom', 'innan', 'sedan', 'bland', 'hos', 'kring', 'enligt', 'emot', 'trots', 'per', 'åt', 'inom',
    'utan', 'ovan', 'bakom', 'framför', 'bredvid', 'mellan', 'där', 'här', 'nu', 'då', 'när', 'hur', 'vad', 'vem',
    'vilken', 'vilket', 'vilka', 'denna', 'detta', 'dessa', 'sådan', 'sådant', 'sådana', 'ingen', 'inget', 'inga',
    'någon', 'något', 'några', 'alla', 'allt', 'allting', 'varje', 'annan', 'annat', 'andra', 'sin', 'sitt', 'sina',
    'hans', 'hennes', 'deras', 'vår', 'vårt', 'våra', 'din', 'ditt', 'dina', 'min', 'mitt', 'mina'
}

# Kontrollera kommandoradsargument
if len(sys.argv) != 4:
    print("Användning: python script.py <filnamn> <min_fraslängd> <ignore_stopwords>")
    print("  <min_fraslängd>: Minsta antal ord i fraser (räknar även längre fraser).")
    print("  <ignore_stopwords>: 'ignore' för att ignorera fraser med stoppord, annars valfri sträng för att inkludera alla.")
    sys.exit(1)

filename = sys.argv[1]
try:
    min_n = int(sys.argv[2])
    if min_n <= 0:
        print("Minsta fraslängd måste vara ett positivt heltal.")
        sys.exit(1)
except ValueError:
    print("Minsta fraslängd måste vara ett heltal.")
    sys.exit(1)

ignore_stopwords_flag = sys.argv[3].lower() == 'ignore'

# Kontrollera att filen existerar
if not os.path.isfile(filename):
    print(f"Filen {filename} finns inte.")
    sys.exit(1)

# Läs in textfilen
try:
    with open(filename, 'r', encoding='utf-8') as file:
        text = file.read()
except Exception as e:
    print(f"Kunde inte läsa filen {filename}: {e}")
    sys.exit(1)

# Rengör texten: till små bokstäver (case-insensitive), dela upp i ord med regex
words = re.findall(r'\b\w+\b', text.lower())

# För debugging: Skriv ut antal ord och de första 20 orden
print(f"Antal ord i texten: {len(words)}")
if words:
    print("Första 20 orden:", words[:20])
else:
    print("Inga ord i texten.")
    sys.exit(0)

# Kontrollera att det finns tillräckligt med ord för minsta fraslängd
if len(words) < min_n:
    print(f"Inte tillräckligt med ord för minsta fraslängd {min_n}. Behöver minst {min_n} ord.")
    sys.exit(0)

# Generera n-grams för längder från min_n till max_n (begränsa till min_n + 10 eller textlängd)
max_n = min(min_n + 10, len(words))  # Begränsa maximal fraslängd
phrases = Counter()
print("Genererar fraser...", flush=True)
for n in range(min_n, max_n + 1):
    for i in range(len(words) - n + 1):
        phrase = ' '.join(words[i:i+n])
        phrases[phrase] += 1
print("Frasgenerering klar!", flush=True)

# Filtrera fraser: förekommer mer än en gång, och eventuellt ignorera de med stoppord
filtered_phrases = [
    (phrase, count) for phrase, count in phrases.items()
    if count > 1 and (not ignore_stopwords_flag or all(word not in stopwords for word in phrase.split()))
]

# Sortera efter förekomster, descending
sorted_phrases = sorted(filtered_phrases, key=lambda x: x[1], reverse=True)

# Skriv ut i CSV-format
if not sorted_phrases:
    print(f"Inga återkommande fraser (mer än en gång, med minst {min_n} ord) hittades.")
else:
    for phrase, count in sorted_phrases:
        print(f"{phrase},{count}")
