# Fidel Telegram (easy, static)

**Concept:** a classical cipher written in Ge'ez script (fidel).

## Mechanics
- Each printable ASCII character maps to a cell of the fidel grid: `idx = ord(c) - 32`, `row = idx % 31`, `order = idx // 31`.
- The row is encrypted with an affine cipher mod 31: `row' = a*row + b`.
- The vowel order is encrypted with a repeating Vigenère key mod 7. The key is 5-8 entries long.
- The output is rendered as Unicode fidel (`ROWS[row'] + order'`).

## Intended solve
Players get only `message.txt` (no source). The flag body is uppercase, so everything except `{`, `}` and `_` uses the same symbols as the message body.
1. Split each fidel into consonant + vowel form.
2. Every crib letter in `TELEGRAM` (given in the description) has the same plaintext order, so its cipher orders give the order key directly. The key repeats after its length (5-8). Confirm the period on the body: the correct period leaves about 2 distinct orders per column.
3. Undo the order shift per column. Each (consonant, order) pair is now a fixed letter, so solve the rest as a monoalphabetic substitution, starting from the crib letters.
4. `_` is the only unseen consonant inside the flag and is obvious from context.

## Build
```bash
cd src && cp ../flag.txt . && python3 encrypt.py && rm flag.txt
mv message.txt ../dist/
python3 ../solve/solve.py ../dist/message.txt
```
