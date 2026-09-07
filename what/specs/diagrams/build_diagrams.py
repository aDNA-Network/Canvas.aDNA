#!/usr/bin/env python3
"""Build the spec diagrams that shipped examples reference.

Run from anywhere::

    <Canvas.aDNA>/what/production/canvas_core/.venv/bin/python \
        what/specs/diagrams/build_diagrams.py

Why this file exists rather than two committed PNGs with no provenance: at Blueprint P2c the
producer re-gate found **3 HIGH ``CV-FILE-PROPS-01/file_missing`` findings** — three shipped
examples referencing images that did not exist and were not gitignored. Canvas went MIT and
publicly clonable on 2026-09-04, so an external clone got three broken examples. The images are now
real, and *generated*, so anyone can see what they assert and regenerate them.

Deterministic: no randomness, no wall-clock, fixed fonts with an explicit fallback chain. Pillow is
the only dependency (already an environment dep of the ``canvas_core`` import surface).

Both diagrams are authored at 2× and downsampled, which is the cheapest way to get clean edges out
of PIL's non-antialiased primitives.
"""

from __future__ import annotations

import os
import sys

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

S = 2  # supersample factor

INK = (32, 32, 34)
MUTED = (122, 122, 128)
RULE = (198, 198, 204)
PAPER = (255, 255, 255)
WASH = (244, 244, 246)
# Mondrian's three, muted enough to print.
RED = (192, 57, 43)
BLUE = (41, 89, 156)
YELLOW = (222, 170, 44)

