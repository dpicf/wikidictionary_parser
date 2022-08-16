import requests
from bs4 import BeautifulSoup

word_prop = {}


def get_one(word_url):
    url = 'https://ru.wiktionary.org' + word_url
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features="html.parser")
    morfo_table = soup.find("table", {"class": "morfotable"})
    words_table = morfo_table.find_all("td")
    h3 = soup.find_all("h3")
    print(h3)

    inter_words = []
    for word in words_table:
        if word.get('bgcolor') == '#ffffff':
            inter_words.append(word.text.strip())

    word_prop['word'] = inter_words[0]
    word_prop['ед_ч'] = {
        'им': inter_words[0],
        'род': inter_words[2],
        'дат': inter_words[4],
        'вин': inter_words[6],
        'тв': inter_words[8],
        'пр': inter_words[10]
    }
    word_prop['мн_ч'] = {
        'им': inter_words[1],
        'род': inter_words[3],
        'дат': inter_words[5],
        'вин': inter_words[7],
        'тв': inter_words[9],
        'пр': inter_words[11]
    }

    return word_prop


words = get_one('/wiki/ажиотаж')
# for key in words['ед_ч']:
#     print(key, '->', words['ед_ч'][key])
# print()
# for key in words['мн_ч']:
#     print(key, '->', words['мн_ч'][key])
