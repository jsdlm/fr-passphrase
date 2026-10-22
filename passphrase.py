#!/usr/bin/env python3

import argparse
import math
import random
import re
import string
import sys
from collections.abc import Iterable
from pathlib import Path
from typing import TextIO

MIN_ENTROPY = 44
WORDLIST_PATH = Path(__file__).resolve().parent / "wordlist.txt"


def choose(words: "Wordlist", nb: int) -> list[str]:
    rng = random.SystemRandom()
    return [rng.choice(words) for _ in range(nb)]


def capitalize_random_word(words: list[str]) -> float:
    rng = random.SystemRandom()
    index = rng.randrange(len(words))
    words[index] = words[index].capitalize()
    return math.log(len(words), 2)


def insert_random_number(words: list[str], nb_digits: int) -> float:
    rng = random.SystemRandom()
    number = "".join(rng.choice(string.digits) for _ in range(nb_digits))
    nb_positions = len(words) + 1
    words.insert(rng.randrange(nb_positions), number)
    return nb_digits * math.log(10, 2) + math.log(nb_positions, 2)


class Wordlist:
    def __init__(self, words: Iterable[str]) -> None:
        self.words = list(words)
        self._len = len(self.words)
        self.entropy_per_word = math.log(self._len, 2)

    def __len__(self) -> int:
        return self._len

    def __getitem__(self, key: int) -> str:
        return self.words[key]


def wordlist_from_file(wordfile: TextIO) -> Wordlist:
    is_diceware = bool(re.fullmatch(r"[1-6]+\s[\w '-]+", wordfile.readline().strip()))
    wordfile.seek(0)

    if is_diceware:
        return Wordlist(word.strip().split(maxsplit=1)[1] for word in wordfile)

    return Wordlist(word.strip() for word in wordfile)


def print_passphrase(words: list[str], entropy: float, sep: str = "-", verbose: bool = False) -> None:
    passphrase = sep.join(words)

    entropy = min(len(passphrase) * math.log(26, 2), entropy)

    if entropy < MIN_ENTROPY:
        print(f"Warning: the passphrase entropy of {entropy:2.1f} bits seems very low.", file=sys.stderr)

    if verbose:
        print(f"Passphrase entropy: {entropy:2.1f}", file=sys.stderr)

    print(passphrase)


def rolldice(entropy: float, nb_words: int | None = None, uppercase: bool = False, nb_digits: int = 0) -> tuple[list[str], float]:
    with open(WORDLIST_PATH, encoding="utf-8") as wordfile:
        wordlist = wordlist_from_file(wordfile)

    if nb_words is None:
        nb_words = math.ceil(entropy / wordlist.entropy_per_word)

    words = choose(wordlist, nb_words)
    entropy = nb_words * wordlist.entropy_per_word

    if uppercase:
        entropy += capitalize_random_word(words)

    if nb_digits > 0:
        entropy += insert_random_number(words, nb_digits)

    return words, entropy


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-e", "--entropy", type=int, default=56)
    group.add_argument("nb_words", type=int, nargs="?", default=None)
    parser.add_argument("-s", "--separator", default="-")
    parser.add_argument("-u", "--uppercase", action="store_true")
    parser.add_argument("-d", "--digits", type=int, default=0)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if args.nb_words is not None and args.nb_words < 1:
        parser.error("nb_words must be at least 1")

    if args.digits < 0:
        parser.error("--digits cannot be negative")

    words, entropy = rolldice(args.entropy, args.nb_words, args.uppercase, args.digits)

    print_passphrase(words, entropy, args.separator, args.verbose)


if __name__ == "__main__":
    main()
