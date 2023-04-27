# rewrite.py
# author: Archie McKenzie
# Uses a language model to rewrite the prepared archaic text of Herodotus' Histories into a new text

# ----- IMPORTS ----- #

import openai
import os
from dotenv import load_dotenv
import time, datetime

# Load the API key from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

# ----- FUNCTIONS ----- #

def process_line(line):
    return " ".join(line.strip().split()[1:])

def is_direct_speech(line):
    for char in line:
        if char == '"':
            return True
    return False

# ----- EDITABLE VARIABLES ----- #
name = "remainder" 
path = "./prepared/english/" + name + ".txt"
i = 139 # starting paragraph

# ----- PROCESS LINES ----- #

lines = (open(path).readlines())

open("./output/" + name + ".txt", "w")

messages = [
        {"role": "system", "content": "You are a scholarly assistant who rewrites classical texts into simple English."}
]

for line in lines:

    line = process_line(line)
    final_line = ''

    prompt = "Rewrite the following passage into simple, fluid, easily readable English"

    if (is_direct_speech(line)):
        print('contains direct speech? y')
        prompt += ". If there is direct speech with quotation marks in the original passage, use direct speech with quotation marks in your rewriting. "
        prompt += "Original passage:\n\n" + line + "\n\nRewritten passage:"
    else:
        prompt += ":\n\n" + line

    if (len(messages) > 10):
        messages = messages[-5:]
        messages.insert(0, {"role": "system", "content": "You are a scholarly assistant who rewrites classical texts into simple English."})

    messages.append({"role": "user", "content": prompt})

    # GPT-4 is often overloaded, so wrap this in a loop with try/except to retry until it works
    while True:
        try:
            completion = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = messages,
                temperature = 0
            )
            break
        except:
            time.sleep(2)
            continue
    
    messages.append(completion.choices[0].message)
    final_line += completion.choices[0].message.content.strip().replace('\n\n', ' ').replace('\n', ' ') + ' '
    
    translation = str(i) + ". " + final_line + "\n"
    
    i += 1

    print('----------')
    print(line.strip())
    print()
    print(translation.strip())
    print('----------')
    print(datetime.datetime.now())

    with open("./output/" + name + ".txt", "a") as file:
        file.write(translation)

