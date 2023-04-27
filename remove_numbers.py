# creates a copy of a given prepared text without paragraph numbers

name = "1"
path = "prepared/greek/" + name + ".txt"

# Read lines from input_file.txt
with open(path, 'r') as infile:
    lines = infile.readlines()

# Write sorted lines to output_file.txt
with open('output/without_numbers/greek/' + name + '.txt', 'w') as outfile:
    for line in lines:
        raw_line = ""
        for i, word in enumerate(line.split(' ')[1:]):
            raw_line += word
            if (i < len(line.split(' ')[1:]) - 1):
                raw_line += " "
        outfile.write(raw_line)