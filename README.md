# KindleFlashcards
#### Video Demo:  <URL HERE>
#### Description:

This program creates contextual English vocabulary
Anki cards from text copied from Kindle for PC. Below I included an instruction on how to
use it properly and set up the necessary requirements. 
Originally I wrote this program entirely without AI, both the code i have written, and the way the program looks
for the meaning/synonyms/translation etc. Seeing as AI was allowed in this final project I found it fitting and almost
necessary for me to get used to the AI workflow as it seems to become increasingly more important in the current age of
coding.

*copied from the below section describing the workflow of the program*

1. Copy a sentence/passage from Kindle.
2. The program detects the Kindle window.
3. Enter the English word you want to study.
4. Dictionary definitions and candidate synonyms are collected.
5. Gemini determines the contextual meaning, part of speech,
   relevant synonyms, and German translation.
6. The card is added to Anki through AnkiConnect.


Explanation of files:

main.py:

* The main python file were I call upon my other files, window_stuff and invoker, and finally add the anki card via anki
connect.

window_stuff.py:

* In this file I created various functions that enable me to find the Kindle Window, and switch automatically to the
  Python script window once a Sentence has been copied. If this didn't exist it would open the Script window whenever
  you copy anything anywhere, like this it only pops up when you copy something in the Kindle window.

invoker.py:

* This file serves to fill out the Anki card templates, as well as look up the word the user wants in the dictionary,
  and call upon the ai.py file to fill out the template.

ai.py:

* The AI is being giving strict demands to fulfill its job. It gets the word and the context of the Sentence in order
  to determine which words' meaning/synonyms/translations etc. it should use. some words have multiple meanings and the
  AI figures out in context which meaning is the one we want for the sentence we put in.

_

Design philosophy:

As said previously, this program initially had no AI in it. One challenge without AI was that if a word had multiple
meanings, i would not get correct synonyms/meaning/translation from webscraping thesaurus. 
for example: the word pitch could mean level/tilt or frequency, I dont want both of those definitions on the back of my
flash card; AI figures out the correct word from context and only gives me the relevant ones.

At first I wanted to implement an open source LLM like ollama but decided to end up going with a cloud service since
every pc will be able to run that. Gemini (as of writing this at least) has a free tier that is sufficient for this
programs' use case.

Theres a ton of things to improve and work on, which I might do in the future. Some of the things I might implement are:

* Flexibility in which AI model to use instead of hardcoding gemini.
* A UI instead of a script window
* Support for other software that is not kindle, perhaps even a browser plugin
* Languages other than english, as well as translations other than german. Ideally you can just choose this when
  starting the program for the first time or in the config.py


___
⚠ The project is currently Windows-specific and designed for
Kindle for PC + AnkiConnect.

This program creates contextual English vocabulary
Anki cards from text copied from Kindle for PC.

Workflow:

1. Copy a sentence/passage from Kindle.
2. The program detects the Kindle window.
3. Enter the English word you want to study.
4. Dictionary definitions and candidate synonyms are collected.
5. Gemini determines the contextual meaning, part of speech,
   relevant synonyms, and German translation.
6. The card is added to Anki through AnkiConnect.

## Current limitations

- Currently designed around Kindle for PC.
- The target word is entered manually.
- The program uses the first line of the clipboard contents as the sentence.
- Gemini is currently limited to noun, verb, and adjective classification.
- Anki must be running with AnkiConnect available.
___
## Anki setup

1. Install Anki.
2. Install the AnkiConnect add-on.
3. Make sure Anki is running while the program is active.
4. Create a deck named `test1`.
5. Create a note type named `Kindle`. ("Deck" and "note type" names, can be changed in config.py)
6. Add the following fields:


Front
Meaning
Sentence
Synonyms
Translation
PartOfSpeech
___
## Gemini API setup

This project uses Google's Gemini API for contextual word analysis.

1. Create a Gemini API key through Google AI Studio.
2. Create a `.env` file in the project directory.
3. Add:

GEMINI_API_KEY=your_key_here

The `.env` file is ignored by Git and must never be committed.