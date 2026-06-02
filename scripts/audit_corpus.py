#!/usr/bin/env python3
"""Audit hpmor-vi corpus for residue and approved term counts.

Reports:
  - English residue (Dementor/Auror/Patronus, awkward, poor Harry, etc.)
  - Title-case violations of approved Vietnamese HP terms
  - Count of approved Vietnamese terms
  - Word-concat and English bleed patterns
  - Punctuation, URL, time, typo, and other mechanical issues

For each issue pattern, lists up to MAX_EXAMPLES file/line/snippet occurrences
so the editor can locate and fix them.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

CHAPTER_DIR = Path(__file__).resolve().parents[1] / "text" / "chapters"
MAX_EXAMPLES = 5

# Force UTF-8 stdout for Windows consoles
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


# Each pattern: (label, regex, is_blocker)
# is_blocker=True means the issue must be fixed before commercial release.
# is_blocker=False means it's intentional source residue or low-risk.
PATTERNS: list[tuple[str, re.Pattern, bool]] = [
    # --- Hard blockers: must be zero ---
    ("Dementor (English)", re.compile(r"\bDementor\w*\b"), True),
    ("Auror (English)", re.compile(r"\bAuror(s)?\b"), True),
    ("Patronus (English)", re.compile(r"\bPatronus\b"), True),
    ("Hiệu Trưởng (wrong cap)", re.compile(r"\bHiệu\s+Trưởng\b"), True),
    ("Biến Hình (wrong cap)", re.compile(r"\bBiến\s+Hình\b"), True),
    ("Thần Sáng (wrong cap)", re.compile(r"\bThần\s+Sáng\b"), True),
    ("Bàn Chính (legacy)", re.compile(r"\bBàn\s+Chính\b"), True),
    ("hobgit typo", re.compile(r"\bhobgit\b", re.IGNORECASE), True),
    # Fused-word patterns
    ("fused 'làsự'", re.compile(r"làsự"), True),
    ("fused 'làkhông'", re.compile(r"làkhông"), True),
    ("fused 'làcó'", re.compile(r"làcó"), True),
    ("fused 'làrất'", re.compile(r"làrất"), True),
    ("fused 'làmột'", re.compile(r"làmột"), True),
    ("fused 'lànguy'", re.compile(r"lànguy"), True),
    ("fused 'làbạn'", re.compile(r"làbạn"), True),
    ("fused 'làcô'", re.compile(r"làcô"), True),
    ("fused 'làanh'", re.compile(r"làanh"), True),
    ("fused 'córất'", re.compile(r"córất"), True),
    ("fused 'cómột'", re.compile(r"cómột"), True),
    ("fused 'cókhông'", re.compile(r"cókhông"), True),
    ("fused 'cósự'", re.compile(r"cósự"), True),
    ("fused 'cóbạn'", re.compile(r"cóbạn"), True),
    ("fused 'khôngthực sự'", re.compile(r"khôngthực sự"), True),
    ("fused 'khôngthực'", re.compile(r"khôngthực"), True),
    ("fused 'khôngphải'", re.compile(r"khôngphải"), True),
    ("fused 'khôngthể'", re.compile(r"khôngthể"), True),
    ("fused 'khôngcó'", re.compile(r"khôngcó"), True),
    ("fused 'rấtthực sự'", re.compile(r"rấtthực sự"), True),
    ("fused 'thực sựrất'", re.compile(r"thực sựrất"), True),
    ("fused 'thực sựkhông'", re.compile(r"thực sựkhông"), True),
    ("fused 'thực sựlà'", re.compile(r"thực sựlà"), True),
    ("fused 'thực sựcó'", re.compile(r"thực sựcó"), True),
    ("fused 'thực sựđã'", re.compile(r"thực sựđã"), True),
    ("fused 'thực sựrằng'", re.compile(r"thực sựrằng"), True),
    ("fused 'mộtsự'", re.compile(r"mộtsự"), True),
    ("fused 'mộtcách'", re.compile(r"mộtcách"), True),
    ("fused 'mộtthứ'", re.compile(r"mộtthứ"), True),
    ("fused 'lạivà'", re.compile(r"lạivà"), True),
    ("fused 'lạithì'", re.compile(r"lạithì"), True),
    ("fused 'lạinói'", re.compile(r"lạinói"), True),
    ("fused 'lạicó'", re.compile(r"lạicó"), True),
    ("fused 'lạikhông'", re.compile(r"lạikhông"), True),
    ("fused 'lạimột'", re.compile(r"lạimột"), True),
    ("fused 'talà'", re.compile(r"talà"), True),
    ("fused 'tathì'", re.compile(r"tathì"), True),
    ("fused 'bỏtôi'", re.compile(r"bỏtôi"), True),
    ("fused 'thứMuggle'", re.compile(r"thứMuggle"), True),
    ("fused 'thứcon'", re.compile(r"thứcon"), True),
    ("fused 'sống sótkhông'", re.compile(r"sống sótkhông"), True),
    ("fused 'tin tưởngthực'", re.compile(r"tin tưởngthực"), True),
    ("fused 'như vậynghe'", re.compile(r"như vậynghe"), True),
    ("fused 'có vẻhay'", re.compile(r"có vẻhay"), True),
    ("fused 'cảnh sátnêncố'", re.compile(r"cảnh sátnêncố"), True),
    ("fused 'thêmkẻ'", re.compile(r"thêmkẻ"), True),
    ("fused 'vàthêm'", re.compile(r"vàthêm"), True),
    ("fused 'nhìn nhậnnó'", re.compile(r"nhìn nhậnnó"), True),
    ("fused 'đề phòngthầy'", re.compile(r"đề phòngthầy"), True),
    ("fused 'ấyđến'", re.compile(r"ấyđến"), True),
    ("fused 'đócólà'", re.compile(r"đócólà"), True),
    ("fused 'Đó lànội'", re.compile(r"Đó lànội"), True),
    ("fused 'bất tiệnkẻ'", re.compile(r"bất tiệnkẻ"), True),
    ("fused 'ăn trộmthứ'", re.compile(r"ăn trộmthứ"), True),
    ("fused 'tin tưởng thực sựrằng'", re.compile(r"tin tưởng thực sựrằng"), True),
    # Punctuation
    ("space before comma", re.compile(r"\s+,"), True),
    ("space before period", re.compile(r"\s+\.(?!\.)"), True),
    ("space before ;", re.compile(r"\s+;"), True),
    ("space before :", re.compile(r"\s+:"), True),
    ("space before ?", re.compile(r"\s+\?"), True),
    ("space before !", re.compile(r"\s+!"), True),
    ("period-space-!", re.compile(r"\.\s+!"), True),
    ("period-space-!quote", re.compile(r"\.\s+!\""), True),
    # URL/time
    ("URL space", re.compile(r"https?\s+:\s*/\s*/", re.IGNORECASE), True),
    ("time space '7: 24'", re.compile(r"\b\d{1,2}\s+:\s*\d{2}\b|\b\d{1,2}\s*:\s+\d{2}\b"), True),
    # Stray honorifics
    ("Mr. Potter (stray period)", re.compile(r"Mr\.\s+Potter"), True),
    # QA pass 3: broad fused-word regex (the user's independent scan regex)
    ("broad fused '[a-zà-ỹ](connector)[a-zà-ỹ]'", re.compile(r"[a-zà-ỹ](và|thì|không|bạn|thực|Những|anh|ấy|có)[a-zà-ỹ]"), True),
    # QA pass 3: "không?" directly followed by word char (no space)
    ("fused 'không?<word>'", re.compile(r"không\?\w"), True),
    # --- Source-intentional residue (informational, not blocker) ---
    ("residue: awkward (narrative)", re.compile(r"\bawkward(ly|ness)?\b", re.IGNORECASE), False),
    ("residue: poor Harry", re.compile(r"\bpoor\s+Harry\b"), False),
    ("residue: Tolkien's wizard", re.compile(r"\bTolkien's\s+wizard\b"), False),
    # --- Approved term counts (informational) ---
    ("Hiệu trưởng (approved)", re.compile(r"\bHiệu trưởng\b"), False),
    ("Thần sáng (approved)", re.compile(r"\bThần sáng\b"), False),
    ("Biến hình (approved)", re.compile(r"\bBiến hình\b"), False),
    ("Bàn Trưởng (approved)", re.compile(r"\bBàn Trưởng\b"), False),
    ("Giám ngục (approved)", re.compile(r"\bGiám ngục\b"), False),
    ("Bùa hộ mệnh (approved)", re.compile(r"\bBùa hộ mệnh\b"), False),
    ("Chúa tể Hắc ám (approved)", re.compile(r"\bChúa tể Hắc ám\b"), False),
    ("Mr Potter (preserve in formal voice)", re.compile(r"\bMr\s+Potter\b"), False),
]


def find_occurrences(text: str, pat: re.Pattern) -> list[tuple[int, str]]:
    """Return up to MAX_EXAMPLES (line_number_1based, snippet) for matches."""
    out: list[tuple[int, str]] = []
    for m in pat.finditer(text):
        line_no = text.count("\n", 0, m.start()) + 1
        start = max(0, m.start() - 20)
        end = min(len(text), m.end() + 30)
        snippet = text[start:end].replace("\n", " ").replace("\r", " ")
        out.append((line_no, snippet))
        if len(out) >= MAX_EXAMPLES:
            break
    return out


# Chapter list for tracking
chapters = sorted(CHAPTER_DIR.glob("ch*-vn.txt"))
total_chars = 0
counts: dict[str, int] = {label: 0 for label, _, _ in PATTERNS}
blockers: dict[str, int] = {label: 0 for label, _, is_blocker in PATTERNS if is_blocker}
examples: dict[str, list[tuple[str, int, str]]] = {label: [] for label, _, _ in PATTERNS}

for path in chapters:
    text = path.read_text(encoding="utf-8")
    total_chars += len(text)
    for label, pat, is_blocker in PATTERNS:
        n = len(pat.findall(text))
        counts[label] += n
        if is_blocker:
            blockers[label] = blockers.get(label, 0) + n
        if n > 0 and len(examples[label]) < MAX_EXAMPLES:
            for line_no, snippet in find_occurrences(text, pat):
                if len(examples[label]) < MAX_EXAMPLES:
                    examples[label].append((path.name, line_no, snippet))

print(f"Files: {len(chapters)}, total chars: {total_chars:,}")
print()

print("=== Blocker counts (must be 0) ===")
for label in blockers:
    n = counts[label]
    flag = "  ✅" if n == 0 else "  ⚠️"
    print(f"  {n:5d}  {label}{flag}")
print()

print("=== Approved term counts (informational) ===")
for label, _, is_blocker in PATTERNS:
    if not is_blocker and "approved" in label or "preserve" in label:
        print(f"  {counts[label]:5d}  {label}")
print()

print("=== Source-intentional residue (informational) ===")
for label, _, is_blocker in PATTERNS:
    if not is_blocker and "residue" in label:
        print(f"  {counts[label]:5d}  {label}")
print()

# Per-label examples for any blocker with count > 0
print("=== Blocker examples (file/line/snippet) ===")
any_blocker = False
for label, _, is_blocker in PATTERNS:
    if is_blocker and counts[label] > 0:
        any_blocker = True
        print(f"\n  {label} ({counts[label]} occurrences):")
        for fname, line_no, snippet in examples[label]:
            print(f"    {fname}:{line_no}  ...{snippet}...")
if not any_blocker:
    print("  (no blockers)")
print()

# Top files with wrong-cap or English residue
print("=== Per-file residue (blocker hits per file) ===")
per_file_blocker_count: dict[str, int] = {}
for path in chapters:
    text = path.read_text(encoding="utf-8")
    file_blockers = 0
    for label, pat, is_blocker in PATTERNS:
        if is_blocker and "approved" not in label and "preserve" not in label:
            file_blockers += len(pat.findall(text))
    if file_blockers:
        per_file_blocker_count[path.name] = file_blockers
if per_file_blocker_count:
    for fname, c in sorted(per_file_blocker_count.items()):
        print(f"  {fname}: {c} blocker hit(s)")
else:
    print("  (no blockers)")
