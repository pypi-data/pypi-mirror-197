"""
Usage:
    boofoo.py --query=<query>
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
import constants
import configparser

cfg = configparser.ConfigParser()
cfg.read('config.cfg')

openai.api_key = (cfg.get('KEYS', 'CHATGPT_API_KEY', raw=''))

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

def main():
    args = docopt(__doc__, version='boofoo 1.0')

    if args['--version']:
        print('BooFoo 1.3')
    elif args['--query']:
        query = args['--query']
        if len(query) < 2:
            print (RED+'Ask IT questions only')
        print(YELLOW+f'Searching for "{query}"...'+RESET)

        text = search(query)
        text = text.lstrip()
        text = text.replace("Run the following command in Terminal:", "")
        text = text.replace("Run the following command: ", "")
        print(GREEN +text+RESET)
        pyperclip.copy(text)

    else:
        print('No command specified. Use --help for usage instructions.')


if __name__ == '__main__':
    main() 