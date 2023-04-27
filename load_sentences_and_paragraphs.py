# LOADS ALL SENTENCE AND CHAPTER JSONS FROM output/jsons/sentences.json AND output/jsons/chapters.json INTO THE DATABASE
# Sentences as a JSON, with attributes: sentence/book/chapter/embedding
# Chapters as a JSON, with attributes: english/greek/book/chapter/embedding

# LOADS EACH GREEK WORD JSON FROM output/jsons/greek_words.json INTO THE DATABASE
# With attributes word/transliteration/book/chapter/index/englishChapterText/greekChapterText/parsing/meaning
# Parsing and meaning are initially blank, filled-in with demand by gpt-3.5-turbo when the app is live

import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi

# Load the API key from the .env file
load_dotenv()

# Replace these with your MongoDB connection details
mongo_uri = os.getenv("MONGODB_CONNECTION_STRING")
db_name = "histories"
collection_name = "sentences"
json_file_path = "output/jsons/sentences.json"

# Connect to MongoDB
client = MongoClient(mongo_uri, tlsCAFile=certifi.where())
db = client[db_name]
collection = db[collection_name]

# Read the JSON file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

# Validate that the data is a list of JSON objects
if isinstance(json_data, list):
    # Insert each JSON object into the MongoDB collection
    length = len(json_data)
    index = 1
    for json_object in json_data:
        if isinstance(json_object, dict):
            collection.insert_one(json_object)
            print("Inserted sentence " + str(index) + "/" + str(length))
            index += 1
        else:
            print(f"Skipping non-JSON object: {json_object}")
else:
    print("The file does not contain a list of JSON objects.")

# ----- INSERT CHAPTERS ----- #

collection_name = "chapters"
collection = db[collection_name]
json_file_path = "output/jsons/chapters.json"

# Read the JSON file
with open(json_file_path, 'r') as file:
    json_data = json.load(file)

    # Validate that the data is a list of JSON objects
if isinstance(json_data, list):
    # Insert each JSON object into the MongoDB collection
    length = len(json_data)
    index = 1
    for json_object in json_data:
        if isinstance(json_object, dict):
            collection.insert_one(json_object)
            print("Inserted chapter " + str(index) + "/" + str(length))
            index += 1
        else:
            print(f"Skipping non-JSON object: {json_object}")
else:
    print("The file does not contain a list of JSON objects.")

# Close the connection to MongoDB
client.close()
