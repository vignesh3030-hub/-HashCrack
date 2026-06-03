#!/usr/bin/env python3
"""
HashCrack - A Password Hash Cracking Tool
For educational purposes, CTFs, and authorized penetration testing only.
"""

import sys
import os
import hashlib
import argparse
import itertools
import string
import time

# ─────────────────────────────────────────
#  BANNER
# ─────────────────────────────────────────
def print_banner():
    print("\033[91m")
    print("  ██╗  ██╗ █████╗ ███████╗██╗  ██╗ ██████╗██████╗  █████╗  ██████╗██╗  ██╗")
    print("  ██║  ██║██╔══██╗██╔════╝██║  ██║██╔════╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝")
    print("  ███████║███████║███████╗███████║██║     ██████╔╝███████║██║     █████╔╝ ")
    print("  ██╔══██║██╔══██║╚════██║██╔══██║██║     ██╔══██╗██╔══██║██║     ██╔═██╗ ")
    print("  ██║  ██║██║  ██║███████║██║  ██║╚██████╗██║  ██║██║  ██║╚██████╗██║  ██╗")
    print("  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝")
    print("\033[0m")
    print("  \033[90mv1.0.0 | For authorized use only | github.com/vignesh3030-hub/-HashCrack\033[0m")
    print("  \033[93m  ⚠  Only use on systems you own or have explicit permission to test\033[0m\n")


# ─────────────────────────────────────────
#  HASH IDENTIFIER
# ─────────────────────────────────────────
HASH_LENGTHS = {32: "md5", 40: "sha1", 56: "sha224",
                64: "sha256", 96: "sha384", 128: "sha512"}

def identify_hash(hash_val):
    h = hash_val.strip().lower()
    if h.startswith(("$2b$", "$2a$", "$2y$")):
        return "bcrypt"
    if h.startswith("$1$"):
        return "md5_crypt"
    if h.startswith("$6$"):
        return "sha512_crypt"
    return HASH_LENGTHS.get(len(h), "md5")


# ─────────────────────────────────────────
#  HASH HELPER
# ─────────────────────────────────────────
def do_hash(word, algo):
    try:
        h = hashlib.new(algo)
        h.update(word.encode("utf-8", errors="ignore"))
        return h.hexdigest()
    except ValueError:
        return ""


# ─────────────────────────────────────────
#  DICTIONARY ATTACK
# ─────────────────────────────────────────
def dictionary_attack(target_hash, wordlist_path, hash_type, quiet=False):
    target = target_hash.strip().lower()
    count = 0
    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            for line in f:
                word = line.rstrip("\n")
                count += 1
                if not quiet and count % 50000 == 0:
                    print(f"  [~] Tried {count:,} words...", end="\r")
                if do_hash(word, hash_type) == target:
                    if not quiet:
                        print()
                    return word
    except FileNotFoundError:
        print(f"  [!] Wordlist not found: {wordlist_path}")
        return None
    if not quiet:
        print(f"  [~] Tried {count:,} words total.        ")
    return None


# ─────────────────────────────────────────
#  BRUTE FORCE ATTACK
# ─────────────────────────────────────────
CHARSETS = {
    "alpha":     string.ascii_lowercase,
    "alpha_num": string.ascii_lowercase + string.digits,
    "all":       string.ascii_letters + string.digits + string.punctuation,
}

def brute_force_attack(target_hash, hash_type, charset="alpha_num",
                       min_len=1, max_len=6, quiet=False):
    target = target_hash.strip().lower()
    chars  = CHARSETS.get(charset, CHARSETS["alpha_num"])
    total  = 0
    if not quiet:
        print(f"  [~] Charset: {charset}  |  Lengths: {min_len}-{max_len}")
    for length in range(min_len, max_len + 1):
        if not quiet:
            print(f"  [~] Trying length {length} ({len(chars)**length:,} combos)")
        for combo in itertools.product(chars, repeat=length):
            word = "".join(combo)
            total += 1
            if not quiet and total % 500000 == 0:
                print(f"  [~] Tried {total:,}...", end="\r")
            if do_hash(word, hash_type) == target:
                if not quiet:
                    print()
                return word
    if not quiet:
        print(f"\n  [~] Tried {total:,} total combinations.")
    return None


# ─────────────────────────────────────────
#  HYBRID ATTACK
# ─────────────────────────────────────────
LEET = str.maketrans({"a": "@", "e": "3", "i": "1",
                       "o": "0", "s": "$", "t": "7"})
SUFFIXES = ["!", "1", "123", "1234", "#", "@", "99", "2023", "2024", "2025"]

def mutations(word):
    bases = [word, word.lower(), word.upper(), word.capitalize(), word.swapcase()]
    leet = word.lower().translate(LEET)
    if leet != word.lower():
        bases += [leet, leet.capitalize()]
    for b in list(bases):
        yield b
        for n in range(100):
            yield b + str(n)
        for s in SUFFIXES:
            yield b + s

def hybrid_attack(target_hash, wordlist_path, hash_type, quiet=False):
    target = target_hash.strip().lower()
    words_seen = 0
    tried = 0
    try:
        with open(wordlist_path, "r", errors="ignore") as f:
            for line in f:
                word = line.rstrip("\n")
                words_seen += 1
                for m in mutations(word):
                    tried += 1
                    if do_hash(m, hash_type) == target:
                        if not quiet:
                            print()
                        return m
                if not quiet and words_seen % 10000 == 0:
                    print(f"  [~] Words: {words_seen:,}  Mutations: {tried:,}...", end="\r")
    except FileNotFoundError:
        print(f"  [!] Wordlist not found: {wordlist_path}")
        return None
    if not quiet:
        print(f"  [~] Words: {words_seen:,}  Mutations: {tried:,}       ")
    return None


