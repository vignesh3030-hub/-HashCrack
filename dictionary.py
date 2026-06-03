"""
Dictionary Attack Module
Tries each word in a wordlist against the target hash.
"""

import hashlib


def hash_word(word: str, hash_type: str) -> str:
    try:
        h = hashlib.new(hash_type)
        h.update(word.encode("utf-8", errors="ignore"))
        return h.hexdigest()
    except ValueError:
        return ""


def dictionary_attack(target_hash: str, wordlist_path: str, hash_type: str, quiet: bool = False) -> str | None:
    target = target_hash.strip().lower()
    count = 0

    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            for line in f:
                word = line.rstrip("\n")
                count += 1

                if not quiet and count % 50000 == 0:
                    print(f"  [~] Tried {count:,} words...", end="\r")

                if hash_word(word, hash_type) == target:
                    if not quiet:
                        print()
                    return word

    except FileNotFoundError:
        print(f"  [!] Wordlist not found: {wordlist_path}")
        return None

    if not quiet:
        print(f"  [~] Tried {count:,} words total.        ")
    return None
