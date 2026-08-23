# Letterboxed Solver
This program solves the NYT Letter Boxed puzzle (https://www.nytimes.com/puzzles/letter-boxed).

Run `python solve.py` in this directory and you are prompted for the four sides of the puzzle, three
letters each. A word may use any of the twelve letters, but never two letters in a row from the same
side, and every word after the first has to start with the letter the previous word ended on. A
solution is a chain of words that between them use all twelve letters.

The solver looks for a one word solution first, then two, then three, and prints only the shortest
chain it finds: there is no point offering three words when two will do. Within a word count the
solutions are printed shortest first, counting total letters.

## Word lists
| List | Words | Source |
| --- | --- | --- |
| `words.txt` | 278,950 | [Collins Scrabble Words 2021][csw21], the tournament list |
| `megaWords.txt` | 525,462 | [SCOWL/aspell][scowl], every English spelling variant |

The Collins list holds no proper nouns, so it is stored entirely in lowercase. The SCOWL list covers
US, GB (both `-ise` and `-ize`), Canadian and Australian spellings with no diacritics, and keeps its
capitalised words, which is what the `-c` switch reaches.

Both lists are built by `buildWordList.py`, which downloads the raw sources into `./sources`
(ignored by git) and filters them down. Rebuild them at any time with:

```
python buildWordList.py
```

Only words of 3 letters or more made purely of ASCII letters are kept, since nothing else can be
traced on the puzzle. To change what is kept, edit `allow()` in `buildWordList.py` and rebuild.

## Switches
| Switch | Effect |
| --- | --- |
| `-b`, `--big` | Search `megaWords.txt`: about twice as many words, and far looser |
| `-c`, `--caps` | Also allow capitalised words, such as proper nouns. Needs `-b` |
| `-w`, `--words COUNT` | Most words a solution may use, default 3 |
| `-l`, `--limit COUNT` | Most solutions to print, 0 for all, default 20 |

Switches can be given in any order and combined:\
`python solve.py -b -c`\
`python solve.py -b -l 5`\
`python solve.py -w 2`

## Files
| File | Purpose |
| --- | --- |
| `solve.py` | Command line entry point: reads the puzzle and prints the solutions |
| `letterBoxed.py` | The solving itself: tracing words and chaining them together |
| `buildWordList.py` | Downloads the raw sources and filters them into the two lists |
| `words.txt` | Default word list |
| `megaWords.txt` | Larger word list used by `-b` |

`words.txt` is published under licence with Collins, an imprint of HarperCollins Publishers Limited.

[csw21]: https://github.com/scrabblewords/scrabblewords
[scowl]: https://github.com/nlile/dictionary-word-list
