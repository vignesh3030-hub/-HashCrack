"""
Hybrid Attack Module
Applies common mutations to each word in a wordlist:
- Original, capitalized, uppercased
- Numeric suffixes (0–999)
- Leet-speak substitutions
- Common prefix/suffix patterns
"""

import hashlib


LEET_MAP = str.maketrans({
    "a": "@", "e": "3", "i": "1",
    "o": "0", "s": "$", "t": "7",
})

COMMON_SUFFIXES = ["!", "123", "1", "#", "2024", "2023", "@", "99", "1234"]
COMMON_PREFIXES = ["the", "my", "mr", "dr"]


def hash_word(word: str, hash_type: str) -> str:
    try:
        h = hashlib.new(hash_type)
        h.update(word.encode("utf-8", errors="ignore"))
        return h.hexdigest()
    except ValueError:
        return ""


def generate_mutations(word: str):
    base_variants = [
        word,
        word.upper(),
        word.capitalize(),
        word.lower(),
        word.swapcase(),
    ]

    leet = word.lower().translate(LEET_MAP)
    if leet != word.lower():
        base_variants.append(leet)
        base_variants.append(leet.capitalize())

    mutations = list(base_variants)

    # Numeric suffixes
    for v in list(base_variants):
        for n in range(100):
            mutations.append(v + str(n))
        for year in ["2020", "2021", "2022", "2023", "2024"]:
            mutations.append(v + year)

    # Common suffixes
    for v in list(base_variants):
        for suf in COMMON_SUFFIXES:
            mutations.append(v + suf)

    # Common prefixes
    for v in list(base_variants):
        for pre in COMMON_PREFIXES:
            mutations.append(pre + v)

    return mutations


def hybrid_attack(target_hash: str, wordlist_path: str, hash_type: str, quiet: bool = False) -> str | None:
    target = target_hash.strip().lower()
    word_count = 0
    tried = 0

    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            for line in f:
                word = line.rstrip("\n")
                word_count += 1

                for mutation in generate_mutations(word):
                    tried += 1
                    if hash_word(mutation, hash_type) == target:
                        if not quiet:
                            print()
                        return mutation

                if not quiet and word_count % 10000 == 0:
                    print(f"  [~] Words: {word_count:,} | Mutations tried: {tried:,}...", end="\r")

    except FileNotFoundError:
        print(f"  [!] Wordlist not found: {wordlist_path}")
        return None

    if not quiet:
        print(f"  [~] Words: {word_count:,} | Mutations tried: {tried:,}       ")
    return None
