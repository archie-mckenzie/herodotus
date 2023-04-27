import subprocess

# Run first script
subprocess.run(['python3', 'create_data_jsons.py'])

# Run second script after first script finishes
subprocess.run(['python3', 'load_sentences_and_paragraphs.py'])

# Run third script after second script finishes
subprocess.run(['python3', 'load_greek_words.py'])
