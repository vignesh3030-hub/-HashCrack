# 🔓 HashCrack

A modular, terminal-based password hash cracking tool written in Python. Built for **CTF challenges**, **security research**, and **authorized penetration testing**.

> ⚠️ **Legal Disclaimer**: Only use this tool on systems and hashes you own or have **explicit written permission** to test. Unauthorized use is illegal under laws including the CFAA (Computer Fraud and Abuse Act).

---

## Features

- 🔍 **Auto hash detection** (MD5, SHA1, SHA256, SHA512, and more)
- 📖 **Dictionary attack** — test against a wordlist
- 💪 **Brute force attack** — all combinations up to N length
- 🧬 **Hybrid attack** — dictionary + smart mutations (leet speak, suffixes, numbers)
- 📂 **Batch mode** — crack multiple hashes from a file
- 💾 **Output to file** — save results to disk
- 🎨 **Colored terminal UI** with progress feedback

---

## Installation

```bash
git clone https://github.com/youruser/hashcrack.git
cd hashcrack
pip install -r requirements.txt
chmod +x hashcrack.py
```

**Python 3.10+** is required (uses union type hints).

---

## Usage

### Basic syntax

```
python hashcrack.py [options]
```

### Options

| Flag | Description |
|------|-------------|
| `-H HASH` | Single hash to crack |
| `--file FILE` | File with one hash per line |
| `-a MODE` | Attack mode: `dict`, `brute`, `hybrid` |
| `-w FILE` | Wordlist path (required for dict/hybrid) |
| `-t TYPE` | Hash type: `md5`, `sha1`, `sha256`, etc. (default: auto) |
| `--charset` | Brute force charset: `alpha`, `alpha_num`, `all` |
| `--minlen` | Min length for brute force (default: 1) |
| `--maxlen` | Max length for brute force (default: 6) |
| `--identify` | Only identify the hash type |
| `-o FILE` | Save results to output file |
| `-q` | Quiet mode — only print results |

---

## Examples

### Dictionary attack
```bash
python hashcrack.py -H 5f4dcc3b5aa765d61d8327deb882cf99 -a dict -w wordlists/common.txt
```

### Brute force (alpha-numeric, up to 5 chars)
```bash
python hashcrack.py -H ab56b4d92b40713acc5af89985d4b786 -a brute --charset alpha_num --maxlen 5
```

### Hybrid attack (dictionary + mutations)
```bash
python hashcrack.py -H 5f4dcc3b5aa765d61d8327deb882cf99 -a hybrid -w wordlists/common.txt
```

### Crack multiple hashes from file
```bash
python hashcrack.py --file hashes.txt -a dict -w wordlists/rockyou.txt -o results.txt
```

### Identify hash type only
```bash
python hashcrack.py --identify 5f4dcc3b5aa765d61d8327deb882cf99
```

---

## Project Structure

```
hashcrack/
├── hashcrack.py          # CLI entry point
├── attacks/
│   ├── dictionary.py     # Dictionary attack
│   ├── brute_force.py    # Brute force attack
│   └── hybrid.py         # Hybrid attack (mutations)
├── utils/
│   ├── banner.py         # ASCII art banner
│   └── hash_id.py        # Hash type identification
├── wordlists/
│   └── common.txt        # Sample wordlist
├── requirements.txt
└── README.md
```

---

## Wordlists

The included `wordlists/common.txt` is a minimal starter list. For real-world testing, use:

- [RockYou](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt) (14M passwords)
- [SecLists](https://github.com/danielmiessler/SecLists/tree/master/Passwords)
- [weakpass.com](https://weakpass.com/wordlists) (various sizes)

---

## Supported Hash Types

| Hash | Length | Auto-detected |
|------|--------|---------------|
| MD5 | 32 | ✅ |
| SHA1 | 40 | ✅ |
| SHA224 | 56 | ✅ |
| SHA256 | 64 | ✅ |
| SHA384 | 96 | ✅ |
| SHA512 | 128 | ✅ |

---

## Contributing

Pull requests welcome. Please open an issue first to discuss major changes.

---

## License

MIT License — see [LICENSE](LICENSE) for details.
