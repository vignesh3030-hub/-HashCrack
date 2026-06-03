#!/usr/bin/env python3
"""
HashCrack - A Password Hash Cracking Tool
For educational purposes, CTFs, and authorized penetration testing only.
"""

import argparse
import sys
import time
from utils.banner import print_banner
from utils.hash_id import identify_hash
from attacks.dictionary import dictionary_attack
from attacks.brute_force import brute_force_attack
from attacks.hybrid import hybrid_attack


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

    parser.add_argument("-H", "--hash", metavar="HASH",
                        help="Single hash to crack")
    parser.add_argument("--file", "-f", metavar="FILE",
                        help="File containing one hash per line")
    parser.add_argument("-a", "--attack", choices=["dict", "brute", "hybrid"],
                        help="Attack mode: dict | brute | hybrid")
    parser.add_argument("-w", "--wordlist", metavar="FILE",
                        help="Path to wordlist file (for dict/hybrid attacks)")
    parser.add_argument("-t", "--type", metavar="TYPE", default="auto",
                        help="Hash type: md5, sha1, sha256, sha512 (default: auto-detect)")
    parser.add_argument("--charset", choices=["alpha", "alpha_num", "all"],
                        default="alpha_num",
                        help="Charset for brute force (default: alpha_num)")
    parser.add_argument("--minlen", type=int, default=1,
                        help="Min password length for brute force (default: 1)")
    parser.add_argument("--maxlen", type=int, default=6,
                        help="Max password length for brute force (default: 6)")
    parser.add_argument("--identify", metavar="HASH",
                        help="Identify the hash type only")
    parser.add_argument("--threads", type=int, default=4,
                        help="Number of threads (default: 4)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Quiet mode — only print results")
    parser.add_argument("-o", "--output", metavar="FILE",
                        help="Save results to file")

    return parser.parse_args()


def crack_single(hash_val, args):
    hash_type = args.type
    if hash_type == "auto":
        hash_type = identify_hash(hash_val)
        if not args.quiet:
            print(f"  [~] Auto-detected hash type: \033[93m{hash_type}\033[0m")

    start = time.time()

    if args.attack == "dict":
        if not args.wordlist:
            print("  [!] Dictionary attack requires --wordlist")
            return None, None
        result = dictionary_attack(hash_val, args.wordlist, hash_type, args.quiet)

    elif args.attack == "brute":
        result = brute_force_attack(
            hash_val, hash_type,
            charset=args.charset,
            min_len=args.minlen,
            max_len=args.maxlen,
            quiet=args.quiet
        )

    elif args.attack == "hybrid":
        if not args.wordlist:
            print("  [!] Hybrid attack requires --wordlist")
            return None, None
        result = hybrid_attack(hash_val, args.wordlist, hash_type, args.quiet)

    else:
        print("  [!] Please specify an attack mode with -a")
        return None, None

    elapsed = time.time() - start
    return result, elapsed


def main():
    args = parse_args()

    if not args.quiet:
        print_banner()

    # Identify-only mode
    if args.identify:
        ht = identify_hash(args.identify)
        print(f"\n  Hash  : {args.identify}")
        print(f"  Type  : \033[93m{ht}\033[0m\n")
        sys.exit(0)

    hashes = []
    if args.hash:
        hashes.append(args.hash.strip())
    elif args.file:
        try:
            with open(args.file) as f:
                hashes = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"[!] File not found: {args.file}")
            sys.exit(1)
    else:
        print("[!] Provide a hash with -H or a file with --file")
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
