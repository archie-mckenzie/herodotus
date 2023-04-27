import json

# read the first JSON file
with open('output/jsons/sentences.json', 'r') as f:
    data1 = json.load(f)

# read the second JSON file
with open('output/jsons/chapters.json', 'r') as f:
    data2 = json.load(f)

# combine the two arrays of JSON objects
combined_data = data1 + data2

# write the merged JSON to a new file
with open('output/jsons/combined.json', 'w') as f:
    json.dump(combined_data, f)