# ─────────────────────────────────────────
#  ARG PARSER
# ─────────────────────────────────────────
def parse_args():
    parser = argparse.ArgumentParser(
        prog="hashcrack",
        description="HashCrack - Password Hash Cracking Tool",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python hashcrack.py -H 5f4dcc3b5aa765d61d8327deb882cf99 -a dict -w wordlists/common.txt
  python hashcrack.py -H 5f4dcc3b5aa765d61d8327deb882cf99 -a brute --charset alpha --maxlen 6
  python hashcrack.py -H 5f4dcc3b5aa765d61d8327deb882cf99 -a hybrid -w wordlists/common.txt
  python hashcrack.py --identify 5f4dcc3b5aa765d61d8327deb882cf99
  python hashcrack.py --file hashes.txt -a dict -w wordlists/common.txt
        """
    )
    parser.add_argument("-H", "--hash",     metavar="HASH", help="Single hash to crack")
    parser.add_argument("--file", "-f",     metavar="FILE", help="File with one hash per line")
    parser.add_argument("-a", "--attack",   choices=["dict", "brute", "hybrid"],
                        help="Attack mode: dict | brute | hybrid")
    parser.add_argument("-w", "--wordlist", metavar="FILE",
                        help="Wordlist path (required for dict/hybrid)")
    parser.add_argument("-t", "--type",     metavar="TYPE", default="auto",
                        help="Hash type: md5, sha1, sha256, sha512 (default: auto)")
    parser.add_argument("--charset",        choices=["alpha", "alpha_num", "all"],
                        default="alpha_num", help="Charset for brute force (default: alpha_num)")
    parser.add_argument("--minlen",         type=int, default=1,
                        help="Min length for brute force (default: 1)")
    parser.add_argument("--maxlen",         type=int, default=6,
                        help="Max length for brute force (default: 6)")
    parser.add_argument("--identify",       metavar="HASH", help="Identify hash type only")
    parser.add_argument("-o", "--output",   metavar="FILE", help="Save results to file")
    parser.add_argument("-q", "--quiet",    action="store_true", help="Only print results")
    return parser.parse_args()


# ─────────────────────────────────────────
#  CRACK ONE HASH
# ─────────────────────────────────────────
def crack_single(hash_val, args):
    hash_type = args.type
    if hash_type == "auto":
        hash_type = identify_hash(hash_val)
        if not args.quiet:
            print(f"  [~] Auto-detected: \033[93m{hash_type}\033[0m")
    start = time.time()
    if args.attack == "dict":
        if not args.wordlist:
            print("  [!] Dictionary attack requires -w / --wordlist")
            return None, None
        result = dictionary_attack(hash_val, args.wordlist, hash_type, args.quiet)
    elif args.attack == "brute":
        result = brute_force_attack(hash_val, hash_type,
                                    charset=args.charset,
                                    min_len=args.minlen,
                                    max_len=args.maxlen,
                                    quiet=args.quiet)
    elif args.attack == "hybrid":
        if not args.wordlist:
            print("  [!] Hybrid attack requires -w / --wordlist")
            return None, None
        result = hybrid_attack(hash_val, args.wordlist, hash_type, args.quiet)
    else:
        print("  [!] Specify an attack mode with -a  (dict | brute | hybrid)")
        return None, None
    return result, time.time() - start


# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    args = parse_args()
    if not args.quiet:
        print_banner()
    if args.identify:
        ht = identify_hash(args.identify)
        print(f"\n  Hash : {args.identify}")
        print(f"  Type : \033[93m{ht}\033[0m\n")
        sys.exit(0)
    hashes = []
    if args.hash:
        hashes.append(args.hash.strip())
    elif args.file:
        try:
            with open(args.file) as f:
                hashes = [l.strip() for l in f if l.strip()]
        except FileNotFoundError:
            print(f"  [!] File not found: {args.file}")
            sys.exit(1)
    else:
        print("  [!] Provide a hash with -H or a file with --file")
        sys.exit(1)
    results = []
    for h in hashes:
        if not args.quiet:
            print(f"\n  \033[96m[*]\033[0m Target : {h}")
        result, elapsed = crack_single(h, args)
        if result:
            print(f"  \033[92m[+]\033[0m CRACKED : \033[92m{result}\033[0m  (in {elapsed:.2f}s)")
            results.append((h, result))
        else:
            if elapsed is not None:
                print(f"  \033[91m[-]\033[0m NOT FOUND (in {elapsed:.2f}s)")
            results.append((h, None))
    if args.output:
        with open(args.output, "w") as f:
            for h, pw in results:
                f.write(f"{h}:{pw if pw else 'NOT_FOUND'}\n")
        print(f"\n  [>] Results saved to: {args.output}")
    cracked = sum(1 for _, pw in results if pw)
    if not args.quiet:
        print(f"\n  \033[96m[=]\033[0m Summary: {cracked}/{len(hashes)} hashes cracked\n")


if __name__ == "__main__":
    main()
