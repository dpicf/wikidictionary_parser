from get_word import get_one
from get_words import get_words

words = get_words('А')
for word_url in words:
    word = get_one(word_url)
    if len(word) == 0:
        print('00000 ' + word_url)
    if len(word) == 2:
        print('22222 ' + word_url)
