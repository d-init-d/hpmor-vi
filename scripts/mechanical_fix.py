#!/usr/bin/env python3
"""Mechanical corpus fixes for hpmor-vi.

Apply the editorial decisions from workflow/glossary.md and workflow/style-sheet.md
across every text/chapters/ch*-vn.txt file. Idempotent — running twice yields the
same result, and `--dry-run` reports zero changes once the corpus is clean.

Phases covered:
  Phase 3 - mechanical: word concatenation, URL/time spacing, dialogue punctuation,
                          English residue cleanup
  Phase 4 - terminology: Dementor->Giám ngục, Auror->Thần sáng, Patronus->Bùa hộ mệnh,
                          Hiệu Trưởng->Hiệu trưởng, Biến Hình->Biến hình,
                          Thuốc Biến Hình->Thuốc Biến hình,
                          Bàn Chính->Bàn Trưởng, Áo Choàng Tàng Hình->Áo choàng Tàng hình
  Phase 5 - honorifics: preserve Mr Potter in formal voice contexts (handled by
                         separate, manual audit; this script only removes 'Mr. Potter'
                         with stray period)

Idempotence: each substitution only counts as a change if `new_text != text`.
Patterns that always match (e.g. `"\s*,\s*` against already-correct `", `) are
tightened so they only match broken forms.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CHAPTER_DIR = Path(__file__).resolve().parents[1] / "text" / "chapters"


# ---------------------------------------------------------------------------
# Phase 3 — mechanical fixes
# ---------------------------------------------------------------------------

# Word concatenation: clear Vietnamese word-merge errors.
# Patterns anchored so they only match broken (no-space) forms.
WORD_CONCAT_FIXES = [
    # Two-prefix + single-word
    (re.compile(r"làsự"), "là sự"),
    (re.compile(r"làcó"), "là có"),
    (re.compile(r"làkhông"), "là không"),
    (re.compile(r"làrất"), "là rất"),
    (re.compile(r"làmột"), "là một"),
    (re.compile(r"lànguy hiểm"), "là nguy hiểm"),
    (re.compile(r"lànguy"), "là nguy"),
    (re.compile(r"làbạn"), "là bạn"),
    (re.compile(r"làcô"), "là cô"),
    (re.compile(r"làanh"), "là anh"),
    (re.compile(r"lànhư"), "là như"),
    (re.compile(r"córất"), "có rất"),
    (re.compile(r"cómột"), "có một"),
    (re.compile(r"cókhông"), "có không"),
    (re.compile(r"cósự"), "có sự"),
    (re.compile(r"cóbạn"), "có bạn"),
    (re.compile(r"khôngthực sự"), "không thực sự"),
    (re.compile(r"khôngthực"), "không thực"),
    (re.compile(r"khôngphải"), "không phải"),
    (re.compile(r"khôngthể"), "không thể"),
    (re.compile(r"khôngcó"), "không có"),
    (re.compile(r"khôngngoằn"), "không ngoằn"),
    (re.compile(r"rấtthực sự"), "rất thực sự"),
    (re.compile(r"rấtnguy hiểm"), "rất nguy hiểm"),
    (re.compile(r"rấtnguy"), "rất nguy"),
    (re.compile(r"rấtlâu"), "rất lâu"),
    (re.compile(r"thực sựrất"), "thực sự rất"),
    (re.compile(r"thực sựkhông"), "thực sự không"),
    (re.compile(r"thực sựlà"), "thực sự là"),
    (re.compile(r"thực sựcó"), "thực sự có"),
    (re.compile(r"thực sựđã"), "thực sự đã"),
    (re.compile(r"thực sựrằng"), "thực sự rằng"),
    (re.compile(r"thực sựthể"), "thực sự thể"),
    (re.compile(r"thực sựkhiến"), "thực sự khiến"),
    (re.compile(r"vànguy hiểm"), "và nguy hiểm"),
    (re.compile(r"vàthêm"), "và thêm"),
    (re.compile(r"bất tiệnkẻ"), "bất tiện kẻ"),
    (re.compile(r"ăn trộmthứ"), "ăn trộm thứ"),
    (re.compile(r"mộtsự"), "một sự"),
    (re.compile(r"mộtcách"), "một cách"),
    (re.compile(r"mộtthứ"), "một thứ"),
    (re.compile(r"mộtkhoảng"), "một khoảng"),
    (re.compile(r"mộtbạn"), "một bạn"),
    # lại/ta/bỏ/thứ prefix
    (re.compile(r"lạivà"), "lại và"),
    (re.compile(r"lạithì"), "lại thì"),
    (re.compile(r"lạinói"), "lại nói"),
    (re.compile(r"lạicó"), "lại có"),
    (re.compile(r"lạikhông"), "lại không"),
    (re.compile(r"lạimột"), "lại một"),
    (re.compile(r"lạiđể"), "lại để"),
    (re.compile(r"talà"), "ta là"),
    (re.compile(r"taxin"), "ta xin"),
    (re.compile(r"tathì"), "ta thì"),
    (re.compile(r"tavẫn"), "ta vẫn"),
    (re.compile(r"takhông"), "ta không"),
    (re.compile(r"tacũng"), "ta cũng"),
    (re.compile(r"bỏtôi"), "bỏ tôi"),
    (re.compile(r"thứMuggle"), "thứ Muggle"),
    (re.compile(r"thứcon"), "thứ con"),
    (re.compile(r"thứWizard"), "thứ Wizard"),
    (re.compile(r"thứmỗi"), "thứ mỗi"),
    (re.compile(r"sống sótkhông"), "sống sót không"),
    (re.compile(r"phảikhông"), "phải không"),
    (re.compile(r"nhưngmà"), "nhưng mà"),
    (re.compile(r"tin tưởngthực"), "tin tưởng thực"),
    (re.compile(r"như vậynghe"), "như vậy nghe"),
    (re.compile(r"có vẻhay"), "có vẻ hay"),
    (re.compile(r"cảnh sátnêncố"), "cảnh sát nên cố"),
    (re.compile(r"cảnh sátnên"), "cảnh sát nên"),
    (re.compile(r"nhưsự bất tiện"), "như sự bất tiện"),
    (re.compile(r"thêmkẻ trộm"), "thêm kẻ trộm"),
    (re.compile(r"vàthêmkẻ trộm"), "và thêm kẻ trộm"),
    (re.compile(r"nhìn nhậnnó"), "nhìn nhận nó"),
    (re.compile(r"đề phòngthầy"), "đề phòng thầy"),
    (re.compile(r"ấyđến"), "ấy đến"),
    (re.compile(r"đócólà"), "đó có là"),
    (re.compile(r"Đó lànội dung"), "Đó là nội dung"),
    (re.compile(r"Đó lànội"), "Đó là nội"),
    (re.compile(r"chỉ làbạn"), "chỉ là bạn"),
    (re.compile(r"bạn bèvới"), "bạn bè với"),
    # --- QA pass 3: broad fused-word patterns found by independent regex scan ---
    # Pattern: <letter><connector><letter|uppercase-letter> with no spaces.
    # Connector set from user's independent scan regex:
    #   và, thì, không, bạn, thực, Những, anh, ấy, có
    # The fix is purely additive (inserts spaces); idempotent.
    (re.compile(r"([a-zA-Zà-ỹÀ-Ỹ])(và|thì|không|bạn|thực|anh|ấy|có)([A-Za-zà-ỹÀ-Ỹ])"), r"\1 \2 \3"),
    (re.compile(r"([a-zA-Zà-ỹÀ-Ỹ])(Những)([A-Za-zà-ỹÀ-Ỹ])"), r"\1 \2 \3"),
    # --- QA pass 3: connector at start of chunk (no letter before, just space/punct) ---
    # Handles: " cóthực", " vàkhông", " vàbạn", " vàthực", " sáchNhững", " thìanh",
    #          " cóthì", " ấynghĩ" — all without a preceding letter, so rule 1 misses them.
    #
    # DISABLED 2026-06-02: this regex produced false positives on legitimate
    # Vietnamese words like "vào", "vàng", "vài", "thìa" (matching them as
    # "và + o", "và + ng", "và + i", "thì + a" fused corruptions). The
    # corpus is clean of fused words; the broader regex cannot distinguish
    # correct prepositions from real corruption. Removed to make
    # mechanical_fix.py idempotent again (was reporting 4,074 false positives).
    # (re.compile(r"([\s\.\,\;\:\?\!\(])(và|thì|không|bạn|thực|anh|có|Những)([A-Za-zà-ỹÀ-Ỹ])"), r"\1 \2 \3"),
    # (re.compile(r"([\s\.\,\;\:\?\!\(])(ấy)([A-Za-zà-ỹÀ-Ỹ])"), r"\1 \2 \3"),
    # Capitalized connector preceded by letter, followed by space/punct
    # e.g. "sáchNhững cuộc" — Những has capital N so rule 1+2 don't fire when next char is space.
    (re.compile(r"([a-zA-Zà-ỹÀ-Ỹ])(Những)([\s\.\,\;\:\?\!\)\(])"), r"\1 Những\3"),
    # "?" directly followed by a word char (no space) — common typo,
    # e.g. "không?Ravenclaw", "không?Harry", "phải không?vàTôi" (when no connector follows).
    (re.compile(r"(\?)(\w)"), r"\1 \2"),
    # User-listed specific QA pass 3 items (idiomatic / context-aware fixes)
    (re.compile(r"chống\s+lại(bạn)"), r"chống lại \1"),
    (re.compile(r"cócó\s+điều"), "có điều"),
    # "?" directly followed by a word char (no space) — common typo,
    # e.g. "không?Ravenclaw", "không?Harry", "phải không?vàTôi" (when no connector follows).
    (re.compile(r"(\?)(\w)"), r"\1 \2"),
    # "!" directly followed by a word char (no space) — common typo,
    # e.g. "nữa rồi!và", "trụ!Đặc biệt", "đi!Đó"
    (re.compile(r"(!)(\w)"), r"\1 \2"),
    # "..." (ellipsis) directly followed by a word char (no space),
    # e.g. "...bình", "...hãy gọi", "...chúc may mắn"
    (re.compile(r"\.{3}(\w)"), r"... \1"),
    # Note: "phút.!" (period directly followed by !) is the desired form per
    # QA pass 2 fix Q2-011 — no space between "." and "!".
    # Specific QA pass 3 fixes not caught by the broad connector patterns
    (re.compile(r"đó\.có"), "đó. có"),
    (re.compile(r"giỏi\.võ"), "giỏi. võ"),
    (re.compile(r"yếu đuối\.một"), "yếu đuối. một"),
    (re.compile(r"cậucó"), "cậu có"),
]

# URL / time spacing — strict, only match broken forms
URL_TIME_FIXES = [
    (re.compile(r"https?\s+:\s*/\s*/"), "https://"),
    (re.compile(r"http\s+:\s*/\s*/"), "http://"),
    (re.compile(r"(\d{1,2})\s+:\s*(\d{2})\b"), r"\1:\2"),
    (re.compile(r"(\d{1,2})\s*:\s+(\d{2})\b"), r"\1:\2"),
]

# Dialogue punctuation: idempotent — only match broken forms.
# Pattern: quote + WHITESPACE + punct [+ WHITESPACE]. Replacement collapses leading
# whitespace inside the quote and preserves any trailing space.
DIALOGUE_PUNCT_FIXES = [
    # Comma inside quote with leading space -> remove leading space, keep trailing.
    (re.compile(r'"\s+,\s*'), '",'),
    # Period / ? / ! inside quote with leading whitespace -> remove leading, keep trailing.
    (re.compile(r'"\s+\.\s*'), '".'),
    (re.compile(r'"\s+\?\s*'), '"?'),
    (re.compile(r'"\s+!\s*'), '"!'),
    # Then put the canonical trailing space back where there is a following word.
    # Only insert space when next char is a word letter, not another period (…).
    (re.compile(r'",([^\s"”’])'), r'", \1'),
    (re.compile(r'"\.([a-zA-Zà-ỹÀ-Ỹ])'), r'". \1'),
    (re.compile(r'"\?([a-zA-Zà-ỹÀ-Ỹ])'), r'"? \1'),
    (re.compile(r'"!([a-zA-Zà-ỹÀ-Ỹ])'), r'"! \1'),
]

# Forbidden comma-then-quote pattern: , "  -> ," and . " -> ."
# Guard against false positives: e.g. "x", etc. "y", i.e. "z", etc.
# Pattern: any punctuation+space+quote, but NOT when the punctuation is
# preceded by a single letter (so e.g. / i.e. / vs. are safe).
DIALOGUE_OUTER_FIXES = [
    (re.compile(r'(?<![A-Za-zà-ỹ])\.\s+"'), '."'),
    (re.compile(r'(?<![A-Za-zà-ỹ]),\s+"'), ',"'),
    (re.compile(r'(?<![A-Za-zà-ỹ]);\s+"'), ';"'),
    (re.compile(r'(?<![A-Za-zà-ỹ])\?\s+"'), '?"'),
    (re.compile(r'(?<![A-Za-zà-ỹ])!\s+"'), '!"'),
]

# Space before comma / period (general, not just inside quotes)
# Only match whitespace immediately before punctuation so we don't touch
# "Mr Potter" or normal text.
# Note: For "!" we require a letter before the space — this preserves
# intentional spacing like "phút. !" where the "." precedes the space.
GENERAL_PUNCT_FIXES = [
    (re.compile(r"\s+,"), ","),
    (re.compile(r"\s+\."), "."),
    (re.compile(r"\s+;"), ";"),
    (re.compile(r"\s+:"), ":"),
    (re.compile(r"\s+\?"), "?"),
    (re.compile(r"([a-zA-Zà-ỹÀ-Ỹ])\s+!"), r"\1!"),
]


# ---------------------------------------------------------------------------
# Phase 4 — terminology normalization
# ---------------------------------------------------------------------------

# All case-sensitive; order matters (longer/more specific first).

TERMINOLOGY_FIXES = [
    # Title-case violations of approved Vietnamese HP terms
    (re.compile(r"\bHiệu\s+Trưởng\b"), "Hiệu trưởng"),
    (re.compile(r"\bBiến\s+Hình\b"), "Biến hình"),
    (re.compile(r"\bHiện\s+Hình\b"), "Hiện hình"),
    (re.compile(r"\bPhượng\s+Hoàng\b"), "Phượng hoàng"),
    (re.compile(r"\bHội\s+Trưởng\b"), "Hội trưởng"),
    (re.compile(r"\bBộ\s+Trưởng\b"), "Bộ trưởng"),
    (re.compile(r"\bGiáo\s+Sư\b"), "Giáo sư"),
    (re.compile(r"\bGiáo\s+Sư\s+Phòng\s+Thủ\b"), "Giáo sư Phòng Thủ"),
    (re.compile(r"\bThần\s+Sáng\b"), "Thần sáng"),
    # Special compounds
    (re.compile(r"\bThuốc\s+Biến\s+Hình\b"), "Thuốc Biến hình"),
    (re.compile(r"\bÁo\s+Choàng\s+Tàng\s+Hình\b"), "Áo choàng Tàng hình"),
    (re.compile(r"\bChúa\s+Tể\s+Hắc\s+Ám\b"), "Chúa tể Hắc ám"),
    (re.compile(r"\bKẻ\s+Ăn\s+Chết\b"), "Kẻ Ăn Chết"),
    (re.compile(r"\bTử\s+Thần\s+Thực\s+Tập\b"), "Tử thần thực tập"),
    # Auror/Patronus/Dementor — replace with approved Vietnamese terms.
    (re.compile(r"\bDementor(?:'s|s)?\b"), "Giám ngục"),
    (re.compile(r"\bdementor(?:'s|s)?\b"), "giám ngục"),
    (re.compile(r"\bDEMENTOR(?:'s|S)?\b"), "GIÁM NGỤC"),
    (re.compile(r"\bAuror(?:s)?\b"), "Thần sáng"),
    (re.compile(r"\bauror(?:s)?\b"), "thần sáng"),
    (re.compile(r"\bAUROR(?:S)?\b"), "THẦN SÁNG"),
    (re.compile(r"\bPatronus\b"), "Bùa hộ mệnh"),
    (re.compile(r"\bpatronus\b"), "bùa hộ mệnh"),
    (re.compile(r"\bPATRONUS\b"), "BÙA HỘ MỆNH"),
    # 'Bàn Chính' (legacy form for Head Table) — normalize to 'Bàn Trưởng'
    (re.compile(r"\bBàn\s+Chính\b"), "Bàn Trưởng"),
    # Quirrell/Voldemort voice: keep 'Mr Potter' in formal contexts.
    # This script does NOT touch 'Mr Potter' — that's a manual review.
    # But it does clean obvious stray-period variants.
    (re.compile(r"Mr\.\s+Potter\b"), "Mr Potter"),
    # hobgit typo (Lord of the Rings parody chapter ch066)
    (re.compile(r"\bhobgit\b"), "hobbit"),
    (re.compile(r"\bHobgit\b"), "Hobbit"),
]


# ---------------------------------------------------------------------------
# Phase 5 — honorifics: handled separately (manual audit)
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def fix_text(text: str) -> tuple[str, dict[str, int]]:
    counts: dict[str, int] = {}
    for pattern, replacement in (
        WORD_CONCAT_FIXES
        + URL_TIME_FIXES
        + DIALOGUE_PUNCT_FIXES
        + DIALOGUE_OUTER_FIXES
        + GENERAL_PUNCT_FIXES
        + TERMINOLOGY_FIXES
    ):
        new_text, n = pattern.subn(replacement, text)
        # Idempotence: only count if the text actually changed.
        if new_text != text:
            counts[pattern.pattern] = n
            text = new_text
    # Clean up accidental double-spaces from insertions
    text = re.sub(r"  +", " ", text)
    return text, counts


def process_file(path: Path) -> dict[str, int]:
    original = path.read_text(encoding="utf-8")
    fixed, counts = fix_text(original)
    if fixed != original:
        path.write_text(fixed, encoding="utf-8")
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Mechanical + terminology fix for hpmor-vi corpus.")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files.")
    parser.add_argument("--files", nargs="*", help="Restrict to specific filenames.")
    args = parser.parse_args()

    # Force UTF-8 stdout so the summary table can render Vietnamese characters
    # even on Windows consoles with cp1252.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

    files = sorted(CHAPTER_DIR.glob("ch*-vn.txt"))
    if args.files:
        wanted = {Path(name).name for name in args.files}
        files = [f for f in files if f.name in wanted]

    grand_total: dict[str, int] = {}
    files_with_changes = 0
    for path in files:
        if args.dry_run:
            original = path.read_text(encoding="utf-8")
            _, counts = fix_text(original)
        else:
            counts = process_file(path)
        for k, v in counts.items():
            grand_total[k] = grand_total.get(k, 0) + v
        if counts:
            files_with_changes += 1
            print(f"{path.name}: {sum(counts.values())} change(s)")

    print("\n=== Grand total ===")
    if not grand_total:
        print("  (no changes — corpus is clean)")
    else:
        for pattern, count in sorted(grand_total.items(), key=lambda x: -x[1]):
            print(f"  {count:5d}  {pattern}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
