Räknar antalet förekomster av fraser i en textfil och skriver ut dem i terminalen om de överstiger en, på csv format
fras, antal förekomster

Användning.
python fras_koll.py <textfil> <minsta längd på frasen> <ignore/no>

Exempel att räkna fraser större eller lika med 4 och ignorera alla fraser som innehåller ett stopp ord ('och', 'i', 'men' och så vidare)
python fras_koll.py minfil.txt <4> ignore
