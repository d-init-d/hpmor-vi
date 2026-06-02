#!/usr/bin/env python3
"""Extra-fused scanner: looks for common 2-char Vietnamese words fused
between two letters (no space). Each match shows whether the boundary
is suspicious or a legitimate bigram like 'mọi người'.
"""
from __future__ import annotations
import glob
import os
import re
import sys

# Common 2-char Vietnamese words that, when missing a space, would create
# a fused word. Test: [letter][WORD][letter] with no space inside.
CANDIDATES = [
    "đã", "sẽ", "còn", "rồi", "vẫn", "cứ", "chỉ", "cũng", "đều",
    "khá", "quá", "hơi", "tới", "từng", "bởi", "bằng", "theo", "trước",
    "sau", "trong", "ngoài", "trên", "dưới", "giữa", "quanh", "dọc",
    "ngang", "vào", "ra", "lên", "xuống", "qua", "lại",
    "của", "với", "cho", "đến", "đi", "để", "vì", "nên", "nếu",
    "khi", "lúc", "kể", "mỗi", "mọi", "hay", "hoặc", "nhưng",
    "mà", "thì", "là", "có", "không", "chưa", "đang",
    "ai", "gì", "nào", "đâu", "sao", "bao", "mấy", "thế",
    "tôi", "em", "anh", "chị", "bà", "ông", "cô", "chú", "bác", "cậu",
    "nó", "họ", "mình", "ta", "chúng",
    "cô ấy", "anh ấy", "cậu ấy", "bà ấy", "ông ấy", "em ấy", "chị ấy",
    "cô ta", "anh ta", "cậu ta", "bà ta", "ông ta", "em ta", "chị ta",
    "hắn", "nàng", "chàng",
    "rất", "lắm", "quá", "hơn", "nhất", "nhé", "nhỉ", "nha",
    "thôi", "vậy", "thật", "đúng", "sai",
    "nữa", "thêm", "lại",
    "học", "dạy", "làm", "chơi", "nói", "nghe", "nhìn", "thấy",
    "biết", "tin", "yêu", "ghét", "sợ",
    "thương", "ghét",
    "luôn", "cũng", "đều", "vẫn",
    "cần", "muốn", "được", "phải", "nên", "có thể",
    "và", "với", "cùng",
    "rồi", "sau đó", "trước đó", "sau này",
    "bởi vì", "vì vậy", "vì thế", "bởi thế",
    "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín", "mười",
    "thứ", "cái", "con", "chiếc", "cuốn", "quyển",
    "như", "như là", "như thể", "như thế",
    "nếu như", "nếu mà", "mà không",
    "tại", "ở", "tại sao", "tại vì",
]

# Build regex: any letter, any of the candidates (as whole word), any letter
# But candidates may include ' ' (multi-word). Skip those.
single_tokens = [c for c in CANDIDATES if " " not in c]
# Sort by length desc so longer matches take priority
single_tokens.sort(key=len, reverse=True)
escaped = [re.escape(t) for t in single_tokens]
pattern_str = r"([a-zà-ỹ])(" + "|".join(escaped) + r")([a-zà-ỹ])"
pat = re.compile(pattern_str)

# Whitelist of legitimate bigrams (curated)
WHITELIST = {
    # 'lại' + verb is OK (react back, do again)
    ("ộ", "lại", "v"), ("ằ", "lại", "v"), ("ứ", "lại", "v"),
    # 'đã'/etc inside proper nouns or known compounds
    ("ậ", "có", " "),  # keep rare
    # Common legitimate bigrams that look fused
    (" ", "và", "o"),  # "và o" is the ch111 typo we already fixed
    (" ", "và", " "),
    (" ", "với", " "),
    (" ", "cho", " "),
    ("ợ", "có", " "),  # legitimate "được có"
    ("ề", "có", " "),  # legitimate "kể có"
    # the "i" + "là" + "m" pattern in "đólàm" is the verb "làm" (make)
    ("ó", "là", "m"),
    ("ấ", "là", "m"),
    # the "i" + "có" + space is "có" in compound
    # etc.
}

chapters = sorted(glob.glob("text/chapters/ch*-vn.txt"))
total_real = 0
real_hits = []
for fp in chapters:
    with open(fp, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            for m in pat.finditer(line):
                first, mid, last = m.group(1), m.group(2), m.group(3)
                if (first, mid, last) in WHITELIST:
                    continue
                # Heuristic: if mid is a "verb-soft" word and we're in past
                # tense, allow; but we can't easily tell. Be conservative.
                real_hits.append((os.path.basename(fp), ln, mid, f"{first}[{mid}]{last}", line.strip()[:120]))
                total_real += 1

print(f"Total potentially fused: {total_real}")
for h in real_hits[:60]:
    print(f"  {h[0]}:{h[1]}: [{h[2]}] ctx={h[3]!r} | {h[4]}")
