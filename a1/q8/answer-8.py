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

def findRepeatSeq(message):
    message = NONLETTERS_PATTERN.sub('', message.upper())
    seqSpacings = {}

    for seqLen in range(3,6):
        for seqStart in range(len(message) - seqLen):
            seq = message[seqStart:seqStart + seqLen]

            for i in range(seqStart + seqLen, len(message) - seqLen):
                if message[i:i + seqLen] == seq:
                    if seq not in seqSpacings:
                        seqSpacings[seq] = []
                        seqSpacings[seq].append(i - seqStart)
    return seqSpacings

def getFactors(num):
    # this explicitly excludes 1 bc it's not useful
    if num < 2:
        return []
    
    factors = []

    for i in range(2, MAX_KEY_LENGTH + 1):
        if num % i == 0:
            factors.append(i)
            otherFactor = int(num / i)

            if otherFactor < MAX_KEY_LENGTH + 1 and otherFactor != 1:
                factors.append(otherFactor)
    return list(set(factors)) # to remove duplicate factors

def getItemAtIndexOne(items):
    return items[1]

def getMCF(seqFactors):
    factorCounts = {}

    for seq in seqFactors:
        factorList = seqFactors[seq]
        for factor in factorList:
            if factor not in factorCounts:
                factorCounts[factor] = 0
            factorCounts[factor] += 1
    
    factorsByCount = []
    for factor in factorCounts:
        if factor <= MAX_KEY_LENGTH:
            factorsByCount.append((factor, factorsByCount[factor]))
    
    factorsByCount.sort(key=getItemAtIndexOne, reverse=True)

    return factorsByCount

def kasiskiExam(cipherText):
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
    message = NONLETTERS_PATTERN.sub('', message)

    i = nth - 1
    letters = []
    while i < len(message):
        letters.append(message[i])
        i += keyLen
    return ''.join(letters)

def attemptHackWithKeyLength(ciphertext, mostLikelyKeyLength):

    ciphertextUp = ciphertext.upper()

    allFreqScores = []
    for nth in range(1, mostLikelyKeyLength + 1):
        nthLetters = getNthSubkeysLetters(nth, mostLikelyKeyLength, ciphertextUp)

        freqScores = []
        for possibleKey in ALPHABET:
            decryptedText = vigenereCipher.decryptMessage(possibleKey, nthLetters)
            keyAndFreqMatchTuple = (possibleKey, frequencyAnalysis.englishFreqMatchScore(decryptedText))
            freqScores.append(keyAndFreqMatchTuple)

        freqScores.sort(key=getItemAtIndexOne, reverse=True)

        allFreqScores.append(freqScores[:NUM_MOST_FREQ_LETTERS])

    if not SILENT_MODE:
        for i in range(len(allFreqScores)):

            print('Possible letters for letter %s of the key: ' % (i + 1), end='')
            for freqScore in allFreqScores[i]:
                print('%s ' % freqScore[0], end='')
            print()



    for indexes in itertools.product(range(NUM_MOST_FREQ_LETTERS), repeat=mostLikelyKeyLength):

        possibleKey = ''
        for i in range(mostLikelyKeyLength):
            possibleKey += allFreqScores[i][indexes[i]][0]

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
            print(decryptedText[:200]) # Only show first 200 characters.
            print()
            print('Enter D if done, anything else to continue hacking:')
            response = input('> ')

            if response.strip().upper().startswith('D'):
                return decryptedText

    return None

def hackVigenere(ciphertext):
    # First, we need to do Kasiski Examination to figure out what the
    # length of the ciphertext's encryption key is:
    allLikelyKeyLengths = kasiskiExamination(ciphertext)
    if not SILENT_MODE:
        keyLengthStr = ''
        for keyLength in allLikelyKeyLengths:
            keyLengthStr += '%s ' % (keyLength)
        print('Kasiski Examination results say the most likely key lengths are: ' + keyLengthStr + '\n')
    hackedMessage = None
    for keyLength in allLikelyKeyLengths:
        if not SILENT_MODE:
            print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
        hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
        if hackedMessage != None:
            break

    # If none of the key lengths we found using Kasiski Examination
    # worked, start brute-forcing through key lengths:
    if hackedMessage == None:
        if not SILENT_MODE:
            print('Unable to hack message with likely key length(s). Brute forcing key length...')
        for keyLength in range(1, MAX_KEY_LENGTH + 1):
            # Don't re-check key lengths already tried from Kasiski:
            if keyLength not in allLikelyKeyLengths:
                if not SILENT_MODE:
                    print('Attempting hack with key length %s (%s possible keys)...' % (keyLength, NUM_MOST_FREQ_LETTERS ** keyLength))
                hackedMessage = attemptHackWithKeyLength(ciphertext, keyLength)
                if hackedMessage != None:
                    break
    return hackedMessage