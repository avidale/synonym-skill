import requests
from dialogic.cascade import DialogTurn
from dialogic.nlu.basic_nlu import fast_normalize
from bs4 import BeautifulSoup


def find_synonyms(word):
    word = fast_normalize(word, lemmatize=True)
    text = word.replace(' ', '%20')
    resp = requests.get(f'https://www.ruwordnet.ru/ru/search/{text}')
    soup = BeautifulSoup(resp.text, 'html.parser')
    synsets = soup.find_all('div', {'class': 'synonyms'})
    texts = [
        [
            sense.text.strip(' \n,')
            for sense in ss.find_all('div', {'class': 'sense'})
        ]
        for ss in synsets
    ]
    return texts


def make_synonym_response(turn: DialogTurn, word=None):
    if not word:
        word = turn.text
    if not word:
        return
    syns = find_synonyms(word)
    all_synonyms = sorted({
        text for ss in syns for text in ss
        if word.upper() not in text.upper().split()
    })
    if not all_synonyms:
        turn.response_text = f'Простите, не нашла синонимов к слову "{word}".'
        return
    turn.response_text = f'Синонимы к слову "{word}":'
    for syn in all_synonyms[:-1]:
        turn.response_text += '\n' + syn + ';'
    turn.response_text += '\n' + all_synonyms[-1] + '.'

    turn.user_object['word'] = word
