#!/usr/bin/env python3
import sys

ROWS = [
    0x1200, 0x1208, 0x1210, 0x1218, 0x1220, 0x1228, 0x1230, 0x1238,
    0x1240, 0x1260, 0x1268, 0x1270, 0x1278, 0x1280, 0x1290, 0x1298,
    0x12A0, 0x12A8, 0x12B8, 0x12C8, 0x12D0, 0x12D8, 0x12E0, 0x12E8,
    0x12F0, 0x1300, 0x1308, 0x1320, 0x1328, 0x1330, 0x1338,
]
R, ORDERS = len(ROWS), 7
CRIB = "TELEGRAM"


def parse(ch):
    cp = ord(ch)
    for row, base in enumerate(ROWS):
        if base <= cp < base + ORDERS:
            return row, cp - base
    raise ValueError(f"unknown fidel {ch!r}")


def plain(ch):
    idx = ord(ch) - 32
    return idx % R, idx // R


def solve(ct):
    cells = [parse(c) for c in ct]
    for a in range(1, R):
        a_inv = pow(a, -1, R)
        for b in range(R):
            rows = [a_inv * (r - b) % R for r, _ in cells]
            if any(rows[i] != plain(CRIB[i])[0] for i in range(len(CRIB))):
                continue
            for klen in range(1, len(CRIB) + 1):
                key = [(cells[i][1] - plain(CRIB[i])[1]) % ORDERS for i in range(klen)]
                orders = [(o - key[i % klen]) % ORDERS for i, (_, o) in enumerate(cells)]
                idxs = [o * R + r for r, o in zip(rows, orders)]
                if all(i < 95 for i in idxs):
                    text = "".join(chr(32 + i) for i in idxs)
                    if text.startswith(CRIB) and "AdwaCTF{" in text:
                        return text
    return None


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "message.txt"
    text = solve(open(path, encoding="utf-8").read().strip())
    print(text)
    print(text[text.index("AdwaCTF{"):text.index("}") + 1])
