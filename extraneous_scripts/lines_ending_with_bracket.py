
for i in range(9):
    # Open the file for reading
    lines = (open('raw/greek/' + str(i + 1) + ".txt").readlines())
    for line in lines:
        # Check if the line ends with ']'
        if line.strip().endswith(']'):
            print("Book " + str(i + 1) + ". Line ends with ']': " + line.strip())
