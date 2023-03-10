# STEP 2
# Uses a language model to rewrite the prepared archaic text into a new text

import openai
import os
from dotenv import load_dotenv

# Load the API key from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openai_api_key

def process_line(line):
    return " ".join(line.strip().split()[1:])

# MAGIC

# Variables
name = "1"
path = "./prepared/" + name + ".txt"
lines = (open(path).readlines())
i = 0 # starting paragraph

open("./output/" + name + ".txt", "w")

for line in lines:

    line = process_line(line)
    sentences = line.split('.')

    final_line = ''

    messages = [
        {"role": "system", "content": "You are an assistant with great knowledge of Herodotus' Histories."}
    ]

    print()
    for sentence in sentences:
        # Call the OpenAI API to generate a summary
        if len(sentence.strip()) < 4:
            continue

        print('Sentence: ' + sentence)
        
        prompt = "Rewrite the following sentence into modern, fluid, readable English. Do not use archaic vocabulary.\n\nOld sentence:\n\n" + sentence + ".\n\nNew sentence(s):"
        messages.append({"role": "user", "content": prompt})

        completion = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
            messages = messages,
            temperature = 0
        )
        
        final_line += completion.choices[0].message.content + ' '

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


