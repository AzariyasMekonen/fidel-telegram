#!/usr/bin/env python3
import secrets

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
    assert 0 <= idx < 95, "only printable ASCII can be telegraphed"
    return idx % R, idx // R


def from_fidel(row, order):
    return chr(32 + order * R + row)


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


if __name__ == "__main__":
    flag = open("flag.txt").read().strip()
    message = (
        "TELEGRAM FROM RAS ALULA AT ADWA TO EMPEROR MENELIK II. "
        "THE ITALIAN COLUMNS UNDER BARATIERI MARCH BEFORE DAWN. "
        "OUR SCOUTS HAVE SEEN THEM AT THE PASS. "
        "KEEP THIS WORD SAFE: " + flag
    )
    a = secrets.randbelow(R - 1) + 1
    b = secrets.randbelow(R)
    key = [secrets.randbelow(ORDERS) for _ in range(secrets.randbelow(4) + 5)]
    with open("message.txt", "w", encoding="utf-8") as f:
        f.write(encrypt(message, a, b, key) + "\n")
