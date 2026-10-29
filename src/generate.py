#!/usr/bin/env python3
"""
On-Demand Dynamic Challenge File Generator for Fidel Telegram (AdwaCTF).

Environment variables:
  - FLAG: Dynamic participant-specific flag (e.g. 'AdwaCTF{...}')
  - USER_ID: Optional participant or team identifier
  - OUTPUT_FILENAME: Output file name (default: 'message.txt')
  - OUTPUT_DIR: Target directory to write to (default: '/output')
"""

import os
import secrets
import sys

# Base consonants of the 31 complete fidel rows used by the Imperial Post.
ROWS = [
    0x1200, 0x1208, 0x1210, 0x1218, 0x1220, 0x1228, 0x1230, 0x1238,
    0x1240, 0x1260, 0x1268, 0x1270, 0x1278, 0x1280, 0x1290, 0x1298,
    0x12A0, 0x12A8, 0x12B8, 0x12C8, 0x12D0, 0x12D8, 0x12E0, 0x12E8,
    0x12F0, 0x1300, 0x1308, 0x1320, 0x1328, 0x1330, 0x1338,
]
R = len(ROWS)
ORDERS = 7


def to_fidel(ch):
    idx = ord(ch) - 32
    assert 0 <= idx < 95, f"character {ch!r} (ASCII {ord(ch)}) outside telegraphed range [32..126]"
    return idx % R, idx // R


def render(row, order):
    return chr(ROWS[row] + order)


def encrypt(text, a, b, key):
    out = []
    for i, ch in enumerate(text):
        row, order = to_fidel(ch)
        row = (a * row + b) % R
        order = (order + key[i % len(key)]) % ORDERS
        out.append(render(row, order))
    return "".join(out)


def get_flag():
    flag = os.environ.get("FLAG", "").strip()
    if flag:
        return flag

    # Fallback to local flag.txt if available
    for candidate in ["flag.txt", "/app/flag.txt", "../flag.txt"]:
        if os.path.isfile(candidate):
            try:
                with open(candidate, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        return content
            except OSError:
                pass

    return "AdwaCTF{FIDEL_ROWS_AND_ORDERS_CANT_HIDE_FROM_FREQUENCY}"


def main():
    flag = get_flag()
    user_id = os.environ.get("USER_ID", "anonymous").strip()
    output_dir = os.environ.get("OUTPUT_DIR", "/output")
    output_filename = os.environ.get("OUTPUT_FILENAME", "message.txt").strip()

    os.makedirs(output_dir, exist_ok=True)
    target_path = os.path.join(output_dir, output_filename)

    message = (
        "TELEGRAM FROM RAS ALULA AT ADWA TO EMPEROR MENELIK II. "
        "THE ITALIAN COLUMNS UNDER BARATIERI MARCH BEFORE DAWN. "
        "OUR SCOUTS HAVE SEEN THEM AT THE PASS. "
        "KEEP THIS WORD SAFE: " + flag
    )

    # Cryptographic parameter selection
    a = secrets.randbelow(R - 1) + 1  # 1 <= a < 31 (always coprime since 31 is prime)
    b = secrets.randbelow(R)
    # Key length between 5 and 8 (crib 'TELEGRAM' has length 8, ensuring solvability)
    key_len = secrets.randbelow(4) + 5
    key = [secrets.randbelow(ORDERS) for _ in range(key_len)]

    ciphertext = encrypt(message, a, b, key)

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(ciphertext + "\n")

    # Set world-readable permissions for extracted files
    try:
        os.chmod(target_path, 0o666)
    except OSError:
        pass

    print(f"[generator] user_id={user_id}")
    print(f"[generator] target={target_path}")
    print(f"[generator] generated {len(ciphertext)} fidel characters successfully.")


if __name__ == "__main__":
    main()
