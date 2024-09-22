import itertools, re, pyperclip
import detectEnglish, vigenereCipher, frequencyAnalysis

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
MAX_KEY_LENGTH = 6 # Will not attempt keys longer than this.
NUM_MOST_FREQ_LETTERS = 10 # Attempt this many letters per subkey.
SILENT_MODE = False # If set to True, program doesn't print anything.
NONLETTERS_PATTERN = re.compile('[^A-Z]')



def main():
    # enter the ciphertext here
    ciphertext = "qivjukosqegnyiytxypshzewjsnsdpeybsuiranshzewjsnsdvusdvozqhasghexhvtdrynjyirlrrnfpekjbsuhucnjyirlrrnfveylrsdgbinjyirlrrnfwilqbsuqlisfqhhzuxytxaewhroxwvasjirxwsltyiytxontzxhjuyljvenivsdtlectpqiypinylwwmdxirosoplrgkrvytxaoswkeywlixivordrytwlewjyynmysyzensdxeqocozkswnpjejomnlzensdqaphcozxrdjuwtfqhnjyirlrrnfjmvjbsuzsreahvgtqraqhxytxhobq" 
    hackedMessage = hackVigenere(ciphertext)

    if hackedMessage != None:
        print('Copying hacked message to clipboard:')
        print(hackedMessage)
        pyperclip.copy(hackedMessage)
    else:
        print('Failed to hack encryption.')

# this goes through the msg to find ANY 3-5 repeated letter sequences
# returns: dictionary w the keys of the sequence and values of a list of spacings
def findRepeatSeq(message):
    message = NONLETTERS_PATTERN.sub('', message.upper()) # using regex to remove non-letter chars
    seqSpacings = {} # keys are sequences; values are lists of int spacings

    for seqLen in range(3,6):
        for seqStart in range(len(message) - seqLen):
            seq = message[seqStart:seqStart + seqLen] # find sequence and store in seq

            for i in range(seqStart + seqLen, len(message) - seqLen): # look for aforementioned seq in rest of msg
                if message[i:i + seqLen] == seq:
                    if seq not in seqSpacings:
                        seqSpacings[seq] = []
                        seqSpacings[seq].append(i - seqStart)
    return seqSpacings

def getFactors(num):
    # this explicitly excludes 1 bc it's not useful
    # returns: list of non-1 factors
    if num < 2:
        return []
    
    factors = []

    for i in range(2, MAX_KEY_LENGTH + 1): # no need to check beyond max key length
        if num % i == 0:
            factors.append(i)
            otherFactor = int(num / i)

            if otherFactor < MAX_KEY_LENGTH + 1 and otherFactor != 1:
                factors.append(otherFactor)
    return list(set(factors)) # to remove duplicate factors

def getItemAtIndexOne(items): # self-explanatory
    return items[1]

def getMCF(seqFactors):
    # MCF: Most Common Factor
    factorCounts = {} # key is a factor; value is how often it occurs

    # how many times does a seqeunce occur in seqFactors?
    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1
    
    # put factor &  its count into a tuple and make a list
    factorsByCount = []
    for factor in factorCounts:
        if factor <= MAX_KEY_LENGTH: # again, no need to check beyond max key length
            factorsByCount.append((factor, factorsByCount[factor]))
    
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True) # sort by factor count

    return factorsByCount

def kasiskiExam(cipherText):
    # find sequences b/w 3-5 letters that occur multiple times
    repeatedSeqSpacings = findRepeatSeq(cipherText)

    seqFactors = {}
    for seq in repeatedSeqSpacings:
        seqFactors[seq] = []
        for spacing in repeatedSeqSpacings[seq]:
            seqFactors[seq].extend(getFactors(spacing))
    
    factorsByCount = getFactors(seqFactors)

    likelyKeyLens = []
    for twoIntTuple in factorsByCount:
        likelyKeyLens.append(twoIntTuple[0])
    
    return likelyKeyLens

def getNthSubkeysLetters(nth, keyLen, message):
    # format:
    # getNthSubkeysLetters (1, 3, ABCDEFGHIJK) -> ADGJ
    # returns every nth letter for each keyLen set of letters in text
    message = NONLETTERS_PATTERN.sub('', message) # again, using regex to remove non-letter chars

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLen
    return ''.join(letters)

def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):
    # what is the most likely letters for each letter in the key?
    ciphertextUp = ciphertext.upper()

    allFreqScores = [] # list of mostLikelyKeyLength number of lists
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)

        freqScores = [] # list of tuples
        for possibleKey in ALPHABET:
            decryptedText = vigenereCipher.decryptMessage(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, frequencyAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)

        freqScores.sort(key=getItemAtIndexOne, reverse=True) # sort by match score -> higher is better match

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):

            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print()


    # try every combination of the most likely letters for each position in the key
    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):

        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0] # create a possible key from the letters in allFreqScores

        if not SILENT_MODE:
            print('Attempting with key: %s' % (possibleKey))

        decryptedText = vigenereCipher.decryptMessage(possibleKey, ciphertextUp)

        if detectEnglish.isEnglish(decryptedText):

            origCase = []
            for i in range(len(ciphertext)):
                if ciphertext[i].isupper():
                    origCase.append(decryptedText[i].upper())
                else:
                    origCase.append(decryptedText[i].lower())
            decryptedText = ''.join(origCase)

            print('Possible encryption hack with key %s:' % (possibleKey))
            print(decryptedText[:200])
            print()
            print('Enter D if done, anything else to continue hacking:') # check with user to see if the key has been found
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText

    return None

def hackVigenere(ciphertext):
    # kasiski examination
    allLikelyKeyLengths = kasiskiExam(ciphertext)
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Results of the Kasiski Examination say the most likely key lengths are: ' + keyLengthStr + '\n')
    hackedMessage = None
    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage != None:
            break

    # start brute-forcing through key lengths
    if hackedMessage == None:
        if not SILENT_MODE:
            print('Unable to hack message with likely key length(s). Brute forcing key length...')
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            # don't re-check key lengths already tried from Kasiski:
            if keyLength not in allLikelyKeyLengths:
                if not SILENT_MODE:
                    print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
                if hackedMessage != None:
                    break
    return hackedMessage

# If vigenereHacker.py is run (instead of imported as a module) call
# the main() function.
if __name__ == '__main__':
    main()