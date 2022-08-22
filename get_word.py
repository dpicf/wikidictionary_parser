import requests
from bs4 import BeautifulSoup
import pprint

pp = pprint.PrettyPrinter(sort_dicts=False)
word_prop = {}

url = 'https://ru.wiktionary.org/wiki/ввергнувший'

req = requests.get(url)
soup = BeautifulSoup(req.text, features="html.parser")
morfo_table = soup.find("table", {"class": "morfotable"})
if morfo_table is not None:
    words_table = morfo_table.find_all("td")
all_h2 = soup.find_all("h2")
all_h1 = soup.find_all("h1")

# поиск всех вариантов слова
target_tags = []
for h2 in all_h2:
    if h2.find_previous_sibling('h1') is not None:
        if h2.find_previous_sibling('h1').text.strip() == 'Русский':
            target_tags.append(h2)
if not target_tags:
    for h1 in all_h1:
        if h1.text.strip() == 'Русский[править]' or h1.text.strip() == 'Русский':
            target_tags.append(h1)

words = []
for tag in target_tags:
    # Морфологические и синтаксические свойства
    target_p = tag.find_next_sibling('p').find_next_sibling('p').text.strip()
    morfo_p = target_p.replace("\xa0", " ")

    # Значения
    means_check = tag.find_next_sibling('h4')
    if means_check.text.strip() == 'Значение' or means_check.text.strip() == 'Значение[править]':
        means_ol = tag.find_next_sibling('ol')
        all_li = means_ol.find_all('li')
        means = []
        for li in all_li:
            if li.text.strip() != '' and li.text.strip() != '—':
                mean = li.text.strip().split("◆ ")[0]
                means.append(mean.replace("\xa0", " "))
    else:
        means = None

    # Синонимы
    synonyms_check = tag.find_next_sibling('h4').find_next_sibling('h4')
    if synonyms_check.text.strip() == 'Синонимы' or synonyms_check.text.strip() == 'Синонимы[править]':
        synonyms_ol = tag.find_next_sibling('ol').find_next_sibling('ol')
        all_li = synonyms_ol.find_all('li')
        synonyms = []
        for li in all_li:
            if li.text.strip() != '' and li.text.strip() != '—':
                synonym = li.text.strip()
                synonyms.append(synonym.replace("\xa0", " "))
    else:
        synonyms = None

    # Антонимы
    antonyms_check = tag.find_next_sibling('h4').find_next_sibling('h4').find_next_sibling('h4')
    if antonyms_check.text.strip() == 'Антонимы' or antonyms_check.text.strip() == 'Антонимы[править]':
        antonyms_ol = tag.find_next_sibling('ol').find_next_sibling('ol').find_next_sibling('ol')
        all_li = antonyms_ol.find_all('li')
        antonyms = []
        for li in all_li:
            if li.text.strip() != '' and li.text.strip() != '—':
                antonym = li.text.strip()
                antonyms.append(antonym.replace("\xa0", " "))
    else:
        antonyms = None

    # Гиперонимы
    hypernyms_check = tag.find_next_sibling('h4').find_next_sibling('h4').find_next_sibling('h4').find_next_sibling(
        'h4')
    if hypernyms_check.text.strip() == 'Гиперонимы' or hypernyms_check.text.strip() == 'Гиперонимы[править]':
        hypernyms_ol = tag.find_next_sibling('ol').find_next_sibling('ol').find_next_sibling('ol').find_next_sibling(
            'ol')
        all_li = hypernyms_ol.find_all('li')
        hypernyms = []
        for li in all_li:
            if li.text.strip() != '' and li.text.strip() != '—':
                hypernym = li.text.strip()
                hypernyms.append(hypernym.replace("\xa0", " "))
    else:
        hypernyms = None

    # Гипонимы
    hyponyms_check = tag.find_next_sibling('h4').find_next_sibling('h4').find_next_sibling('h4').find_next_sibling(
        'h4').find_next_sibling('h4')
    if hyponyms_check.text.strip() == 'Гипонимы' or hyponyms_check.text.strip() == 'Гипонимы[править]':
        hyponyms_ol = tag.find_next_sibling('ol').find_next_sibling('ol').find_next_sibling('ol').find_next_sibling(
            'ol').find_next_sibling('ol')
        all_li = hyponyms_ol.find_all('li')
        hyponyms = []
        for li in all_li:
            if li.text.strip() != '' and li.text.strip() != '—':
                hyponym = li.text.strip()
                hyponyms.append(hyponym.replace("\xa0", " "))
    else:
        hyponyms = None

    # Родственные слова
    relative_check = tag.find_next_sibling('h3').find_next_sibling('h3').find_next_sibling('h3').find_next_sibling('h3')
    if relative_check.text.strip() == 'Родственные слова' or relative_check.text.strip() == 'Родственные слова[править]':
        relatives_table = tag.find_next_sibling('table')
        all_li = relatives_table.find_all('li')
        relatives = {}
        for li in all_li:
            if li.text.strip() != '' and li.text.strip() != '—':
                relative = li.text.strip().split(': ')
                relatives[relative[0]] = relative[1].split(', ')
        if relatives == {}:
            relatives_table = tag.find_next_sibling('table').find_next_sibling('table')
            all_li = relatives_table.find_all('li')
            relatives = {}
            for li in all_li:
                if li.text.strip() != '' and li.text.strip() != '—':
                    relative = li.text.strip().split(': ')
                    relatives[relative[0]] = relative[1].split(', ')
            if relatives == {}:
                relatives_table = tag.find_next_sibling('table').find_next_sibling('table').find_next_sibling('table')
                all_li = relatives_table.find_all('li')
                relatives = {}
                for li in all_li:
                    if li.text.strip() != '' and li.text.strip() != '—':
                        relative = li.text.strip().split(': ')
                        try:
                            relatives[relative[0]] = relative[1].split(', ')
                        except:
                            relatives = None
    else:
        relatives = None

    # морфологическая таблица
    if morfo_table is not None:
        inter_words = []
        for words in words_table:
            if words.get('bgcolor') != '#EEF9FF' and words.get('bgcolor') != '#eef9ff':
                words_arr = words.get_text(strip=True, separator='\n').splitlines()
                if len(words_arr) == 1:
                    words_arr = words_arr[0].split(' ')
                # if '—' in words:
                #     inter_words.append(None)
                if ',' in words_arr:
                    words_arr.remove(',')
                inter_words.append(words_arr)

    # морфологическая таблица доп.глагол
    if morfo_table is not None and 'Глагол' in morfo_p:
        all_tr = morfo_table.find_all('tr')
        optional_verb = {}
        for tr in all_tr:
            all_td = tr.find_all('td')
            if len(all_td) <= 2 and len(all_td) != 0:
                if all_td[0].text.strip() == 'Будущее':
                    optional_verb[all_td[0].text.strip()] = all_td[1].text.strip().split(' ')[1]
                else:
                    optional_verb[all_td[0].text.strip()] = all_td[1].text.strip().split(' ')

    # составление информации о слове
    if len(target_tags) == 1:
        word_prop['word'] = soup.find("h1").text.strip()
    else:
        word_prop['word'] = tag.text.strip()
    word_prop['morfo_prop'] = morfo_p

    if 'Существительное' in morfo_p or 'существительное' in morfo_p:
        try:
            word_prop['morfo_table'] = {
                'ед. ч.': {
                    'Им.': inter_words[0],
                    'Р.': inter_words[2],
                    'Д.': inter_words[4],
                    'В.': inter_words[6],
                    'Т.': inter_words[8],
                    'П.': inter_words[10]
                },
                'мн. ч.': {
                    'Им.': inter_words[1],
                    'Р.': inter_words[3],
                    'Д.': inter_words[5],
                    'В.': inter_words[7],
                    'Т.': inter_words[9],
                    'П.': inter_words[11]
                }
            }
        except:
            word_prop['morfo_table'] = None
        count = 11
        if len(inter_words) > count + 1:
            print(
                '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!error какое-то слово не попало в морфо-таблицу - ' + word_prop['word'])
    elif 'Глагол' in morfo_p or 'глагол' in morfo_p:
        try:
            word_prop['morfo_table'] = {
                'наст.': {
                    'Я': inter_words[0],
                    'Ты': inter_words[3],
                    'Он Она Оно': inter_words[6],
                    'Мы': inter_words[9],
                    'Вы': inter_words[12],
                    'Они': inter_words[15],
                },
                'прош.': {
                    'Я': inter_words[1],
                    'Ты': inter_words[4],
                    'Он Она Оно': inter_words[7],
                    'Мы': inter_words[10],
                    'Вы': inter_words[13],
                    'Они': inter_words[16],
                },
                'повелит.': {
                    'Я': inter_words[2],
                    'Ты': inter_words[5],
                    'Он Она Оно': inter_words[8],
                    'Мы': inter_words[11],
                    'Вы': inter_words[14],
                    'Они': inter_words[17],
                },
                'Пр. действ. наст.': optional_verb['Пр. действ. наст.'] if 'Пр. действ. наст.' in optional_verb else None,
                'Пр. действ. прош.': optional_verb['Пр. действ. прош.'] if 'Пр. действ. прош.' in optional_verb else None,
                'Деепр. наст.': optional_verb['Деепр. наст.'] if 'Деепр. наст.' in optional_verb else None,
                'Деепр. прош.': optional_verb['Деепр. прош.'] if 'Деепр. прош.' in optional_verb else None,
                'Пр. страд. наст.': optional_verb['Пр. страд. наст.'] if 'Пр. страд. наст.' in optional_verb else None,
                'Пр. страд. прош.': optional_verb['Пр. страд. прош.'] if 'Пр. страд. прош.' in optional_verb else None,
                'Будущее': optional_verb['Будущее'] if 'Будущее' in optional_verb else None,
            }
        except:
            word_prop['morfo_table'] = None
        # count = 24
        # if len(inter_words) > count + 1:
        #     print(
        #         '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!error какое-то слово не попало в морфо-таблицу - ' + word_prop['word'])
    elif 'Прилагательное' in morfo_p or 'прилагательное' in morfo_p:
        try:
            word_prop['morfo_table'] = {
                'ед. ч.': {
                    'муж. р.': {
                        'Им.': inter_words[0],
                        'Р.': inter_words[4],
                        'Д.': inter_words[8],
                        'В.': {
                            'одуш.': inter_words[12],
                            'неод.': inter_words[16],
                        },
                        'Т.': inter_words[18],
                        'П.': inter_words[22],
                        'Кратк. форма': inter_words[26] if 26 <= len(inter_words) - 1 else None
                    },
                    'ср. р.': {
                        'Им.': inter_words[1],
                        'Р.': inter_words[5],
                        'Д.': inter_words[9],
                        'В.': {
                            'одуш.': inter_words[13],
                            'неод.': inter_words[13],
                        },
                        'Т.': inter_words[19],
                        'П.': inter_words[23],
                        'Кратк. форма': inter_words[27] if 27 <= len(inter_words) - 1 else None
                    },
                    'жен. р.': {
                        'Им.': inter_words[2],
                        'Р.': inter_words[6],
                        'Д.': inter_words[10],
                        'В.': {
                            'одуш.': inter_words[14],
                            'неод.': inter_words[14],
                        },
                        'Т.': inter_words[20],
                        'П.': inter_words[24],
                        'Кратк. форма': inter_words[28] if 28 <= len(inter_words) - 1 else None
                    }
                },
                'мн. ч.': {
                    'Им.': inter_words[3],
                    'Р.': inter_words[7],
                    'Д.': inter_words[11],
                    'В.': {
                        'одуш.': inter_words[15],
                        'неод.': inter_words[17],
                    },
                    'Т.': inter_words[21],
                    'П.': inter_words[25],
                    'Кратк. форма': inter_words[29] if 29 <= len(inter_words) - 1 else None
                }
            }
        except:
            word_prop['morfo_table'] = None
        # count = 29
        # if len(inter_words) > count + 1:
        #     print(
        #         '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!error какое-то слово не попало в морфо-таблицу - ' + word_prop['word'])
    elif 'Причастие' in morfo_p or 'причастие' in morfo_p:
        try:
            word_prop['morfo_table'] = {
                'ед. ч.': {
                    'муж. р.': {
                        'Им.': inter_words[0],
                        'Р.': inter_words[4],
                        'Д.': inter_words[8],
                        'В.': {
                            'одуш.': inter_words[12],
                            'неод.': inter_words[16],
                        },
                        'Т.': inter_words[18],
                        'П.': inter_words[22],
                        'Кратк. форма': inter_words[26] if 26 <= len(inter_words) - 1 else None
                    },
                    'ср. р.': {
                        'Им.': inter_words[1],
                        'Р.': inter_words[5],
                        'Д.': inter_words[9],
                        'В.': {
                            'одуш.': inter_words[13],
                            'неод.': inter_words[13],
                        },
                        'Т.': inter_words[19],
                        'П.': inter_words[23],
                        'Кратк. форма': inter_words[27] if 27 <= len(inter_words) - 1 else None
                    },
                    'жен. р.': {
                        'Им.': inter_words[2],
                        'Р.': inter_words[6],
                        'Д.': inter_words[10],
                        'В.': {
                            'одуш.': inter_words[14],
                            'неод.': inter_words[14],
                        },
                        'Т.': inter_words[20],
                        'П.': inter_words[24],
                        'Кратк. форма': inter_words[28] if 28 <= len(inter_words) - 1 else None
                    }
                },
                'мн. ч.': {
                    'Им.': inter_words[3],
                    'Р.': inter_words[7],
                    'Д.': inter_words[11],
                    'В.': {
                        'одуш.': inter_words[15],
                        'неод.': inter_words[17],
                    },
                    'Т.': inter_words[21],
                    'П.': inter_words[25],
                    'Кратк. форма': inter_words[29] if 29 <= len(inter_words) - 1 else None
                }
            }
        except:
            word_prop['morfo_table'] = None
        # count = 29
        # if len(inter_words) > count + 1:
        #     print(
        #         '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!error какое-то слово не попало в морфо-таблицу - ' + word_prop['word'])
    else:
        word_prop['morfo_table'] = None

    word_prop['means'] = means
    word_prop['synonyms'] = synonyms
    word_prop['antonyms'] = antonyms
    word_prop['hypernyms'] = hypernyms
    word_prop['hyponyms'] = hyponyms
    word_prop['relatives'] = relatives

    pp.pprint(word_prop)
    print('-----------------------------------------------------------------------')

# нужны ли Этимология и Фразеологизмы?
