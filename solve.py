import sys


ROWS = ("SKU", "HNU", "AJI", "YCE")


def findInRow(char):
    positions = []
    for i in range(4):
        if char.upper() in ROWS[i]:
            positions.append(i)
    return positions

def possible(word):
    lastPos = [-1]
    for i in range(len(word)):
        pos = findInRow(word[i])
        # print("char: " + word[i] + " | lastPos: " + str(lastPos) + " | pos: " + str(pos))
        if pos == []:
            return False
        elif len(lastPos) < 2 and len(pos) < 2 and pos[0] == lastPos[0]:
            return False
        lastPos = pos

    return True

def usedLetters(word):
    foundLetters = []
    for char in word.lower():
        if char not in foundLetters:
            foundLetters.append(char)
    return len(foundLetters)

includeCaps = False
if len(sys.argv) == 1:
    wordFile = "words.txt"
elif len(sys.argv) == 2:
    if sys.argv[1] == "-B":
        wordFile = "megaWords.txt"
    elif sys.argv[1] == "-C":
        includeCaps = True
    else:
        raise Exception("Invalid argument: '" + sys.argv[1] + "'")
elif len(sys.argv) == 3:
    args = sorted([a.upper() for a in sys.argv[1:]])
    if args[0] == "-B":
        wordFile = "megaWords.txt"
    else:
        raise Exception("Invalid argument: '" + sys.argv[1] + "'")
    if args[1] == "-C":
        wordFile = "megaWords.txt"
    else:
        raise Exception("Invalid argument: '" + sys.argv[2] + "'")
else:
    raise Exception("Too many arguments/s: '" + " ".join(sys.argv[1:]) + "'")

rows = []
for i in range(4):
    row = input(str(i+1) + ": ").replace(" ", "").replace(",", "").upper()
    rows.append(row)
ROWS = tuple(rows)

singleWord = False
doubleWord = False

extraWords = ["nitpicky", "whataboutism"]
possibleWords = []
with open(wordFile, "r") as dictFile:
    for word in extraWords:
        word = word.replace("\n", "").replace(" ", "")
        if possible(word) == True and (includeCaps or word == word.lower()):
            if usedLetters(word) == 12:
                singleWord = True
                print(word)
            possibleWords.append(word)

    for word in dictFile.readlines():
        word = word.replace("\n", "").replace(" ", "")
        if possible(word) == True and (includeCaps or word == word.lower()):
            if usedLetters(word) == 12:
                singleWord = True
                print(word)
            possibleWords.append(word)

if singleWord == False:
    possibleWords.sort(key = usedLetters)
    combinations = []
    for i in range(len(possibleWords)):
        for j in range(len(possibleWords)):
            if i != j:
                if possibleWords[i][-1] == possibleWords[j][0] and usedLetters(possibleWords[i] + possibleWords[j]) == 12:
                    combinations.append((possibleWords[i], possibleWords[j]))

    combinations.sort(key=lambda c : sum(len(w) for w in c))
    if combinations != []:
        doubleWord = True
        for comb in combinations:
            print("{0} - {1}".format(*comb))

if singleWord == False and doubleWord == False:
    possibleWords.sort(key = usedLetters)
    combinations = []
    for i in range(len(possibleWords)):
        for j in range(len(possibleWords)):
            for k in range(len(possibleWords)):
                if k != i and k != j and i != j:
                    if possibleWords[i][-1] == possibleWords[j][0] and possibleWords[j][-1] == possibleWords[k][0]:
                        count = usedLetters(possibleWords[i] + possibleWords[j] + possibleWords[k])
                        if count == 12:
                            combinations.append((possibleWords[i], possibleWords[j], possibleWords[k]))

    combinations.sort(key=lambda c : sum(len(w) for w in c))
    if combinations != []:
        doubleWord = True
        for comb in combinations:
            print("{0} - {1} - {2}".format(*comb))