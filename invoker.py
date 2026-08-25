import json
import urllib.request

import requests
import pyperclip

from PyMultiDictionary import MultiDictionary

from ai import analyze_word

def invoke(action, params):
    request_data = {
        "action": action,
        "params": params,
        "version": 6
    }

    request_json = json.dumps(request_data).encode("utf-8")

    response = json.load(
        urllib.request.urlopen(
            urllib.request.Request(
                "http://127.0.0.1:8765",
                request_json
            )
        )
    )

    if "error" not in response:
        raise Exception("Response is missing required error field")

    if "result" not in response:
        raise Exception("Response is missing required result field")

    if response["error"] is not None:
        raise Exception(response["error"])

    return response["result"]

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
                meanings.append({
                    "part_of_speech": part_of_speech,
                    "definition": text,
                    "example": example
                })

    return meanings

def format_meanings(meanings):
    formatted = []

    for i, meaning in enumerate(meanings, start=1):
        part_of_speech = meaning["part_of_speech"]
        definition = meaning["definition"]
        example = meaning["example"]

        text = f"{i}. {part_of_speech}: {definition}"

        if example:
            text += f"\n   Example: {example}"

        formatted.append(text)

    return "\n\n".join(formatted)

def extract_first_part(text):
    # Find the index of the first newline character
    newline_index = text.find('\n')

    # Extract the substring before the first newline
    if newline_index != -1:
        first_part = text[:newline_index]
    else:
        first_part = text

    return first_part.strip()  # Remove leading and trailing whitespaces


def fill_anki_card():
    multi_dicc = MultiDictionary()

    clipboard_content = pyperclip.paste()
    sentence = extract_first_part(clipboard_content)

    print("\nThe sentence you provided:")
    print(sentence)

    word = input(
        "\nPlease input the word you want as an Anki card:\n"
    ).strip()

    if not word:
        raise ValueError("No word was provided.")

    print("\nLooking up dictionary definitions...")

    meanings = get_meaning(word)

    if not meanings:
        raise ValueError(
            f"No dictionary meanings found for '{word}'."
        )

    dictionary_text = format_meanings(meanings)

    print("\nGetting candidate synonyms...")

    synonyms = multi_dicc.synonym("en", word)

    print("\nAnalyzing word in context with Gemini...")

    result = analyze_word(
        word=word,
        sentence=sentence,
        dictionary_meanings=dictionary_text,
        candidate_synonyms=synonyms,
    )

    print("\nGemini selected:")
    print(f"Meaning: {result.meaning}")
    print(f"Part of speech: {result.part_of_speech}")
    print(f"Synonyms: {result.synonyms}")
    print(f"Translation: {result.translation}")

    return {
        "note": {
            "deckName": "test1",
            "modelName": "Kindle",
            "fields": {
                "Front": word,
                "Meaning": result.meaning,
                "Sentence": sentence,
                "Synonyms": ", ".join(result.synonyms),
                "Translation": result.translation,
                "PartOfSpeech": result.part_of_speech.value,
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