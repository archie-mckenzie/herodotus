# create_data_jsons.py
# author: Archie McKenzie

# ----- IMPORTS ----- #

import openai
import os
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

# Import natural language toolkit
import nltk
import ssl
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('punkt')

# Import time for dealing with rate-limits
import time

# Import json
import json

# for processing greek words
from unidecode import unidecode
import unicodedata
import re

# -----  1: WRITES EACH GREEK WORD IN HERODOTUS----- #
# As a JSON, with attributes word/transliteration/book/chapter/index/englishChapterText/greekChapterText/parsing/meaning
# Parsing and meaning are initially blank, filled-in with demand by gpt-3.5-turbo when the app is live

def has_combining_reversed_comma_above(word):
    for char in word:
        if '\u0314' in unicodedata.normalize('NFD', char):
            return True
    return False

# Transliterate a Greek word into English, so e.g. 'ἀνθρώπων' becomes 'anthropon'
# e.g. 'Ἡροδότου' becomes5 'Herodotou'
def transliterate(word):
    transliteration = unidecode(word)
    if has_combining_reversed_comma_above(word):
        if (transliteration[0].isupper()):
            return "H" + transliteration.lower()
        else: return "h" + transliteration
    else: return transliteration

def get_word_array(sentence):
    return re.findall(r'\w+', sentence)

greek_words = []

for i in range(9):
    
    lines = (open("output/without_numbers/english/" + str(i + 1) + ".txt").readlines())
    greek_lines = (open("output/without_numbers/greek/" + str(i + 1) + ".txt").readlines())

    for chapter, line in enumerate(greek_lines):

        for index, word in enumerate(get_word_array(line)):

            word_json = {
                "word": word.strip(),
                "transliteration": transliterate(word.strip()),
                "book": i + 1,
                "chapter": chapter if (i == 0) else chapter + 1,
                "index": index,
                "englishChapterText": lines[chapter].strip(),
                "greekChapterText": greek_lines[chapter].strip(),
                "parsing": "",
                "meaning": "",
                "dictionaryForm": "",
                "dictionaryFormTransliteration": ""
            }

            greek_words.append(word_json)

with open("output/jsons/greek_words.json", 'w') as output:
    json.dump(greek_words, output, indent = 4)

# ----- 2: WRITES EACH SENTENCE IN HERODOTUS ----- #
# As a JSON, with attributes: sentence/book/chapter/embedding

# Split any given string into sentences
# Return an array of strings
def split_into_sentences(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

sentence_jsons = [] # array of jsons

for i in range(9):
    
    lines = (open("output/without_numbers/english/" + str(i + 1) + ".txt").readlines())

    for chapter, line in enumerate(lines):

        sentences = split_into_sentences(line)

        for index, sentence in enumerate(sentences):

            # create embedding
            sleep_time = 2
            while True:
                try:
                    response = openai.Embedding.create(
                        input = sentence,
                        model = "text-embedding-ada-002"
                    )
                    embedding = response['data'][0]['embedding']
                    print("Embedded H." + str(i + 1) + "." + str(chapter if (i == 0) else chapter + 1) + " sentence " + str(index + 1) + "/" + str(len(sentences)))
                    break
                except:
                    print('Error. Sleeping for ' + str(sleep_time) + ' seconds then trying again...')
                    time.sleep(sleep_time)
                    sleep_time += 2
                    continue

            sentence_json = {
                "sentence": sentence.strip(),
                "book": i + 1,
                "chapter": chapter if (i == 0) else chapter + 1,
                "embedding": embedding
            }

            sentence_jsons.append(sentence_json)

with open("output/jsons/sentences.json", 'w') as output:
    json.dump(sentence_jsons, output, indent = 4)

# -----  3: WRITES EACH CHAPTER IN HERODOTUS----- #
# As a JSON, with attributes: english/greek/book/chapter/embedding

chapter_jsons = [] # array of jsons

for i in range(9):
    
    lines = (open("output/without_numbers/english/" + str(i + 1) + ".txt").readlines())
    greek_lines = (open("output/without_numbers/greek/" + str(i + 1) + ".txt").readlines())

    for chapter, line in enumerate(lines):

        # create embedding
        sleep_time = 2
        while True:
            try:
                response = openai.Embedding.create(
                    input = line,
                    model = "text-embedding-ada-002"
                )
                embedding = response['data'][0]['embedding']
                print("Embedded H." + str(i + 1) + "." + str(chapter if (i == 0) else chapter + 1))
                break
            except:
                print('Error. Sleeping for ' + str(sleep_time) + ' seconds then trying again...')
                time.sleep(sleep_time)
                sleep_time += 2
                continue

        chapter_json = {
            "english": line.strip(),
            "greek": greek_lines[chapter].strip(),
            "book": i + 1,
            "chapter": chapter if (i == 0) else chapter + 1,
            "embedding": embedding
        }

        chapter_jsons.append(chapter_json)

with open("output/jsons/chapters.json", 'w') as output:
    json.dump(chapter_jsons, output, indent = 4)