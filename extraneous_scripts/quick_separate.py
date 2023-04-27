# self-evident
# just learn python if you can't figure out what this does
# or ask chatgpt

name = "4"
filename = "raw/greek/" + name + '.txt'

text = (open(filename).read())

result = ((text.replace('\n', '\n\n')).replace('\n\n\n', '\n\n')).replace('\n\n\n', '\n\n')

with open("./raw/greek/" + name + ".txt", "w") as file:
    file.writelines(result)