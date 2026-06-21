#!/usr/bin/env python3
"""
Re-color the persian-cat-care page from cream/pink palette to Richard's
grey + copper palette. Run once.
"""
import re
from pathlib import Path

FILE = Path("/data/.openclaw/workspace/persian-cat-care/index.html")
content = FILE.read_text(encoding="utf-8")

# 1) CSS variable definitions (the :root block)
css_var_defs = [
    ("--cream: #fff8ee;",      "--mist: #f5f5f7;"),
    ("--cream-2: #fdecd5;",    "--mist-2: #e8eaee;"),
    ("--warm: #f6d6a8;",       "--silver: #b8bcc2;"),
    ("--pink: #ffb6c1;",       "--blush: #e8d4cc;"),
    ("--pink-deep: #ff8da1;",  "--blush-deep: #c89888;"),
    ("--brown: #6b4423;",      "--charcoal: #3a3a3a;"),
    ("--brown-soft: #8a6240;", "--charcoal-soft: #555555;"),
    ("--gold: #e8b86a;",       "--copper: #b87333;"),
    ("--gold-deep: #c89853;",  "--copper-deep: #8b5a2b;"),
    ("--sky: #b8d8e8;",        "--slate: #6e7884;"),
    ("--sky-deep: #7eb5cf;",   "--slate-deep: #4a5260;"),
    ("--lilac: #d6c4dd;",      "--mauve: #b8a8b0;"),
    ("--mint: #c5e0c5;",       "--sage: #aab5a8;"),
    ("--ink: #4a3528;",        "--ink: #1f1f22;"),
    ("--ink-soft: #6b5040;",   "--ink-soft: #4a4a52;"),
]
for old, new in css_var_defs:
    assert old in content, f"Missing var def: {old}"
    content = content.replace(old, new)

# 2) var() references throughout CSS
var_refs = [
    "var(--cream)", "var(--cream-2)", "var(--warm)",
    "var(--pink)", "var(--pink-deep)",
    "var(--brown)", "var(--brown-soft)",
    "var(--gold)", "var(--gold-deep)",
    "var(--sky)", "var(--sky-deep)",
    "var(--lilac)", "var(--mint)",
]
# Map old to new (the renamed vars)
rename = {
    "var(--cream)":       "var(--mist)",
    "var(--cream-2)":     "var(--mist-2)",
    "var(--warm)":        "var(--silver)",
    "var(--pink)":        "var(--blush)",
    "var(--pink-deep)":   "var(--blush-deep)",
    "var(--brown)":       "var(--charcoal)",
    "var(--brown-soft)":  "var(--charcoal-soft)",
    "var(--gold)":        "var(--copper)",
    "var(--gold-deep)":   "var(--copper-deep)",
    "var(--sky)":         "var(--slate)",
    "var(--sky-deep)":    "var(--slate-deep)",
    "var(--lilac)":       "var(--mauve)",
    "var(--mint)":        "var(--sage)",
}
for old, new in rename.items():
    content = content.replace(old, new)

# 3) Direct hex colors used inside SVGs and inline styles
# Cat body: cream → grey gradient
hex_map = [
    # Cream tones → silver/mist
    ("#fff5e0", "#c9cdd3"),  # body fill
    ("#fffaef", "#e8eaee"),  # mane / face fluff
    ("#f0d8b8", "#a8acb2"),  # mane gradient stop (light)
    ("#e8c8a0", "#6e7378"),  # body gradient stop (dark)

    # Ears (warm tan → dark grey)
    ("#d4a574", "#4a4a4a"),  # ear fill, also some mouth/limb

    # Pinks → dusty rose / blush
    ("#ffb6c1", "#d4a5a5"),  # cheek/inner-ear accent
    ("#ff8da1", "#b87373"),  # nose / deeper pink

    # Eye gradient (green → copper)
    ("#6b8c5a", "#e8b86a"),  # eye light
    ("#3a5230", "#a0683a"),  # eye mid
    ("#1a2818", "#4a2a0a"),  # eye dark

    # Mouth / whisker / paw ink
    ("#4a3528", "#1f1f22"),  # mouth stroke, eye stroke
    ("#6b5040", "#4a4a52"),  # whisker stroke

    # brown rgba shadows → charcoal
    ("rgba(107,68,35,0.15)", "rgba(58,58,58,0.12)"),
    ("rgba(107,68,35,0.08)", "rgba(58,58,58,0.06)"),
    ("rgba(107,68,35,0.2)",  "rgba(58,58,58,0.18)"),
    ("rgba(107,68,35,0.4)",  "rgba(58,58,58,0.35)"),
    ("rgba(107,68,35,0.12)", "rgba(58,58,58,0.10)"),

    # Hero background radial gradients (pink + sky tint → blush + slate)
    ("rgba(255,182,193,0.25)", "rgba(212, 165, 165, 0.18)"),
    ("rgba(184,216,232,0.25)", "rgba(150, 165, 180, 0.18)"),

    # Eye shine white stays white (keep)
]
for old, new in hex_map:
    content = content.replace(old, new)

# 4) Card data-color attribute values
card_color_map = {
    'data-color="pink"':  'data-color="copper"',
    'data-color="blue"':  'data-color="slate"',
    'data-color="lilac"': 'data-color="mauve"',
    'data-color="gold"':  'data-color="sage"',
}
for old, new in card_color_map.items():
    content = content.replace(old, new)

# 5) Tip nth-child hard-coded hex (the ones that didn't go through vars)
# .tip:nth-child(3) used #b89bc4 (lilac-ish) and .tip:nth-child(5) used #88c097 (green)
# Replace with mauve and sage to match the new palette
content = content.replace("#b89bc4", "#9a8a92")
content = content.replace("#88c097", "#8a958a")

# 6) Level badge colors in the JS
level_color_map = {
    "'#88c097'": "'#8a958a'",   # sage
    "'#7eb5cf'": "'#6e7884'",   # slate
    "'#b89bc4'": "'#9a8a92'",   # mauve
    "'#ff8da1'": "'#b87373'",   # dusty rose
    "'#e8b86a'": "'#b87333'",   # copper
    "'#6b4423'": "'#1f1f22'",   # ink
}
for old, new in level_color_map.items():
    content = content.replace(old, new)

# 7) Confetti colors in JS
content = content.replace(
    "['#ff8da1', '#7eb5cf', '#e8b86a', '#b89bc4', '#88c097']",
    "['#b87333', '#6e7884', '#d4a574', '#9a8a92', '#8a958a']"
)

# 8) Fur particles colors array
content = content.replace(
    "['#fffaef', '#fdecd5', '#f6d6a8', '#ffb6c1', '#e8d4b8']",
    "['#e8eaee', '#d5d8dc', '#b8bcc2', '#d4a5a5', '#a8acb2']"
)

FILE.write_text(content, encoding="utf-8")
print("Palette migration complete.")
print(f"File size: {len(content)} bytes")
