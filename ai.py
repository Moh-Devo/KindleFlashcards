import os
from enum import Enum

from google import genai
from pydantic import BaseModel


class PartOfSpeech(str, Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"


class VocabularyResult(BaseModel):
    meaning: str
    part_of_speech: PartOfSpeech
    synonyms: list[str]
    translation: str


client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


def analyze_word(
    word: str,
    sentence: str,
    dictionary_meanings: str,
    candidate_synonyms: list[str],
) -> VocabularyResult:

    synonyms_text = ", ".join(candidate_synonyms)

    prompt = f"""
You are helping create an English vocabulary flashcard.

The user is reading an English book and wants to learn the word
"{word}".

Determine the EXACT meaning of "{word}" based on how it is used
in this sentence:

"{sentence}"

Here are dictionary definitions for the word:

{dictionary_meanings}

Here are candidate synonyms:

{synonyms_text}


Your task:

1. Determine the meaning of the target word in THIS sentence.

2. Give ONE concise English definition suitable for a vocabulary
   flashcard.

3. Determine the part of speech based on how the target word is
   actually used in THIS sentence.

4. The part of speech MUST be exactly one of:
   - noun
   - verb
   - adjective

5. Select AT MOST 3 synonyms that could naturally replace the
   target word in THIS specific sentence while preserving its
   meaning.

6. A word being generally related to the target word is NOT enough
   to be considered a synonym. Only include genuine contextual
   synonyms.

7. Do NOT include synonyms belonging to another meaning of the word.

8. Translate the target word as it is used in THIS sentence into
   German.

9. Return only ONE meaning.

10. Return only ONE German translation.

11. If fewer than 3 good synonyms exist, return fewer. It is better
    to return 1-2 accurate synonyms than 3 inaccurate ones.

12. If none of the candidate synonyms are appropriate, return an
    empty synonyms list.

13. Do not invent synonyms simply to fill the list.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": VocabularyResult,
        },
    )

    return VocabularyResult.model_validate_json(response.text)