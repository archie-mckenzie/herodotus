# translate.py
# author: Archie McKenzie
# Uses a language model which takes in the refined, idiomatic English translation and Greek, 
# creates a new translation of Herodotus' Histories

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

# ----- EDITABLE VARIABLES ----- #
name = "5.92" 
english_path = "./prepared/refined_english/" + name + ".txt"
greek_path = "./prepared/greek/" + name + ".txt"
i = 93 # starting paragraph

# ----- PROCESS LINES ----- #

english_text = (open(english_path).readlines())
greek_text = (open(greek_path).readlines())

open("./output/" + name + ".txt", "w")

messages = [
        {"role": "system", "content": "You are a scholarly assistant who translates classical texts."}
]

for index, line in enumerate(english_text):

    final_line = ''

    prompt = "Translate this passage of Herodotus’ Histories from Ancient Greek into English. Use natural, modern English, but keep your sentence structure as close to the original Ancient Greek as possible:"

    prompt += "\n\n" + process_line(greek_text[index])

    prompt += "\n\nAn idiomatic translation to help you in your efforts:\n\n" + process_line(line)
     
    if (len(messages) > 3):
        messages = messages[-1:]
        messages.insert(0, {"role": "system", "content": "You are a scholarly assistant who translates classical texts."})

    messages.append({"role": "user", "content": prompt})

    # GPT-4 is often overloaded, so wrap this in a loop with try/except to retry until it works
    sleep_time = 2
    while True:
        try:
            completion = openai.ChatCompletion.create(
                model = "gpt-4",
                messages = messages,
                temperature = 0
            )
            break
        except:
            print("Sleeping for " + str(sleep_time) + " seconds and trying again")
            time.sleep(sleep_time)
            sleep_time *= 2
            if sleep_time > 8:
                messages = [
                    {"role": "system", "content": "You are a scholarly assistant who translates classical texts."},
                    {"role": "user", "content": prompt}
                ]
            continue
    
    messages.append(completion.choices[0].message)

    final_line += completion.choices[0].message.content.strip()
    
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

