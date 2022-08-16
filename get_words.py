import requests
from bs4 import BeautifulSoup


def get_words(char):
    base_url = 'https://ru.wiktionary.org'
    url = base_url + '/wiki/Индекс:Русский_язык/' + char
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features="html.parser")
    div = soup.find("div", {"class": "index"})
    p_list = div.find_all("p")
    # '<a href="/wiki/%D0%B0" title="а">а</a>'
    end_links = ['/wiki/%D0%B0']

    for li in div.find_all("li"):
        end_links.append(li.find('a').get('href'))

    def get_inner_links(p_tags):
        for p in p_tags:
            inner_url = base_url + p.find('a').get('href')
            inner_req = requests.get(inner_url)
            inner_soup = BeautifulSoup(inner_req.text, features="html.parser")
            inner_div = inner_soup.find("div", {"class": "mw-body-content"})
            inner_all_li = inner_div.find_all("li")
            for inner_li in inner_all_li:
                if inner_li.get('class') is None:
                    end_links.append(inner_li.find('a').get('href'))

    get_inner_links(p_list)
    return end_links

    # for link in end_links:
    #     print(link)
    #     print(link.get('title'))
    #     print(base_url + link.get('href'))
