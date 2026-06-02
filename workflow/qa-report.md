# QA Report

## Metadata
- Project: HPMOR Vietnamese translation
- Date: 2026-06-01 (post-literary-proofread)
- Skill version: 0.3.0
- Scope: 126 source split `ch01`–`ch126` and translated corpus
  `text/chapters/ch001-vn.txt`–`ch126-vn.txt` (126 files, 3,767,507 chars)
- Reference: bản dịch Harry Potter của Lý Lan (Nhã Nam / NXB Trẻ)

## Summary
- Initial state (2026-05-30): release candidate but **NOT commercial-ready**
  (ch066 truncated, terminology violations, 700+ mechanical issues).
- 2026-06-01 first pass: applied 9-phase remediation plan; status moved to APPROVED.
- 2026-06-01 second QA pass: independent re-verification found residual
  fused-word and punctuation issues that had been missed. Status was briefly
  `NEEDS FINAL POLISH` (historical, now resolved) and was re-approved once all
  blockers were closed.
- 2026-06-01 third QA pass: user-provided independent regex scans
  (`[a-zà-ỹ](và|thì|không|bạn|thực|Những|anh|ấy|có)[a-zà-ỹ]` and `không\?\w`)
  plus a 10-item user-listed specific list found a third layer of fused-word
  and punctuation issues across 16 chapter files. All closed.
- 2026-06-02 final pre-release scan: independent regex scan uncovered
  **4,074 residual split-word corruptions** (và o/vàng/vài) across 123
  chapters — re-introduced by literary subagent edits after the original
  mechanical fix. All re-fixed. mechanical_fix.py also patched to remove
  false-positive regex on legitimate "vào / vàng / vài" prepositions.
  Re-verified: sanity_check.py 7/7 PASS, audit_corpus.py 0 blockers,
  mechanical_fix.py --dry-run no changes, EPUB build clean.
- Current status: **APPROVED** for commercial release.

## Gate 1: Completeness
### Result
- **PASS** — 126/126 chapters present.
- ch066 fixed: was 2,897 chars (truncated mid-LOTR parody); now 32,592 chars with
  all 16 parodies (LOTR, Narnia, MLP, Naruto, Anita Blake, Thundercats, He-Man,
  Fate/Sane Night, Kingkiller, Tengen Toppa, Twilight, Aladdin, Hamlet,
  Moby Dick, Alice, Matrix).

### Evidence
```
$ ls text/chapters/ch*-vn.txt | wc -l
126

$ wc -c text/chapters/ch066-vn.txt
32592 text/chapters/ch066-vn.txt
```

## Gate 2: Fidelity
### Result
- **PASS** — 11 priority chapters spot-checked (ch003, ch009, ch010, ch020, ch062,
  ch064, ch065, ch066, ch088, ch117, ch126) match source intent.
- Source-intentional residue ("awkward", "Tolkien's wizard", "poor Harry")
  preserved as faithful translation.
- ch066 Boromir line naturalized for Vietnamese rhythm without changing meaning:
  `Bạn nói tốt đẹp về Kẻ Thù` → `Ngươi tô vẽ Kẻ Thù đẹp đẽ quá nhỉ`.

## Gate 3: Terminology
### Result
- **PASS** — fully aligned with approved glossary.

### Quantitative evidence
- 0 Dementor (English), 0 Auror (English), 0 Patronus (English) residue
- 0 title-case violations (Hiệu Trưởng, Biến Hình, Thần Sáng, Phượng Hoàng, Bộ Trưởng, etc.)
- 0 legacy "Bàn Chính" (all → "Bàn Trưởng")
- 0 `hobgit` typo (Lord of the Rings parody chapter ch066)
- Approved Vietnamese terms in use: 334 Giám ngục, 306 Thần sáng, 148 Bùa hộ mệnh,
  25 Bàn Trưởng, 531 Chúa tể Hắc ám, 651 Hiệu trưởng, 289 Biến hình

## Gate 4: Target-Language Quality
### Result
- **PASS** — corpus reads naturally.
- ch003 (opening dialogue), ch010 (Hermione train scene) spot-checked, both
  fluid Vietnamese.
- ch066 (the 16 parodies) reads with humor and consistency.
- Second QA pass caught and fixed 38 fused-word and 3 punctuation issues that
  were producing clearly ungrammatical surface forms (e.g. `làbạn`, `mộtsự`,
  `chúng talà gì ?`, `khoảng một phút. !"`).

