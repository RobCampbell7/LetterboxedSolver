"""Core solving for the NYT Letter Boxed puzzle (https://www.nytimes.com/puzzles/letter-boxed).

The puzzle is a square with three letters on each of its four sides. A word may use any of them,
but never two letters in a row from the same side, and every word after the first has to start with
the letter the previous word ended on. A solution is a chain of words that between them use all
twelve letters.
"""

import os

MIN_LENGTH = 3
SIDE_COUNT = 4
LETTERS_PER_SIDE = 3
PUZZLE_LETTERS = SIDE_COUNT * LETTERS_PER_SIDE

BITMASK_TARGET = 2 ** PUZZLE_LETTERS - 1

CWD = os.path.dirname(os.path.abspath(__file__))
WORD_FILE = os.path.join(CWD, "words.txt")
BIG_WORD_FILE = os.path.join(CWD, "megaWords.txt")


def findInRow(sides, char):
    """Return the indexes of the sides char sits on."""
    positions = []
    for index in range(len(sides)):
        if char.upper() in sides[index]:
            positions.append(index)
    return positions

def possible(word, sides):
    """Return True if word can be traced on the puzzle."""
    lastPos = [-1]
    for i in range(len(word)):
        pos = findInRow(sides, word[i])
        if pos == []:
            return False
        elif len(lastPos) < 2 and len(pos) < 2 and pos[0] == lastPos[0]:
            return False
        lastPos = pos

    return True

def usedLetters(word):
    """Return how many distinct letters a word uses."""
    foundLetters = []
    for char in word.lower():
        if char not in foundLetters:
            foundLetters.append(char)
    return len(foundLetters)

def findWords(wordFile, sides, includeCaps=False):
    """Yield every word in wordFile that can be traced on the puzzle.

    Words that are capitalised in the word list are proper nouns or abbreviations, which the puzzle
    does not accept, so they are skipped unless includeCaps is set.
    """
    with open(wordFile, "r") as dictFile:
        for line in dictFile:
            word = line.strip()
            if not word.isalpha():
                continue
            if not (includeCaps or word.islower()):
                continue
            if len(word) < MIN_LENGTH:
                continue
            if possible(word, sides):
                yield word

def flatten(twoDList):
    """Flattens a 2-d list into 1-D"""
    def flattenHidden(twoDList):
        for row in twoDList:
            for item in row:
                yield item
    return [*flattenHidden(twoDList)]

def decToInt(n, bits=8):
    res = ""
    while n > 0:
        res = str(n & 1) + res
        n >>= 1
    if len(res) < bits:
        res = (bits - len(res)) * "0" + res
    return res

def convert(word, index, flatSides):
    """Returns a tuple of four integers represnting that word in the new representation

    A word can be characterised as only its starting letter, ending letter, the letters it
    covers and the index of the word in the orignal word list. We can use a 12-bit integer to
    represent the covered letters and a number between 0 and 11 to represent the starting and
    ending letters.
    I'm not 100% sure this representation is internally consistent, but all starts and ends should
    agree and then all bitmasks will agree so not sure it really needs changing.
    """
    start = flatSides.index(word[0])
    end = flatSides.index(word[-1])
    bitmask = 0
    for i in range(PUZZLE_LETTERS):
        if flatSides[i] in word:
            bitmask += 2**(PUZZLE_LETTERS - i - 1)

    return (start, end, index, bitmask)

def solve(words, sides, maxWords=3):
    """Return the solutions found, as a list of tuples of words.

    One word solutions are looked for first, then two, then three, and the search stops at the first
    count that finds anything. Within a count the solutions come back shortest first, counting total
    letters.
    """
    solutions = [(word,) for word in words if usedLetters(word) == PUZZLE_LETTERS]

    flatSides = flatten(sides)
    convertedWords = [convert(words[i].upper(), i, flatSides) for i in range(len(words))]

    initLtrBuckets = [[] for i in range(PUZZLE_LETTERS)]
    for word in convertedWords:
        initLtrBuckets[word[0]].append(word)
    if len(solutions) == 0 and maxWords >= 2:
        for word1 in convertedWords:
            for word2 in initLtrBuckets[word1[1]]:
                if word1[3] | word2[3] == BITMASK_TARGET:
                    solutions.append((words[word1[2]], words[word2[2]]))

    # if len(solutions) == 0 and maxWords >= 2:
    #     for i in range(len(words)):
    #         for j in range(len(words)):
    #             if i != j:
    #                 if (words[i][-1] == words[j][0]
    #                         and usedLetters(words[i] + words[j]) == PUZZLE_LETTERS):
    #                     solutions.append((words[i], words[j]))

    # if len(solutions) == 0 and maxWords >= 3:
    #     for i in range(len(words)):
    #         for j in range(len(words)):
    #             for k in range(len(words)):
    #                 if k != i and k != j and i != j:
    #                     if words[i][-1] == words[j][0] and words[j][-1] == words[k][0]:
    #                         joined = words[i] + words[j] + words[k]
    #                         if usedLetters(joined) == PUZZLE_LETTERS:
    #                             solutions.append((words[i], words[j], words[k]))

    solutions.sort(key=lambda chain: sum(len(word) for word in chain))
    return solutions