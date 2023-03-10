# STEP 1
# Prepares the raw text for processing with a language model
# Formats the text into paragraphs

import re

name = "9"
filename = "raw/" + name + '.txt'
start = 1

#

def split_by_number(string):
    split_text = []
    current_index = 0
    number = start + 1
    while True:
        index = text.find(str(number) + '.', current_index)

        if index == -1:
            split_text.append(text[current_index:])
            break

        split_text.append(text[current_index:index])
        current_index = index
        number += 1
    return split_text

#

#

def process_lines(array):

    # regex pattern to match anything inside square brackets
    pattern = r'\[.*?\]'

    final = []
 
    for string in array:
        new_string = re.sub(pattern, '', string).replace("\n", " ").replace('  ', ' ') + '\n'
        final.append(new_string)

    return final
#

text = (open(filename).read())

result = split_by_number(text)

final_result = process_lines(result)

print(final_result[0])

with open("./prepared/" + name + ".txt", "w") as file:
    file.writelines(final_result)




