"""
Hash type identification based on length and character patterns.
"""


HASH_SIGNATURES = {
    32: "md5",
    40: "sha1",
    56: "sha224",
    64: "sha256",
    96: "sha384",
    128: "sha512",
}


def identify_hash(hash_val: str) -> str:
    """
    Attempt to identify hash type by length.
    Returns hash algorithm name string compatible with hashlib.
    """
    h = hash_val.strip().lower()

    # bcrypt
    if h.startswith("$2b$") or h.startswith("$2a$"):
        return "bcrypt"

    # MD5 crypt
    if h.startswith("$1$"):
        return "md5_crypt"

    # SHA-512 crypt
    if h.startswith("$6$"):
        return "sha512_crypt"

    length = len(h)
    return HASH_SIGNATURES.get(length, "md5")  # default fallback
