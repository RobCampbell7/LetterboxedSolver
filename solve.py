"""Solve the NYT Letter Boxed puzzle (https://www.nytimes.com/puzzles/letter-boxed).

Run with no arguments to be prompted for the twelve letters, three to a side, and have the solutions
printed shortest first. See --help for the word list and output switches.
"""

import argparse

from letterBoxed import (BIG_WORD_FILE, LETTERS_PER_SIDE, PUZZLE_LETTERS, SIDE_COUNT, WORD_FILE,
                         findWords, recursiveSolve)

DEFAULT_LIMIT = 20

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-b", "--big", action="store_true",
                        help="use the larger, more obscure word list")
    parser.add_argument("-c", "--caps", action="store_true",
                        help="also allow capitalised words, such as proper nouns")
    parser.add_argument("-w", "--words", type=int, default=3, metavar="COUNT",
                        help="most words a solution may use (default: %(default)s)")
    parser.add_argument("-l", "--limit", type=int, default=DEFAULT_LIMIT, metavar="COUNT",
                        help="most solutions to print, 0 for all (default: %(default)s)")
    return parser.parse_args()

def readPuzzle():
    """Prompt for the four sides of the puzzle, returning them as a tuple of strings."""
    sides = []
    for number in range(1, SIDE_COUNT + 1):
        side = "".join(c for c in input("Side %d : " % number).upper() if c.isalpha())
        if len(side) != LETTERS_PER_SIDE:
            raise SystemExit("Each side has %d letters, side %d has %d."
                             % (LETTERS_PER_SIDE, number, len(side)))
        sides.append(side)

    letters = "".join(sides)
    if len(set(letters)) != PUZZLE_LETTERS:
        raise SystemExit("The %d letters must all be different." % PUZZLE_LETTERS)
    print()
    return tuple(sides)

def printSolutions(solutions, limit):
    if len(solutions) == 0:
        print("No solutions found. Try again with -b, or allow more words with -w.")
        return
    solutionCounts = [0, 0, 0, 0, 0, 0]
    for s in solutions:
        solutionCounts[len(s) - 1] += 1

    firstLine = "%d solutions found" % len(solutions)
    for i in range(len(solutionCounts)):
        if solutionCounts[i] != 0:
            firstLine += ", %d in %d words" % (solutionCounts[i],  i + 1)

    shown = solutions if limit == 0 else solutions[:limit]
    print(firstLine)
    for chain in shown:
        print(" - ".join(chain))
    if len(shown) < len(solutions):
        print("... and %d more" % (len(solutions) - len(shown)))

def main():
    args = parseArgs()
    wordFile = BIG_WORD_FILE if args.big else WORD_FILE
    # sides = readPuzzle()
    # print(sides)
    # sides = ('CBG', 'UAE', 'FLV', 'TDQ')
    sides = ('VTU', 'BWI', 'NAO', 'EHS')
    # sides = ('ERA', 'VLC', 'TIN', 'OSU')
    words = list(findWords(wordFile, sides, args.caps))
    printSolutions(recursiveSolve(words, sides, args.words), args.limit)

if __name__ == "__main__":
    main()
