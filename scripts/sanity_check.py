#!/usr/bin/env python3
"""Final sanity check for hpmor-vi corpus.

Verifies:
  - 126 chapter files present (ch001-vn.txt ... ch126-vn.txt)
  - ch066 contains all 16 parody titles and is ~32k chars
  - No previously-identified specific errors remain
  - mechanical_fix.py is idempotent (running --dry-run twice is stable)
  - audit_corpus.py reports zero blockers
  - build_epub.py --check succeeds
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

CHAPTER_DIR = Path(__file__).resolve().parents[1] / "text" / "chapters"
ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

# Force UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
except (AttributeError, ValueError):
    pass


def banner(msg: str) -> None:
    print()
    print("=" * 70)
    print(f"  {msg}")
    print("=" * 70)


def fail(msg: str) -> None:
    print(f"  ❌ FAIL: {msg}")


def ok(msg: str) -> None:
    print(f"  ✅ {msg}")


def check_126_chapters() -> bool:
    banner("Check 1: 126 chapter files present")
    files = sorted(CHAPTER_DIR.glob("ch*-vn.txt"))
    expected = [f"ch{i:03d}-vn.txt" for i in range(1, 127)]
    actual = [f.name for f in files]
    if len(actual) != 126:
        fail(f"Expected 126 files, got {len(actual)}")
        return False
    missing = set(expected) - set(actual)
    if missing:
        fail(f"Missing files: {sorted(missing)}")
        return False
    ok(f"126 chapter files present: ch001-vn.txt ... ch126-vn.txt")
    return True


def check_ch066() -> bool:
    banner("Check 2: ch066-vn.txt — 16 parodies, ~32k chars, no hobgit")
    text = (CHAPTER_DIR / "ch066-vn.txt").read_text(encoding="utf-8")
    chars = len(text)
    parodies = [
        "Chúa của Tính Hợp Lý", "Phù Thủy và Tủ Quần Áo", "My Little Pony: Tình Bạn Là Khoa Học",
        "Làng Ẩn Trong Sự Trong Sáng", "Erdős Trong Xiềng Xích", "ThunderSmarts",
        "He-Man và Các Bậc Thầy của Tính Hợp Lý", "Fate/Sane Night", "Tengen Toppa",
        "Utilitarian Twilight", "Aladdin Jasmine", "Hoàng Tử Hamlet",
        "Cái Tên của Tính Hợp Lý", "Moby Ai?", "Alice Ở Xứ Sở", "Chào Mừng Đến Thế Giới Thực",
    ]
    missing = [p for p in parodies if p not in text]
    if missing:
        fail(f"Missing parodies: {missing}")
        return False
    ok(f"All 16 parody titles present")
    if chars < 30000:
        fail(f"ch066 only {chars} chars (expected ~32k+)")
        return False
    ok(f"ch066 length: {chars:,} chars (≥ 30k)")
    if "hobgit" in text.lower():
        fail("'hobgit' typo still present")
        return False
    ok("'hobgit' typo absent")
    # End-of-chapter check (no truncated mid-sentence)
    stripped = text.rstrip()
    last_char = stripped[-1]
    if last_char not in ".!?…\"”’":
        fail(f"ch066 ends with '{last_char}' — possible truncation")
        return False
    ok(f"ch066 ends cleanly with '{last_char}'")
    return True


def check_specific_errors() -> bool:
    banner("Check 3: Previously-identified specific errors")
    targets = [
        # (file, pattern, label)
        ("ch009-vn.txt", r"làsự", "làsự fused"),
        ("ch009-vn.txt", r"làbạn", "làbạn fused"),
        ("ch009-vn.txt", r"talà", "talà fused"),
        ("ch009-vn.txt", r"bỏtôi", "bỏtôi fused"),
        ("ch009-vn.txt", r"thứMuggle", "thứMuggle fused"),
        ("ch009-vn.txt", r"thứcon", "thứcon fused"),
        ("ch009-vn.txt", r"thực sựrằng", "thực sựrằng fused"),
        ("ch014-vn.txt", r"mộtsự", "mộtsự fused"),
        ("ch021-vn.txt", r"cósự", "cósự fused"),
        ("ch025-vn.txt", r"thực sựđã", "thực sựđã fused"),
        ("ch026-vn.txt", r"làsự", "làsự fused"),
        ("ch043-vn.txt", r"làanh", "làanh fused"),
        ("ch066-vn.txt", r"hobgit", "hobgit typo"),
        ("ch066-vn.txt", r"Bạn nói tốt đẹp về Kẻ Thù", "awkward Boromir line"),
        ("ch066-vn.txt", r"sai khiến gửi", "sai khiến awkward"),
        ("ch079-vn.txt", r"chỉ làbạn", "chỉ làbạn fused"),
        ("ch079-vn.txt", r"mộtthứ", "mộtthứ fused"),
        ("ch079-vn.txt", r"như vậynghe", "như vậynghe fused"),
        ("ch079-vn.txt", r"có vẻhay", "có vẻhay fused"),
        ("ch079-vn.txt", r"bất tiệnkẻ", "bất tiệnkẻ fused"),
        ("ch079-vn.txt", r"ăn trộmthứ", "ăn trộmthứ fused"),
        ("ch099-vn.txt", r"Đó lànội dung", "Đó lànội dung fused"),
        ("ch099-vn.txt", r"sống sótkhông", "sống sótkhông fused"),
        ("ch099-vn.txt", r"làbạn", "làbạn fused"),
        ("ch107-vn.txt", r"mộtsự", "mộtsự fused"),
        ("ch116-vn.txt", r"khoảng một phút\. !", "phút. ! punctuation"),
        # QA pass 3: user-listed 10 specific issues + broad-regex catches
        ("ch019-vn.txt", r"phải không\?vàbạn", "phải không?vàbạn fused"),
        ("ch043-vn.txt", r"chống lạibạn", "chống lạibạn fused"),
        ("ch079-vn.txt", r"Anh ấy cóthực sự không", "cothực sự fused"),
        ("ch079-vn.txt", r"nếu cô ấy cóthì", "cô ấy cóthì fused"),
        ("ch087-vn.txt", r"vàkhông được", "vàkhông được fused"),
        ("ch088-vn.txt", r"\bvàbạn không\b", "vàbạn không fused"),
        ("ch099-vn.txt", r"sáchNhững cuộc", "sáchNhững fused"),
        ("ch099-vn.txt", r"thìanh ấynghĩ", "thìanh ấynghĩ fused"),
        ("ch103-vn.txt", r"cócó điều gì đó", "cócó điều gì đó dedup"),
        ("ch107-vn.txt", r"vàthực hiện", "vàthực hiện fused"),
        # QA pass 5 (2026-06-02): Lý Lan terminology residuals
        ("ch017-vn.txt", r"Death Glare", "Death Glare residual (Lý Lan = Ánh nhìn Chết chóc)"),
        ("ch111-vn.txt", r"\. Eater hỏi|Voldemort\. Eater", "Eater residual (Death Eater typo)"),
        ("ch017-vn.txt", r"Death Eater", "Death Eater residual (Lý Lan = Tử thần Thực tử)"),
    ]
    all_pass = True
    for fname, pattern, label in targets:
        path = CHAPTER_DIR / fname
        if not path.exists():
            fail(f"{fname} not found")
            all_pass = False
            continue
        text = path.read_text(encoding="utf-8")
        if re.search(pattern, text):
            fail(f"{fname}: {label!r} still present")
            all_pass = False
    if all_pass:
        ok(f"All {len(targets)} previously-identified errors absent")
    return all_pass


def check_mechanical_fix_idempotent() -> bool:
    banner("Check 4: mechanical_fix.py is idempotent")
    # Run dry-run twice; second run should also show no changes.
    result1 = subprocess.run(
        ["py", "-X", "utf8", str(SCRIPTS / "mechanical_fix.py"), "--dry-run"],
        capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT),
    )
    result2 = subprocess.run(
        ["py", "-X", "utf8", str(SCRIPTS / "mechanical_fix.py"), "--dry-run"],
        capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT),
    )
    out1 = result1.stdout
    out2 = result2.stdout
    if "no changes" in out1 and "no changes" in out2:
        ok("Both dry-run passes show 'no changes — corpus is clean'")
        return True
    fail("dry-run is not stable across runs")
    print(out1)
    print(out2)
    return False


def check_audit_zero_blockers() -> bool:
    banner("Check 5: audit_corpus.py — zero blockers")
    result = subprocess.run(
        ["py", "-X", "utf8", str(SCRIPTS / "audit_corpus.py")],
        capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT),
    )
    out = result.stdout
    # Check no "⚠️" appears in blocker counts
    in_blocker_section = False
    blocker_section = []
    for line in out.split("\n"):
        if "Blocker counts" in line:
            in_blocker_section = True
            continue
        if in_blocker_section:
            if line.startswith("===") and "Approved" in line:
                break
            blocker_section.append(line)
    blocker_text = "\n".join(blocker_section)
    if "⚠️" in blocker_text:
        fail("Some blocker still present")
        print(blocker_text)
        return False
    ok("All blocker patterns report 0")
    return True


def check_independent_scan_zero() -> bool:
    """Run the user's independent regex scans directly (not via audit) and confirm 0 hits."""
    banner("Check 6: independent scan — broad regex + không?\\w = 0")
    # Original 9-connector set
    p_broad = re.compile(r"[a-zà-ỹ](và|thì|không|bạn|thực|Những|anh|ấy|có)[a-zà-ỹ]")
    # Extended 6-connector set (QA pass 4: mở rộng thêm một/là/rất/như/với/... — 2026-06-02)
    p_broad_ext = re.compile(r"[a-zà-ỹ](một|là|rất|như|với|hay|hơn)[a-zà-ỹ]")
    p_khong = re.compile(r"không\?\w")
    # Ch111 'vào' → 'và o' typo class
    p_va_o = re.compile(r" và o[a-zà-ỹ]")
    broad_hits = 0
    broad_ext_hits = 0
    va_o_hits = 0
    khong_hits = 0
    broad_examples: list[tuple[str, int, str]] = []
    broad_ext_examples: list[tuple[str, int, str]] = []
    va_o_examples: list[tuple[str, int, str]] = []
    khong_examples: list[tuple[str, int, str]] = []
    for path in sorted(CHAPTER_DIR.glob("ch*-vn.txt")):
        text = path.read_text(encoding="utf-8")
        for m in p_broad.finditer(text):
            broad_hits += 1
            if len(broad_examples) < 5:
                line_no = text.count("\n", 0, m.start()) + 1
                broad_examples.append((path.name, line_no, m.group()))
        for m in p_broad_ext.finditer(text):
            broad_ext_hits += 1
            if len(broad_ext_examples) < 5:
                line_no = text.count("\n", 0, m.start()) + 1
                broad_ext_examples.append((path.name, line_no, m.group()))
        for m in p_va_o.finditer(text):
            va_o_hits += 1
            if len(va_o_examples) < 5:
                line_no = text.count("\n", 0, m.start()) + 1
                va_o_examples.append((path.name, line_no, m.group()))
        for m in p_khong.finditer(text):
            khong_hits += 1
            if len(khong_examples) < 5:
                line_no = text.count("\n", 0, m.start()) + 1
                khong_examples.append((path.name, line_no, m.group()))
    if broad_hits > 0:
        fail(f"broad regex still has {broad_hits} hit(s)")
        for fname, line_no, grp in broad_examples:
            print(f"    {fname}:{line_no}  {grp!r}")
        return False
    ok("broad fused-word regex: 0 hits")
    if broad_ext_hits > 0:
        fail(f"extended broad regex still has {broad_ext_hits} hit(s)")
        for fname, line_no, grp in broad_ext_examples:
            print(f"    {fname}:{line_no}  {grp!r}")
        return False
    ok("extended broad fused-word regex: 0 hits")
    if va_o_hits > 0:
        fail(f"'và o' typo regex still has {va_o_hits} hit(s)")
        for fname, line_no, grp in va_o_examples:
            print(f"    {fname}:{line_no}  {grp!r}")
        return False
    ok("'và o' → 'vào' typo regex: 0 hits")
    if khong_hits > 0:
        fail(f"không?\\w regex still has {khong_hits} hit(s)")
        for fname, line_no, grp in khong_examples:
            print(f"    {fname}:{line_no}  {grp!r}")
        return False
    ok("không?\\w regex: 0 hits")
    return True


def check_build_epub() -> bool:
    banner("Check 7: build_epub.py --check")
    result = subprocess.run(
        ["py", "-X", "utf8", str(SCRIPTS / "build_epub.py"), "--check"],
        capture_output=True, text=True, encoding="utf-8", cwd=str(ROOT),
    )
    if result.returncode != 0:
        fail(f"build_epub returned {result.returncode}")
        print(result.stdout)
        print(result.stderr)
        return False
    if "Built" not in result.stdout:
        fail("build_epub output missing 'Built'")
        print(result.stdout)
        return False
    ok(result.stdout.strip().splitlines()[-1])
    return True


def main() -> int:
    checks = [
        check_126_chapters(),
        check_ch066(),
        check_specific_errors(),
        check_mechanical_fix_idempotent(),
        check_audit_zero_blockers(),
        check_independent_scan_zero(),
        check_build_epub(),
    ]
    print()
    print("=" * 70)
    if all(checks):
        print(f"  ALL CHECKS PASSED ({len(checks)}/7)")
        print("=" * 70)
        return 0
    print(f"  FAILED: {sum(1 for c in checks if not c)}/{len(checks)} check(s)")
    print("=" * 70)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