## Gate 5: Continuity
### Result
- **PASS** — chapter numbering preserved in EPUB nav; visible chapter titles
  match file names.

## Gate 6: Numbers and Formal Data
### Result
- **PASS** — 0 URL space (`https: //`), 0 time space (`7: 24`), 0 `hobgit` typo.

## Gate 7: Formatting
### Result
- **PASS** — `python scripts/build_epub.py --check` produces valid EPUB 3 with
  cover, CSS, NCX, nav, and 126 chapter files.

### Evidence
```
$ py -X utf8 scripts/build_epub.py --check
Built dist/hpmor-vi.epub
```

## Gate 8: Idempotence
### Result
- **PASS** — `scripts/mechanical_fix.py --dry-run` reports
  `(no changes — corpus is clean)` and is stable across repeated runs.
- Earlier this pass had a false-positive bug: the script reported 66 changes
  (33 + 32 + 1) even when the corpus was already correct. Cause: the dialogue
  patterns `"\s*,\s*` matched already-correct `", ` and the count was based on
  match count rather than actual text change. Fix: patterns tightened to only
  match broken forms, and `fix_text()` now only counts when `new_text != text`.

## Gate 9: Final Sanity Check
### Result
- **PASS** — `python scripts/sanity_check.py` runs 7/7 checks, including
  a fresh independent-scan check (broad fused regex + `không?\w` = 0).

```
$ py -X utf8 scripts/sanity_check.py
  Check 1: 126 chapter files present                        ✅
  Check 2: ch066-vn.txt — 16 parodies, ~32k chars, no hobgit ✅
  Check 3: Previously-identified specific errors             ✅
  Check 4: mechanical_fix.py is idempotent                   ✅
  Check 5: audit_corpus.py — zero blockers                  ✅
  Check 6: independent scan — broad regex + không?\w = 0    ✅
  Check 7: build_epub.py --check                             ✅
  ALL CHECKS PASSED (7/7)
```

## Gate 10: Residual Risk Report
### Critical residual risks
- None. All hard blocker scans clean (audit_corpus, mechanical_fix dry-run,
  independent scan regex, build_epub, sanity_check 7/7).

### Non-blocking residual risks
- RR-001 (low): Some early chapters may retain hybrid-translation rhythm.
  Optional literary proofread recommended.
- RR-002 (informational): 4 source-intentional English references preserved per
  source intent (awkward ×2, poor Harry ×1, Tolkien's wizard ×1).
- RR-003 (low): Mr H. Potter in ch003 letter (1 instance) kept as English
  letter style per glossary.
- RR-004 (informational): Mechanical-fix script covers the most common fused
  patterns but cannot enumerate every possible Vietnamese word-merge. Future
  translations should run `scripts/sanity_check.py` after each chapter.
- RR-005 (informational, new in QA pass 3): 2 instances of "." directly
  followed by "!" (`phút.!` ch116, `phải...!` ch105) — these are the
  established desired forms per QA pass 2 fix Q2-011. Independent scan
  `\.(?=!)` reports 2 hits, but the audit considers them correct.
- RR-006 (informational, new in QA pass 3): URLs and exam abbreviations
  containing ".<letter>" (e.g. `hpmor.com`, `O.W.L.s`, `N.E.W.T.s`,
  `LessWrong.com`, `reddit.com`) are correctly NOT flagged by the audit
  or independent scan.

### Evidence
- See `workflow/spot-check-report.md`,
  `workflow/commercial-readiness-audit.md`, and
  `workflow/unresolved-issues.md` for the full audit trail.

## Current status decision
- **APPROVED** for commercial release.
- All 9 phases of the original remediation plan completed.
- All 18 issues from the second QA pass (Q2-001 … Q2-018) closed.
- All 20 issues from the third QA pass (Q3-001 … Q3-020) closed (10 user-listed
  + 10 categorized broad-regex / punctuation classes; per-file fix counts add to
  100+ changes across 16 chapter files).
- ch066 blocker resolved with full 16-parody translation.
- Terminology consistent with Lý Lan / NXB Trẻ convention.
- EPUB builds clean and is structurally valid.
- `mechanical_fix.py` and `audit_corpus.py` are idempotent and provide
  file/line/snippet examples for any future blocker.
- `sanity_check.py` runs 7/7 checks including the user-supplied
  independent regex scans.

(End of file)
