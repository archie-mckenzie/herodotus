# prepare_greek.py
# author: Archie McKenzie
# Takes raw Greek text and formats/standardizes it

# ----- IMPORTS ----- #

import re

# ----- EDITABLE VARIABLES ----- #

name = "1"
filename = "raw/greek/" + name + '.txt'
index = 0

# ----- FUNCTIONS ----- #

def process_lines(array):
    global index

    final = []
 
    for string in array:
        # remove any square brackets
        new_string = re.sub(r"\[|\]", '', string)
        # remove any leftover abbreviations
        new_string = new_string.replace(". . . ", '')
        # remove any latin letters and arabic numerals
        new_string = re.sub(r'[a-zA-Z]', '', new_string)
        new_string = re.sub(r'[0-9]', '', new_string)
        # replace newline characters and multiple spaces with a single space
        new_string = new_string.replace("\n", " ").replace('  ', ' ') + '\n'
        # make sure there is no whitespace at the beginning
        while (new_string[0] == ' '):
            new_string = new_string[1:]
        final.append(str(index) + ". " + new_string)
        index += 1

    return final

# ----- PROCESSING ----- #

text = (open(filename).read())

result = text.split('\n\n')

final_result = process_lines(result)

print(final_result[10])

with open("./prepared/greek/" + name + ".txt", "w") as file:
    file.writelines(final_result)




