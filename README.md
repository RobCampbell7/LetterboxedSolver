# Letterboxed Solver
Solves the NYT Letter Boxed puzzle: https://www.nytimes.com/puzzles/letter-boxed

Twelve letters, three to a side of a square. You make words out of them, except you can't use two
letters from the same side one after the other, and every word has to start with the letter the
last one ended on. Use all twelve letters and you're done.

## Running it
```
pip install -e .
letterboxed -p ERA VLC TIN OSU
```

Leave off `-p` and it asks you for the four sides one at a time.

Don't remove the `-e` on the install. The word lists sit next to the code rather than inside the package
and the solver goes looking for them relative to its own file, so a plain `pip install .` dumps the
code in site-packages, leaves the lists behind, and then can't find them.

If you'd rather not install anything at all, `python src/solve.py` does the same job.. Although
running anything in `testing/` does need it installed properly only runs once it's installed.

It doesn't stop at the shortest answer. Ask for up to 3 words and you get the 2 word solutions as
well, grouped by word count and sorted shortest first inside each group. `-e` throws away anything
shorter than what you asked for, `-l` caps how many actually get printed.

## Switches
| Switch | Effect |
| --- | --- |
| `-p`, `--puzzle SIDES` | Give the four sides as arguments instead of being prompted |
| `-b`, `--big` | Search `megaWords.txt`: about twice as many words, and far looser |
| `-c`, `--caps` | Also allow capitalised words, such as proper nouns. Needs `-b` |
| `-np`, `--no_pruning` | Turn off the reachability pruning, for timing comparisons |
| `-w`, `--words COUNT` | Most words a solution may use, default 3 |
| `-e`, `--exact` | Keep only solutions using exactly `-w` words, not fewer |
| `-l`, `--limit COUNT` | Most solutions to print, 0 for all, default 20 |
| `-t`, `--time` | Report how long the search itself took, in seconds |

Order doesnt matter, even with arguments:\
`letterboxed -b -c`\
`letterboxed -b -l 5`\
`letterboxed -w 2`\
`letterboxed -p ERA VLC TIN OSU -t`

## Word lists
| List | Words | Source |
| --- | --- | --- |
| `words.txt` | 278,950 | [Collins Scrabble Words 2021][csw21], the tournament list |
| `megaWords.txt` | 525,462 | [SCOWL/aspell][scowl], every English spelling variant |

Collins has no proper nouns in it, so it's all lowercase. SCOWL covers US, GB (both `-ise` and
`-ize`), Canadian and Australian spellings, no accents, and it keeps its capitalised words, which
is the only reason `-c` has anything to do.

`src/buildWordList.py` builds both. It pulls the raw sources down into `./sources` (git ignores
that) and filters them:

```
python src/buildWordList.py
```

It keeps words of 3 or more letters made of plain ASCII, and don't include any words that consist
of more than 12 letters (thats a pretty small filter but still its something).

If you want to change anything the `allow()` method in `src\buildWordList.py` is the function to
change.
## What's where
| File | Purpose |
| --- | --- |
| `pyproject.toml` | Packaging, and the `letterboxed` command it installs |
| `src/solve.py` | The command line bit: reads the puzzle, prints the answers |
| `src/letterBoxed.py` | The actual solving, tracing words and chaining them up |
| `src/buildWordList.py` | Pulls the raw sources down and filters them into the two lists |
| `words.txt` | Default word list |
| `megaWords.txt` | The big one, used by `-b` |
| `testing/timingPruning.py` | Times a puzzle with pruning on and off |

`words.txt` is published under licence with Collins, an imprint of HarperCollins Publishers Limited.

[csw21]: https://github.com/scrabblewords/scrabblewords
[scowl]: https://github.com/nlile/dictionary-word-list
