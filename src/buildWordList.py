"""Build the word lists the solver searches, from their upstream sources.

The default list comes from Collins Scrabble Words 2021, the tournament word list, which is close to
what the puzzle actually accepts. The big list comes from a SCOWL/aspell dump, which is roughly
twice the size and far looser.

Run this script to rebuild both lists; the raw sources are downloaded into ./sources the first time
and reused after that. Adjust the filters in allow() to change what makes it into the built lists.
"""

import os
import urllib.request

from letterBoxed import BIG_WORD_FILE, MIN_LENGTH, WORD_FILE, PUZZLE_LETTERS

CWD = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = os.path.join(os.path.dirname(CWD), "sources")

COLLINS_SOURCE = "CSW21.txt"
COLLINS_URL = ("https://raw.githubusercontent.com/scrabblewords/scrabblewords"
               "/main/words/British/CSW21.txt")
SCOWL_SOURCE = "scowl.txt"
SCOWL_URL = ("https://raw.githubusercontent.com/nlile/dictionary-word-list"
             "/master/largest_possible_aspell_wordlist_without_diacritic.txt")

def doubleLetter(s):
    """Return True if word contains a double letter"""
    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            return True
    return False

def uniqueCharLimit(word, limit=PUZZLE_LETTERS):
    letters = []
    for c in word:
        if c not in letters:
            letters.append(c)
    return len(letters) <= limit

def allow(word):
    """Return True if word is worth keeping in a built list.

    Anything shorter than the puzzle's minimum, or carrying a character that cannot be traced on the
    puzzle, is dead weight.
    If the word contains a double letter or is made up of more than 12 characters it can be removed.
    """
    return (
        len(word) >= MIN_LENGTH
        and word.isascii()
        and word.isalpha()
        and not doubleLetter(word)
        and uniqueCharLimit(word)
    )


def fetchSource(fileName, url):
    """Return the path to a raw source, downloading it if it is not here yet."""
    path = os.path.join(SOURCE_DIR, fileName)
    if not os.path.exists(path):
        if not os.path.isdir(SOURCE_DIR):
            os.mkdir(SOURCE_DIR)
        print("Downloading %s ..." % fileName)
        urllib.request.urlretrieve(url, path)
    return path


def readCollins(path):
    """Yield the words from a Collins list, dropping the attached definitions.

    Collins lists hold no proper nouns, so every word is lowercased.
    """
    with open(path, "r") as sourceFile:
        for line in sourceFile:
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue
            yield line.split(" ")[0].lower()


def readScowl(path):
    """Yield the words from a SCOWL dump, keeping each word's own case.

    Capitalisation is what marks a proper noun here, and the solver's -c switch depends on it, so it
    is left alone.
    """
    with open(path, "r") as sourceFile:
        for line in sourceFile:
            word = line.strip()
            if len(word) == 0 or word.startswith("---"):
                continue
            yield word


def build(sourceFileName, url, reader, targetPath):
    """Filter one raw source into a sorted, deduplicated word list."""
    sourcePath = fetchSource(sourceFileName, url)
    words = sorted({word for word in reader(sourcePath) if allow(word)},
                   key=lambda word: (word.lower(), word))

    with open(targetPath, "w") as targetFile:
        for word in words:
            targetFile.write(word + "\n")

    print("Wrote %d words to %s" % (len(words), os.path.basename(targetPath)))


def main():
    build(COLLINS_SOURCE, COLLINS_URL, readCollins, WORD_FILE)
    build(SCOWL_SOURCE, SCOWL_URL, readScowl, BIG_WORD_FILE)


if __name__ == "__main__":
    main()
