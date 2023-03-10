# STEP 2
# Uses a language model to rewrite the prepared archaic text into a new text

import openai
import os
from dotenv import load_dotenv
import re

# Load the API key from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

def process_line(line):
    return " ".join(line.strip().split()[1:])

def split_string(string):
    result = []
    in_quotes = False
    current_word = ''
    for char in string:
        if char == '"':
            in_quotes = not in_quotes
        elif char == '.' and not in_quotes:
            result.append(current_word)
            current_word = ''
        else:
            current_word += char
    result.append(current_word)
    return result


# Variables
name = "1"
path = "./prepared/" + name + ".txt"
lines = (open(path).readlines())
i = 0 # starting paragraph

open("./output/" + name + ".txt", "w")

for line in lines:

    line = process_line(line)
    sentences = split_string(line)

    final_line = ''

    messages = [
        {"role": "system", "content": "You are a scholarly assistant who edits classical texts. You are working on the following passage: " + line}
    ]

    print()
    for sentence in sentences:
        # Call the OpenAI API to generate a summary
        if len(sentence.strip()) < 4:
            continue

        print('Sentence: ' + sentence)

        if (sentence == sentence[0]):
            prompt = "Rewrite the following sentence into modern, fluid, easily readable English." 
        else:
            prompt = "Continue rewriting the passage. Rewrite the following sentence into modern, fluid, easily readable English."
        if (sentence.__contains__('"')):
            print("TRUE")
            prompt += " Include direct speech in quotation marks if necessary."
        prompt += "\n\nOld sentence:\n\n" + sentence + ".\n\nNew sentence(s):"
        messages.append({"role": "user", "content": prompt})

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages,
            temperature = 0
        )
        
        final_line += completion.choices[0].message.content.strip() + ' '

        messages.append(completion.choices[0].message)
    print()
    
    translation = str(i) + ". " + final_line + "\n"
    
    i += 1

    print('----------')
    print(line.strip())
    print()
    print(translation.strip())
    print('----------')

    with open("./output/" + name + ".txt", "a") as file:
        file.write(translation)


