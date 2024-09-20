# The full list of letters ordered by frequency
ETAOIN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'

# Alphabet
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Returns count of how many times each letter appears in a message
def getLetterCount(msg):
    letterCount = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'I': 0, 'J': 0, 'K': 0, 'L': 0, 'M': 0, 'N': 0, 'O': 0, 'P': 0, 'Q': 0, 'R': 0, 'S': 0, 'T': 0, 'U': 0, 'V': 0, 'W': 0, 'X': 0, 'Y': 0, 'Z': 0}

    for letter in msg.upper():
        if letter in ALPHABET:
            letterCount[letter] += 1
    
    return letterCount

# Returns first item in a list
def getItemAtIndexZero(items):
    return items[0]

# Returns a string of letters arranged in order of occurence in msg
def getFrequencyOrder(msg):
    # Get dictionary of letter w/ frequency count:
    letterToFreq = getLetterCount(msg)

    # Make a dictionary of each frequency count to each letter(s) w that frequency:
    freqToLetter = {}
    for letter in ALPHABET:
        if letterToFreq[letter] not in freqToLetter:
            freqToLetter[letterToFreq[letter]] = [letter]
        else:
            freqToLetter[letterToFreq[letter]].append(letter)

    # Third, put each list of letters in reverse "ETAOIN" order, and then
    # convert it to a string:
    for freq in freqToLetter:
        freqToLetter[freq].sort(key=ETAOIN.find, reverse=True)
        freqToLetter[freq] = ''.join(freqToLetter[freq])

    # Fourth, convert the freqToLetter dictionary to a list of
    # tuple pairs (key, value), then sort them:
    freqPairs = list(freqToLetter.items())
    freqPairs.sort(key=getItemAtIndexZero, reverse=True)

    # Fifth, now that the letters are ordered by frequency, extract all
    # the letters for the final string:
    freqOrder = []
    for freqPair in freqPairs:
        freqOrder.append(freqPair[1])

    return ''.join(freqOrder)

def freqMatchScore(msg):
    freqOrder = getFrequencyOrder(message)

    matchScore = 0
    # How many matches ETAOIN:
    for commonLetter in ETAOIN[:6]:
        if commonLetter in freqOrder[:6]:
            matchScore += 1
    # How many matches for lowest freq letters:
    for uncommonLetter in ETAOIN[-6:]:
        if uncommonLetter in freqOrder[-6:]:
            matchScore += 1

    return matchScore