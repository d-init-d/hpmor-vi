#!/usr/bin/env python3
"""One-shot fix script for fused-word and punctuation issues across hpmor-vi corpus.

Applies targeted replacements for known issues (from QA pass 2026-06-01).
Idempotent: running twice yields the same result.
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

CHAPTER_DIR = Path(__file__).resolve().parents[1] / "text" / "chapters"
sys.stdout.reconfigure(encoding="utf-8")

# ---- Fused-word fixes (specific patterns that slipped past the regex layer) ----
FUSED_FIXES: list[tuple[str, str, str]] = [
    # (file pattern, search, replace) — file_pattern is a glob to limit scope
    ("*", "làsự", "là sự"),
    ("*", "làkhông", "là không"),
    ("*", "làcó", "là có"),
    ("*", "làrất", "là rất"),
    ("*", "làmột", "là một"),
    ("*", "lànguy hiểm", "là nguy hiểm"),
    ("*", "lànguy", "là nguy"),
    ("*", "làbạn", "là bạn"),
    ("*", "làcô", "là cô"),
    ("*", "làanh", "là anh"),
    ("*", "lànhư", "là như"),
    ("*", "córất", "có rất"),
    ("*", "cómột", "có một"),
    ("*", "cókhông", "có không"),
    ("*", "cósự", "có sự"),
    ("*", "cóbạn", "có bạn"),
    ("*", "khôngthực", "không thực"),
    ("*", "khôngphải", "không phải"),
    ("*", "khôngthể", "không thể"),
    ("*", "khôngcó", "không có"),
    ("*", "rấtthực sự", "rất thực sự"),
    ("*", "rấtnguy hiểm", "rất nguy hiểm"),
    ("*", "rấtnguy", "rất nguy"),
    ("*", "rấtlâu", "rất lâu"),
    ("*", "thực sựrất", "thực sự rất"),
    ("*", "thực sựkhông", "thực sự không"),
    ("*", "thực sựlà", "thực sự là"),
    ("*", "thực sựcó", "thực sự có"),
    ("*", "thực sựđã", "thực sự đã"),
    ("*", "thực sựrằng", "thực sự rằng"),
    ("*", "thực sựthể", "thực sự thể"),
    ("*", "thực sựkhiến", "thực sự khiến"),
    ("*", "vànguy hiểm", "và nguy hiểm"),
    ("*", "mộtsự", "một sự"),
    ("*", "mộtcách", "một cách"),
    ("*", "mộtthứ", "một thứ"),
    ("*", "mộtkhoảng", "một khoảng"),
    ("*", "mộtbạn", "một bạn"),
    ("*", "lạivà", "lại và"),
    ("*", "lạithì", "lại thì"),
    ("*", "lạinói", "lại nói"),
    ("*", "lạicó", "lại có"),
    ("*", "lạikhông", "lại không"),
    ("*", "lạimột", "lại một"),
    ("*", "lạiđể", "lại để"),
    ("*", "talà", "ta là"),
    ("*", "taxin", "ta xin"),
    ("*", "tathì", "ta thì"),
    ("*", "tavẫn", "ta vẫn"),
    ("*", "takhông", "ta không"),
    ("*", "tacũng", "ta cũng"),
    ("*", "bỏtôi", "bỏ tôi"),
    ("*", "thứMuggle", "thứ Muggle"),
    ("*", "thứcon", "thứ con"),
    ("*", "thứWizard", "thứ Wizard"),
    ("*", "thứmỗi", "thứ mỗi"),
    ("*", "sống sótkhông", "sống sót không"),
    ("*", "phảikhông", "phải không"),
    ("*", "nhưngmà", "nhưng mà"),
    ("*", "chỉ làbạn", "chỉ là bạn"),
    ("*", "bạn bèvới", "bạn bè với"),
    ("*", "tin tưởngthực", "tin tưởng thực"),
    ("*", "tin tưởng rằng", "tin tưởng rằng"),
    ("*", "như vậynghe", "như vậy nghe"),
    ("*", "có vẻhay", "có vẻ hay"),
    ("*", "cảnh sátnêncố", "cảnh sát nên cố"),
    ("*", "nhưsự bất tiện", "như sự bất tiện"),
    ("*", "thêmkẻ trộm", "thêm kẻ trộm"),
    ("*", "vàthêmkẻ trộm", "và thêm kẻ trộm"),
    ("*", "nhìn nhậnnó", "nhìn nhận nó"),
    ("*", "đề phòngthầy", "đề phòng thầy"),
    ("*", "ấyđến", "ấy đến"),
    ("*", "phòngthầy ấyđến", "phòng thầy ấy đến"),
    ("*", "đócólà", "đó có là"),
    ("*", "đócólà giới", "đó có là giới"),
    ("*", "khôngngoằn ngoèo", "không ngoằn ngoèo"),
    ("*", "Đó lànội dung", "Đó là nội dung"),
    ("*", "Đó lànội", "Đó là nội"),
    ("*", "có lẽ ", "có lẽ "),  # safe — already correct
    # Punctuation fixes
    ("*", "gì ?", "gì?"),
    ("*", " . !\"", "!\""),
    ("*", " . !", "!\""),  # safer
    # URL and time
    ("*", "https: //", "https://"),
    ("*", "http: //", "http://"),
    # hobgit typo
    ("*", "hobgit", "hobbit"),
    ("*", "Hobgit", "Hobbit"),
]

# ---- Localized fixes (specific to certain files) ----
LOCAL_FIXES: dict[str, list[tuple[str, str]]] = {
    "ch066-vn.txt": [
        # Polish awkward parody translations
        ("Bạn nói tốt đẹp về Kẻ Thù",
         "Ngươi tô vẽ Kẻ Thù đẹp đẽ quá nhỉ"),
        # 'elected' / 'chose' → "chọn" not "sai khiến"
        ("sai khiến gửi Chiếc Nhẫn",
         "chọn gửi Chiếc Nhẫn"),
    ],
}


def main() -> int:
    total_changes = 0
    file_reports: dict[str, int] = {}

    files = sorted(CHAPTER_DIR.glob("ch*-vn.txt"))
    for path in files:
        original = path.read_text(encoding="utf-8")
        text = original
        changes = 0

        # Apply general fused/punctuation fixes
        for _, search, repl in FUSED_FIXES:
            if search in text and search != repl:
                count = text.count(search)
                text = text.replace(search, repl)
                changes += count

        # Apply localized fixes
        local = LOCAL_FIXES.get(path.name, [])
        for search, repl in local:
            if search in text and search != repl:
                count = text.count(search)
                text = text.replace(search, repl)
                changes += count

        # Clean up double-spaces created by insertions
        text = re.sub(r"  +", " ", text)

        if text != original:
            path.write_text(text, encoding="utf-8")
            file_reports[path.name] = changes
            total_changes += changes

    print(f"Total changes: {total_changes}")
    print(f"Files modified: {len(file_reports)}")
    for fname, c in sorted(file_reports.items()):
        print(f"  {c:4d}  {fname}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
