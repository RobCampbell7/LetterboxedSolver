import letterBoxed
from time import time

if __name__=="__main__":
    puzzle = ('VTU', 'BWI', 'NAO', 'EHS')
    words = list(letterBoxed.findWords(letterBoxed.WORD_FILE, puzzle))

    start = time()
    letterBoxed.recursiveSolve(words, puzzle, 3, False)
    end = time()
    print("without pruning: " + str(end - start))

    start = time()
    letterBoxed.recursiveSolve(words, puzzle, 3, True)
    end = time()
    print("   with pruning: " + str(end - start))