"""
Brute Force Attack Module
Tries all character combinations up to a given length.
Supports multithreading for speed.
"""

import hashlib
import itertools
import string
from concurrent.futures import ThreadPoolExecutor, as_completed


CHARSETS = {
    "alpha":     string.ascii_lowercase,
    "alpha_num": string.ascii_lowercase + string.digits,
    "all":       string.ascii_letters + string.digits + string.punctuation,
}


def hash_word(word: str, hash_type: str) -> str:
    try:
        h = hashlib.new(hash_type)
        h.update(word.encode("utf-8", errors="ignore"))
        return h.hexdigest()
    except ValueError:
        return ""


def _crack_chunk(candidates, target_hash, hash_type):
    for word in candidates:
        if hash_word(word, hash_type) == target_hash:
            return word
    return None


def brute_force_attack(
    target_hash: str,
    hash_type: str,
    charset: str = "alpha_num",
    min_len: int = 1,
    max_len: int = 6,
    quiet: bool = False,
) -> str | None:
    target = target_hash.strip().lower()
    chars = CHARSETS.get(charset, CHARSETS["alpha_num"])
    total_tried = 0
    CHUNK_SIZE = 100_000

    if not quiet:
        print(f"  [~] Charset: '{chars[:20]}{'...' if len(chars)>20 else ''}' | Lengths: {min_len}–{max_len}")

    for length in range(min_len, max_len + 1):
        if not quiet:
            total_combos = len(chars) ** length
            print(f"  [~] Length {length} — {total_combos:,} combinations")

        gen = itertools.product(chars, repeat=length)
        chunk = []

        for combo in gen:
            word = "".join(combo)
            chunk.append(word)
            total_tried += 1

            if len(chunk) >= CHUNK_SIZE:
                result = _crack_chunk(chunk, target, hash_type)
                if result:
                    return result
                chunk = []
                if not quiet:
                    print(f"  [~] Tried {total_tried:,}...", end="\r")

        if chunk:
            result = _crack_chunk(chunk, target, hash_type)
            if result:
                return result

    if not quiet:
        print(f"\n  [~] Tried {total_tried:,} total combinations.")
    return None
