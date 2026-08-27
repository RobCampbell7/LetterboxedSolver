"""Solve the NYT Letter Boxed puzzle (https://www.nytimes.com/puzzles/letter-boxed).

Run with no arguments to be prompted for the twelve letters, three to a side, and have the solutions
printed shortest first. See --help for the word list and output switches.
"""

import argparse
import time

from letterBoxed import (BIG_WORD_FILE, LETTERS_PER_SIDE, PUZZLE_LETTERS, SIDE_COUNT, WORD_FILE,
                         findWords, recursiveSolve)

DEFAULT_PRINT_LIMIT = 20
DEFAULT_WORD_LIMIT = 3

def parseArgs():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("-b", "--big", action="store_true",
                        help="use the larger, more obscure word list")
    parser.add_argument("-c", "--caps", action="store_true",
                        help="also allow capitalised words, such as proper nouns")
    parser.add_argument("-np", "--no_pruning", action="store_true",
                        help="stop any pruning taking place in the recursion")
    parser.add_argument("-w", "--words", type=int, default=DEFAULT_WORD_LIMIT, metavar="COUNT",
                        help="most words a solution may use (default: %(default)s)")
    parser.add_argument("-e", "--exact", action="store_true",
                        help="only keep solutions using exactly the number of words given by -w")
    parser.add_argument("-l", "--limit", type=int, default=DEFAULT_PRINT_LIMIT, metavar="COUNT",
                        help="most solutions to print, 0 for all (default: %(default)s)")
    parser.add_argument("-t", "--time", action="store_true",
                        help="report how long the search itself took")
    parser.add_argument("-p", "--puzzle", nargs=SIDE_COUNT, metavar="SIDE",
                        help="the %d sides, %d letters each, instead of being prompted for them"
                             % (SIDE_COUNT, LETTERS_PER_SIDE))
    return parser.parse_args()

def checkPuzzle(sides):
    """Return the sides tidied and uppercased, refusing anything that is not a legal puzzle.

    Both ways of giving a puzzle, typed at the prompt or passed with -p, end up here, so they
    complain about the same things in the same words.
    """
    sides = tuple("".join(c for c in side.upper() if c.isalpha()) for side in sides)
    for number, side in enumerate(sides, 1):
        if len(side) != LETTERS_PER_SIDE:
            raise SystemExit("Each side has %d letters, side %d has %d."
                             % (LETTERS_PER_SIDE, number, len(side)))

    if len(set("".join(sides))) != PUZZLE_LETTERS:
        raise SystemExit("The %d letters must all be different." % PUZZLE_LETTERS)
    return sides

def readPuzzle():
    """Prompt for the four sides of the puzzle, returning them as a tuple of strings."""
    sides = [input("Side %d : " % number) for number in range(1, SIDE_COUNT + 1)]
    sides = checkPuzzle(sides)
    print()
    return sides

def printSolutions(solutions, limit, seconds=None):
    """Print the solutions, with a summary line first, and the search time when it was measured."""
    taken = "" if seconds is None else ", found in %.3f seconds" % seconds
    if len(solutions) == 0:
        print("No solutions found%s. Try again with -b, or allow more words with -w."
              % ("" if seconds is None else " in %.3f seconds" % seconds))
        return
    solutionCounts = [0, 0, 0, 0, 0, 0]
    for s in solutions:
        solutionCounts[len(s) - 1] += 1

    firstLine = "%d solutions found" % len(solutions)
    for i in range(len(solutionCounts)):
        if solutionCounts[i] != 0:
            firstLine += ", %d in %d words" % (solutionCounts[i],  i + 1)

    firstLine += taken

    shown = solutions if limit == 0 else solutions[:limit]
    print(firstLine)
    for chain in shown:
        print(" - ".join(chain))
    if len(shown) < len(solutions):
        print("... and %d more" % (len(solutions) - len(shown)))

def exactly(solutions, wordCount):
    """Return only the solutions using exactly wordCount words.

    The search collects everything up to its limit, so this drops the shorter chains afterwards.
    Note it can only keep what the search produced: a chain whose opening words already cover all
    twelve letters is recorded at that shorter length and never padded out, so it does not appear
    here under the longer count.
    """
    return [chain for chain in solutions if len(chain) == wordCount]


def main():
    args = parseArgs()
    wordFile = BIG_WORD_FILE if args.big else WORD_FILE
    sides = checkPuzzle(args.puzzle) if args.puzzle else readPuzzle()
    # print(sides)
    # sides = ('CBG', 'UAE', 'FLV', 'TDQ')
    # sides = ('VTU', 'BWI', 'NAO', 'EHS')
    # sides = ('ERA', 'VLC', 'TIN', 'OSU')
    words = list(findWords(wordFile, sides, args.caps))
    start = time.time()
    solutions = recursiveSolve(words, sides, args.words, not args.no_pruning)
    seconds = time.time() - start

    if args.exact:
        solutions = exactly(solutions, args.words)
    printSolutions(solutions, args.limit, seconds if args.time else None)

if __name__ == "__main__":
    main()
