import requests
from bs4 import BeautifulSoup
import re

file = open("./main.html", "w")
file.write('''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="./style.css">
    <title>Globbers Scraping</title>
</head>
<body>''')

city = input("Entrez la ville : ")

response = requests.get(f'https://fr.wikipedia.org/wiki/{city}')

file.write(f'''<section class="ctn">''')

if response is not None:
    html = BeautifulSoup(response.text, 'html.parser')

    title = html.select("#firstHeading")[0].text

    file.write(f'''<h1 class="title">
    Ville recherchée : {title}
    </h1>''')

    paragraphs = html.select("p")[2:][1:10]
    for para in paragraphs:
        text = re.sub('\[..|...]', '', para.text)
        text = re.sub('\ ̃ʁécouter', '', text)
        text = re.sub('\écouter', '', text)
        text = re.sub('\Écouter', '', text)
        text = re.sub('\]', '', text)
        requests.post('http://localhost:3000/data', {"description": " ".join(text.split())})
        file.write(f'''<p class="paragraph">
        {text}
    </p>''')

file.write(f'''</section>''')

file.write('''
    </body>
    </html>''')
