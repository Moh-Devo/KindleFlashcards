import json
import urllib.request
# from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup
from PyMultiDictionary import MultiDictionary
# from deep_translator import GoogleTranslator
from googletrans import Translator
import pyperclip



def request(action, params):
    return {'action': action, 'params': params, 'version': 6}


def invoke(action, params):
    request_json = json.dumps(request(action, **params)).encode('utf-8')
    print(request_json)
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', request_json)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def translate_word(word):
    url = "https://api.mymemory.translated.net/get"

    params = {
        "q": word,
        "langpair": "en|de"
    }

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    data = response.json()
    return data["responseData"]["translatedText"]


def get_meaning(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    meanings = []

    for meaning in data[0].get("meanings", []):
        part_of_speech = meaning.get("partOfSpeech", "")

        for definition in meaning.get("definitions", []):
            text = definition.get("definition", "")
            example = definition.get("example")

            if text:
                if example:
                    meanings.append(
                        f"{part_of_speech}: {text}\nExample: {example}"
                    )
                else:
                    meanings.append(
                        f"{part_of_speech}: {text}"
                    )

    return "\n\n".join(meanings)


def get_synonyms(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'lxml')
    soup.find('section', {'class': 'css-17ofzyv e1ccqdb60'})
    return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})]
    # 'css-1gyuw4i eh475bn0' for less relevant synonyms


def prettify_dict(input_dict):
    # Convert each key-value pair to a formatted string
    formatted_items = [f"{key}: {value}" for key, value in input_dict.items()]

    # Join the formatted strings with commas
    result_string = ", ".join(formatted_items)

    result_string = result_string.replace('], ', ']\n')

    return result_string


def extract_first_part(text):
    # Find the index of the first newline character
    newline_index = text.find('\n')

    # Extract the substring before the first newline
    if newline_index != -1:
        first_part = text[:newline_index]
    else:
        first_part = text

    return first_part.strip()  # Remove leading and trailing whitespaces


def empty_check(synonym_list):
    empty_string = ""
    print(synonym_list)
    if synonym_list:
        return synonym_list
    else:
        return empty_string


def fill_anki_card():
    # dicc = PyDictionary()
    multi_dicc = MultiDictionary()
    clipboard_content = pyperclip.paste()
    sentence = extract_first_part(clipboard_content)
    print("The Sentence you provided: " + sentence)
    word = input('Please input the word you want as an Anki card:\n')
    # meaning = dicc.meaning(word)
    # meaning = prettify_dict(meaning)
    meaning = get_meaning(word)
    # translation = GoogleTranslator(source='en', target='de').translate(word)
    translation = translate_word(word)

    synonyms = multi_dicc.synonym('en', word)

    add_note = {
        "params": {
            "note": {
                "deckName": "test1",
                "modelName": "Kindle",
                "fields": {
                    "Front": word,
                    "Meaning": f'''{meaning}''',
                    "Sentence": sentence,
                    "Synonyms": f'{empty_check(synonyms)}',
                    "Translation": translation,

                },
                "options": {
                    "allowDuplicate": False,
                    "duplicateScope": "deck",
                    "duplicateScopeOptions": {
                        "deckName": "Default",
                        "checkChildren": False,
                        "checkAllModels": False
                    }
                },
                "tags": [
                    "Kindle Import"
                ]

            }
        }
    }
    return add_note
