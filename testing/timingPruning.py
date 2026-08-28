from time import time

from letterboxed import letterBoxed # type: ignore

if __name__=="__main__":
    puzzle = ('ABC', 'DEF', 'GHI', 'JKL')
    maxWords = 4
    words = list(letterBoxed.findWords(letterBoxed.WORD_FILE, puzzle))

    start = time()
    letterBoxed.recursiveSolve(words, puzzle, maxWords, False)
    end = time()
    print("without pruning: " + str(end - start))

    start = time()
    letterBoxed.recursiveSolve(words, puzzle, maxWords, True)
    end = time()
    print("   with pruning: " + str(end - start))