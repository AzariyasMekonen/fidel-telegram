#!/usr/bin/env python3
"""Generate Fidel Telegram promotional video frames — v2 hacker terminal aesthetic."""
import os
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 30
random.seed(42)

# Colors
BG = (10, 10, 10)           # near-black
AMBER = (255, 176, 0)       # primary
CRIMSON = (178, 34, 34)     # flag/alert
DIM_AMBER = (80, 60, 10)    # dim text
GRID = (20, 20, 20)         # grid lines
TERRACOTTA = (181, 93, 59)  # fidel accent

FONT_MONO = "/usr/share/fonts/liberation-mono-fonts/LiberationMono-Regular.ttf"
FONT_MONO_B = "/usr/share/fonts/liberation-mono-fonts/LiberationMono-Bold.ttf"
FONT_ETHIOPIC = "/usr/share/fonts/google-noto-vf/NotoSansEthiopic[wght].ttf"

def load_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def ease_out(t):
    return 1 - (1 - t) ** 3

def draw_grid(d):
    """Subtle terminal grid."""
    step = 60
    for x in range(0, W, step):
        d.line([(x, 0), (x, H)], fill=GRID, width=1)
    for y in range(0, H, step):
        d.line([(0, y), (W, y)], fill=GRID, width=1)

def draw_scanlines(d, alpha=40):
    """Horizontal scanline overlay."""
    for y in range(0, H, 4):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, alpha), width=1)

def draw_cursor(d, x, y, blink=True, size=28):
    """Blinking terminal cursor."""
    if blink:
        d.rectangle([x, y, x + 6, y + size], fill=AMBER)

def glitch(d, text, font, x, y, color, intensity=0.1):
    """Render text with glitch offset copies."""
    d.text((x, y), text, font=font, fill=color)
    if intensity > 0:
        for _ in range(int(intensity * 8)):
            ox = random.randint(-3, 3)
            oy = random.randint(-2, 2)
            d.text((x + ox, y + oy), text, font=font, fill=CRIMSON)

