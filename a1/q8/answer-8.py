import itertools, re, pyperclip
import detectEnglish, vigenereCipher, frequencyAnalysis

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_KEY_LENGTH = 6 # Will not attempt keys longer than this.
NUM_MOST_FREQ_LETTERS = 4 # Attempt this many letters per subkey.
SILENT_MODE = False # If set to True, program doesn't print anything.
NONLETTERS_PATTERN = re.compile('[^A-Z]')



def main():
    ciphertext = ""
    hackedMessage = hackVigenere(ciphertext)

    if hackedMessage != None:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to hack encryption.')

