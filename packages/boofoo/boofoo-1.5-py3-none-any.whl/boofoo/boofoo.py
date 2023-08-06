"""
Usage:
    boofoo.py --query=<query>
    boofoo.py --key=<key>
    boofoo.py --version

Options:
    --query "install mongodb on ubuntu"        Search query to perform.
    --version               Show version.
"""
import sys
import os
from docopt import docopt
import openai
import pyperclip
import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# cursor.execute('''CREATE TABLE config (id int, key text)''')

# cursor.execute("INSERT INTO config ('id','key') VALUES (1,'none')")

# Commit the changes
conn.commit()

# Query the table 
row = cursor.execute("SELECT * FROM config WHERE id = 1").fetchone()
current_key = row[1]
openai.api_key = current_key
print(current_key)
print(len(current_key))


GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
RESET = '\033[0m'

prompt = ''

def search(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = "IT questions only, Answer with command only "+prompt,
        max_tokens = 1000,
        n = 1,
        stop = None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

def keyInput(key):
    if len(key) < 40:
        print(RED+'Invalid ChatGPT API Key')

    new_key = input(GREEN+"Add your ChatGPT API Key --key ###############': "+RESET)
    if len(new_key) < 40:
        keyInput(new_key)
    else:
        cursor.execute("UPDATE config SET key = ? WHERE id = ?", (new_key, 1))
        openai.api_key = new_key

def main():
    args = docopt(__doc__, version='BooFoo 1.5')
    key = args['--key']
    query = args['--query']

    if len(current_key) < 40:
        new_key = input(GREEN+"Add your ChatGPT API Key --key ###############': "+RESET)
        keyInput(new_key)
    
    if query is not None:
        query = query
        # if len(query) < 2:
        #     print (RED+'Ask IT questions only')
        print(YELLOW+f'Searching for "{query}"...'+RESET)

        text = search(query)
        text = text.lstrip()
        text = text.replace("Run the following command in Terminal:", "")
        text = text.replace("Run the following command: ", "")
        print(GREEN +text+RESET)
        pyperclip.copy(text)

    else:
        print('No command specified. Use --help for usage instructions.')

# conn.close()
if __name__ == '__main__':
    main() 