_FONT_DIRS = [
    "/System/Library/Fonts/Supplemental",
    "/System/Library/Fonts",
    "/Library/Fonts",
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts",
]
_REGULAR = ["Arial.ttf", "Helvetica.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
_BOLD = ["Arial Bold.ttf", "Arial-Bold.ttf", "DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"]


def font(size: int, bold: bool = False):
    for directory in _FONT_DIRS:
        if not os.path.isdir(directory):
            continue
        for name in (_BOLD if bold else _REGULAR):
            path = os.path.join(directory, name)
            if os.path.isfile(path):
                return ImageFont.truetype(path, size * S)
    return ImageFont.load_default()


def centre(draw, box, text, f, fill=INK):
    x0, y0, x1, y1 = box
    bb = draw.textbbox((0, 0), text, font=f)
    draw.text(((x0 + x1 - (bb[2] - bb[0])) / 2, (y0 + y1 - (bb[3] + bb[1])) / 2),
              text, font=f, fill=fill)


def box(draw, rect, *, fill=PAPER, outline=INK, width=2, radius=6):
    draw.rounded_rectangle([c * S for c in rect], radius=radius * S,
                           fill=fill, outline=outline, width=width * S)


def save(img: Image.Image, name: str) -> None:
    out = img.resize((img.width // S, img.height // S), Image.LANCZOS)
    path = os.path.join(HERE, name)
    out.save(path, "PNG", optimize=True)
    print(f"wrote {path} ({out.width}x{out.height})")


# ---------------------------------------------------------------------------
# canvas_grammar.png — referenced by document_generator (whitepaper) + deck_generator
# ---------------------------------------------------------------------------

def canvas_grammar() -> None:
    """The Standard's central claim: a canvas is positioned typed components on a surface."""
    W, H = 960, 460
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    f_title = font(19, bold=True)
    f_lbl = font(13, bold=True)
    f_body = font(11)
    f_note = font(10)

    d.text((36 * S, 26 * S), "The aDNA Canvas grammar", font=f_title, fill=INK)
    d.text((36 * S, 54 * S), "A canvas is a set of typed components positioned on a surface — "
                             "the near-universal 2D output primitive.",
           font=f_body, fill=MUTED)

    # The surface frame.
    box(d, (36, 88, 924, 372), fill=WASH, outline=RULE, width=2, radius=10)
    d.text((48 * S, 98 * S), "CANVAS  ·  surface", font=f_lbl, fill=MUTED)

    # Panel: the addressable region.
    box(d, (60, 126, 520, 352), fill=PAPER, outline=BLUE, width=2)
    d.text((74 * S, 138 * S), "PANEL", font=f_lbl, fill=BLUE)
    d.text((74 * S, 156 * S), "an addressable region", font=f_note, fill=MUTED)

    comps = [
        ("text", RED), ("typography", RED),
        ("image", YELLOW), ("video", YELLOW),
        ("shape", BLUE), ("embed", BLUE),
    ]
    for i, (label, colour) in enumerate(comps):
        col, row = i % 2, i // 2
        x = 78 + col * 216
        y = 184 + row * 52
        box(d, (x, y, x + 196, y + 38), fill=PAPER, outline=colour, width=2, radius=4)
        centre(d, (x * S, y * S, (x + 196) * S, (y + 38) * S), label, f_body, fill=INK)

    # Links between panels — the graph half of the grammar.
    box(d, (560, 126, 900, 236), fill=PAPER, outline=BLUE, width=2)
    d.text((574 * S, 138 * S), "PANEL", font=f_lbl, fill=BLUE)
    d.text((574 * S, 156 * S), "linked, not merely adjacent", font=f_note, fill=MUTED)
    box(d, (578, 182, 882, 220), fill=PAPER, outline=RED, width=2, radius=4)
    centre(d, (578 * S, 182 * S, 882 * S, 220 * S), "link  ·  edge", f_body)

    d.line([(520 * S, 180 * S), (560 * S, 180 * S)], fill=INK, width=2 * S)
    d.polygon([(560 * S, 180 * S), (551 * S, 175 * S), (551 * S, 185 * S)], fill=INK)

    # The reserved block — the additive fork.
    box(d, (560, 258, 900, 352), fill=PAPER, outline=RULE, width=2)
    d.text((574 * S, 270 * S), "metadata.frontmatter._reserved", font=f_lbl, fill=MUTED)
    for j, line in enumerate([
        "aDNA semantics live here, namespaced.",
        "Baseline tooling ignores the block, so",
        "every aDNA canvas is a valid JSON Canvas.",
    ]):
        d.text((574 * S, (292 + j * 17) * S), line, font=f_note, fill=MUTED)

    d.text((36 * S, 398 * S),
           "Fork, don't drift: the extension is additive; a conformant canvas degrades to baseline.",
           font=f_body, fill=MUTED)
    d.text((36 * S, 420 * S),
           "Generated by what/specs/diagrams/build_diagrams.py — aDNA Canvas Standard, MIT © aDNA Labs.",
           font=f_note, fill=RULE)

    save(img, "canvas_grammar.png")


# ---------------------------------------------------------------------------
# diagnostic_odyssey.png — referenced by document_generator (grant_proposal)
# ---------------------------------------------------------------------------

def diagnostic_odyssey() -> None:
    """The rare-disease diagnostic odyssey, as the grant proposal's figure 1."""
    W, H = 960, 380
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    f_title = font(19, bold=True)
    f_lbl = font(11, bold=True)
    f_body = font(11)
    f_note = font(10)

    d.text((36 * S, 26 * S), "The diagnostic odyssey", font=f_title, fill=INK)
    d.text((36 * S, 54 * S),
           "The path a family walks before a name exists for what they have.",
           font=f_body, fill=MUTED)

    # The spine.
    y = 176
    d.line([(52 * S, y * S), (908 * S, y * S)], fill=RULE, width=3 * S)

    stops = [
        ("Symptom\nonset", "year 0", MUTED),
        ("Primary\ncare", "+ 4 mo", MUTED),
        ("Specialist 1", "+ 11 mo", MUTED),
        ("Specialist 2", "+ 2.1 yr", MUTED),
        ("Genetic\npanel", "+ 3.4 yr", YELLOW),
        ("Re-analysis", "+ 5.2 yr", YELLOW),
        ("Diagnosis", "+ 6.3 yr", BLUE),
    ]
    n = len(stops)
    x0, x1 = 76, 884
    step = (x1 - x0) / (n - 1)
    for i, (label, when, colour) in enumerate(stops):
        cx = x0 + i * step
        r = 9 if colour is MUTED else 11
        d.ellipse([(cx - r) * S, (y - r) * S, (cx + r) * S, (y + r) * S],
                  fill=PAPER, outline=colour if colour is not MUTED else INK, width=3 * S)
        lines = label.split("\n")
        for j, line in enumerate(lines):
            bb = d.textbbox((0, 0), line, font=f_lbl)
            d.text((cx * S - (bb[2] - bb[0]) / 2, (y - 62 + j * 15) * S),
                   line, font=f_lbl, fill=INK)
        bb = d.textbbox((0, 0), when, font=f_note)
        d.text((cx * S - (bb[2] - bb[0]) / 2, (y + 22) * S), when, font=f_note, fill=MUTED)

    # The span that the proposal is about.
    d.line([(76 * S, 246 * S), (884 * S, 246 * S)], fill=RED, width=2 * S)
    for cx in (76, 884):
        d.line([(cx * S, 240 * S), (cx * S, 252 * S)], fill=RED, width=2 * S)
    bb = d.textbbox((0, 0), "median 6.3 years  ·  7.3 specialists  ·  2–3 misdiagnoses", font=f_lbl)
    label_w = bb[2] - bb[0]
    d.rectangle([(480 - label_w / 2 - 8) * S, 236 * S, (480 + label_w / 2 + 8) * S, 258 * S],
                fill=PAPER)
    d.text(((480 - label_w / 2) * S, 240 * S),
           "median 6.3 years  ·  7.3 specialists  ·  2–3 misdiagnoses", font=f_lbl, fill=RED)

    d.text((36 * S, 292 * S),
           "Where the harness intervenes: re-analysis is continuous rather than episodic, and every "
           "ranked differential", font=f_body, fill=MUTED)
    d.text((36 * S, 310 * S),
           "carries the evidence subgraph that produced it — so a negative panel stays a live "
           "question, not a dead end.", font=f_body, fill=MUTED)
    d.text((36 * S, 344 * S),
           "Illustrative figure. Generated by what/specs/diagrams/build_diagrams.py — "
           "MIT © aDNA Labs.", font=f_note, fill=RULE)

    save(img, "diagnostic_odyssey.png")


if __name__ == "__main__":
    canvas_grammar()
    diagnostic_odyssey()
    sys.exit(0)