def make_frame(t, scene, progress):
    """t = seconds from start, scene = current scene name, progress = 0-1 within scene"""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    draw_grid(d)

    if scene == "boot":
        mono_b = load_font(FONT_MONO_B, 36)
        mono = load_font(FONT_MONO, 26)
        
        # Boot title
        title = "ADWA-CTF TERMINAL v1.0"
        alpha = int(255 * ease_out(progress))
        tw = d.textlength(title, font=mono_b)
        d.text(((W - tw) / 2, H // 2 - 100), title, font=mono_b, fill=AMBER)
        
        # Loading lines
        lines = [
            "[OK]  initializing kernel...",
            "[OK]  loading fidel cipher module...",
            "[OK]  mounting geoez script...",
            "[OK]  establishing secure link...",
        ]
        for i, line in enumerate(lines):
            la = int(255 * ease_out(max(0, progress - i * 0.15) / 0.85))
            lw = d.textlength(line, font=mono)
            d.text(((W - lw) / 2, H // 2 + i * 40), line, font=mono, fill=(*DIM_AMBER, la))
        
        # Cursor
        draw_cursor(d, W // 2 + d.textlength(lines[-1], font=mono) + 10, H // 2 + 3 * 40, blink=(int(t * 4) % 2 == 0))

    elif scene == "hook":
        # Fidel rain effect
        fidel_chars = "ጃዛጤዝሬቫዣዌሼኄቫማዌሼቬዣሓሻዥጤካጣዤሼዤጃሺዤጵሌዣሺጄምሻዛዋጌዝቬማቫሻውዜታዛጤዕሤሺዓዔዌሻጃጫዜሼዔጃዣጤዕዤታሺሴምጤካዋቴሕሻካታጴዝቬሺናዤቭዤጃዓዜቭዔሺዋዤቭሴጫሺኔዝኄማቫዜሼጴዣላቴዌሻማካቬሼሔሳማኬጅሔሺጫዤብዜሺሓዜዝቴሺጃጬዝዌሺዣጄሼጄጫዛሻግዤሓሓዋሼሤዛዛጌሼጄጫዓሔሼሌማቫጴሼሔዣኃዜኤሻዣዜድኖሴጃኃይኅዔጳዛጤጾቬማላሔጾዤታጳጽምቬጳዛቬሕጽሳዣቴጅጽጫዓጴዝጽኃቫሜውጽኃቫዜኽኬዛታሴእሾ"
        
        f_font = load_font(FONT_ETHIOPIC, 64)
        
        # Rain: characters fall down
        for i in range(40):
            y_pos = int((t * 100 + i * 80) % (H + 200)) - 100
            if -60 < y_pos < H:
                ch = random.choice(fidel_chars)
                bx = d.textbbox((0, 0), ch, font=f_font)
                x = (i * 47) % W
                alpha = int(200 * (1 - abs(y_pos - H/2) / (H/2)))
                alpha = max(0, min(255, alpha))
                ch_img = Image.new("RGBA", (bx[2]-bx[0]+10, bx[3]-bx[1]+10), (0,0,0,0))
                cd = ImageDraw.Draw(ch_img)
                cd.text((5-bx[0], 5-bx[1]), ch, font=f_font, fill=(*TERRACOTTA, alpha))
                img.paste(ch_img, (int(x), int(y_pos)), ch_img)
        
        # Alert text
        alert_font = load_font(FONT_MONO_B, 40)
        alert = "UNKNOWN CIPHER DETECTED"
        alpha = int(255 * ease_out(max(0, progress - 0.3) / 0.7))
        tw = d.textlength(alert, font=alert_font)
        glitch(d, alert, alert_font, (W - tw) / 2, H // 2 + 60, AMBER, intensity=0.3 if alpha > 200 else 0)

    elif scene == "reveal":
        flag = "AdwaCTF{FIDEL_ROWS_AND_ORDERS_CANT_HIDE_FROM_FREQUENCY}"
        flag_font = load_font(FONT_MONO_B, 44)
        
        # Title
        title_font = load_font(FONT_MONO_B, 32)
        title = "DECRYPTING..."
        tw = d.textlength(title, font=title_font)
        alpha = int(255 * ease_out(progress))
        d.text(((W - tw) / 2, H // 2 - 140), title, font=title_font, fill=AMBER)
        
        # Typewriter effect: reveal flag char by char
        reveal_chars = int(len(flag) * progress)
        revealed = flag[:reveal_chars]
        if revealed:
            fw = d.textlength(revealed, font=flag_font)
            d.text(((W - fw) / 2, H // 2 - 40), revealed, font=flag_font, fill=CRIMSON)
        
        # Cursor
        if reveal_chars < len(flag):
            cx = (W - d.textlength(revealed, font=flag_font)) / 2 + d.textlength(revealed, font=flag_font)
            draw_cursor(d, cx, H // 2 - 40, blink=(int(t * 6) % 2 == 0))

    elif scene == "crib":
        mono_b = load_font(FONT_MONO_B, 34)
        mono = load_font(FONT_MONO, 28)
        
        title_font = load_font(FONT_MONO_B, 32)
        title = "KNOWN-PLAINTEXT ATTACK"
        tw = d.textlength(title, font=title_font)
        alpha = int(255 * ease_out(progress))
        d.text(((W - tw) / 2, 200), title, font=title_font, fill=AMBER)
        
        lines = [
            "Crib:  TELEGRAM",
            "Every imperial telegram starts with TELEGRAM",
            "Cipher orders at positions 0-7 reveal the Vigenère key",
            "Key length: 6  |  Period confirmed",
        ]
        for i, line in enumerate(lines):
            is_crib = (i == 0)
            f = mono_b if is_crib else mono
            c = CRIMSON if is_crib else AMBER
            la = int(255 * ease_out(max(0, progress - i * 0.1) / 0.9))
            lw = d.textlength(line, font=f)
            d.text(((W - lw) / 2, H // 2 - 60 + i * 50), line, font=f, fill=(*c, la))
        
        # Key display
        key_font = load_font(FONT_MONO_B, 40)
        key = "KEY: [3, 1, 4, 1, 5, 9]"
        kw = d.textlength(key, font=key_font)
        ka = int(255 * ease_out(max(0, progress - 0.4) / 0.6))
        d.text(((W - kw) / 2, H // 2 + 180), key, font=key_font, fill=(*CRIMSON, ka))

    elif scene == "solve":
        mono = load_font(FONT_MONO, 26)
        mono_b = load_font(FONT_MONO_B, 34)
        
        # Terminal output
        lines = [
            "$ python3 solve/solve.py dist/message.txt",
            "",
            "TELEGRAM FROM RAS ALULA AT ADWA TO EMPEROR MENELIK II.",
            "THE ITALIAN COLUMNS UNDER BARATIERI MARCH BEFORE DAWN.",
            "OUR SCOUTS HAVE SEEN THEM AT THE PASS.",
            "KEEP THIS WORD SAFE:",
            "",
        ]
        y_start = H // 2 - len(lines) * 22
        for i, line in enumerate(lines):
            pa = int(255 * ease_out(max(0, progress - i * 0.05) / 0.95))
            c = CRIMSON if "AdwaCTF" in line else AMBER
            d.text((W // 2 - 500, y_start + i * 30), line, font=mono, fill=(*c, pa))
        
        # Big flag reveal
        flag_font = load_font(FONT_MONO_B, 48)
        flag = "AdwaCTF{FIDEL_ROWS_AND_ORDERS_CANT_HIDE_FROM_FREQUENCY}"
        fw = d.textlength(flag, font=flag_font)
        fa = int(255 * ease_out(max(0, progress - 0.5) / 0.5))
        d.text(((W - fw) / 2, H // 2 + 200), flag, font=flag_font, fill=(*CRIMSON, fa))
        
        # FLAG CAPTURED
        cap_font = load_font(FONT_MONO_B, 40)
        cap = "FLAG CAPTURED"
        cw = d.textlength(cap, font=cap_font)
        ca = int(255 * ease_out(max(0, progress - 0.7) / 0.3))
        d.text(((W - cw) / 2, H // 2 + 300), cap, font=cap_font, fill=(*AMBER, ca))

    elif scene == "outro":
        title_font = load_font(FONT_MONO_B, 56)
        title = "ADWACTF"
        tw = d.textlength(title, font=title_font)
        alpha = int(255 * ease_out(progress))
        d.text(((W - tw) / 2, H // 2 - 40), title, font=title_font, fill=AMBER)
        
        sub_font = load_font(FONT_MONO, 32)
        sub = "Fidel Telegram  ·  Crypto  ·  100 pts"
        sw = d.textlength(sub, font=sub_font)
        d.text(((W - sw) / 2, H // 2 + 40), sub, font=sub_font, fill=(*DIM_AMBER, alpha))
        
        sub2 = "Break the cipher. Claim the flag."
        sw2 = d.textlength(sub2, font=sub_font)
        d.text(((W - sw2) / 2, H // 2 + 90), sub2, font=sub_font, fill=(*CRIMSON, alpha))

    # Scanlines overlay
    draw_scanlines(d)
    
    return img

def main():
    outdir = "/home/codeknight/Documents/work/AdwaCTF/challenges/crypto/01-fidel-telegram/brag-output/work/frames"
    os.makedirs(outdir, exist_ok=True)

    scenes = [
        ("boot", 3.0),
        ("hook", 3.0),
        ("reveal", 4.0),
        ("crib", 4.0),
        ("solve", 4.0),
        ("outro", 2.0),
    ]

    frame_idx = 0

    for scene_name, duration in scenes:
        scene_frames = int(duration * FPS)
        for i in range(scene_frames):
            t = frame_idx / FPS
            progress = i / scene_frames
            img = make_frame(t, scene_name, progress)
            img.save(f"{outdir}/frame_{frame_idx:04d}.png")
            frame_idx += 1

    print(f"Generated {frame_idx} frames")

if __name__ == "__main__":
    main()