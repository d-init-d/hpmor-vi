# QA Report — HPMOR Vietnamese Translation

## Scope
- Project: HPMOR Vietnamese translation
- Date: 2026-05-30
- Chunks covered: 126/126
- Gates executed: all 8

## Artifacts Checked
- Glossary (78 entries)
- Style_Sheet (adaptation rules, forbidden patterns)
- Chunk_Manifest (126 chunks)

## Checks Performed
| Gate | Status | Findings |
|------|--------|----------|
| 1 Completeness | PASS | 0 critical issues |
| 2 Fidelity | PASS | 0 blockers |
| 3 Terminology | FAIL | 4 forbidden-term violations |
| 4 Target-Language | FAIL | 16 concatenated-word issues |
| 5 Continuity | PASS | Character presence confirmed |
| 6 Numbers | PASS | 24 galleon, 15 year refs |
| 7 Formatting | PASS | 1 guillemet, 5 markdown headers |
| 8 Residual Risk | FAIL | 1 stub, 124 missing closing markers |

## Gate 1: Completeness
- Target .txt files: **126** (correct)
- Source HTML files: **127** (correct)
- Missing chapter files (ch001-ch126): **0** (all present)
- Stub files (<200 bytes): **1** (ch101-vn.txt, 158 bytes)

## Gate 2: Fidelity (Blocker Scan)
- English honorifics ("Mr Potter", "Mr. Potter", "Miss Granger", "Mr Granger", "Mrs Granger", "Madam Bones"): **0 matches**
- Vietnamese blockers (Pháp sư Phòng Thí nghiệm, Something to Protect, Slytherin House, sáchHogwarts, A Historysang, soma hou, Từ đây không còn gì, Tời là Thứ Bảy, săn bắt nạn nhân, Tự thực hiện, Mình có con, [—Hết Chương 1—]): **0 matches**

**Result: PASS — No translation blockers detected**

## Gate 3: Terminology
**Forbidden terms found (violations):**
| File | Term | Should be |
|------|------|-----------|
| ch081-vn.txt | nợ máu | món nợ máu |
| ch082-vn.txt | nợ máu | món nợ máu |
| ch083-vn.txt | nợ máu | món nợ máu |
| ch099-vn.txt | nợ máu | món nợ máu |

- "dịch chuyển tức thời" count in corpus: **0** (correct — this phrase is forbidden only for phoenix travel contexts)

**Approved terms presence:**
| Term | Chapters Found |
|------|---------------|
| Lời Thề Bất Khả Phá | 11 |
| phượng hoàng | 33 |
| Patronus | 4 |
| Wizengamot | 32 |
| Hiện Hình | 0 |
| Cổng Phiêu | 1 |

**Result: FAIL — 4 forbidden-term violations in ch081, ch082, ch083, ch099**

## Gate 4: Target-Language Quality
- Concatenated words (lowercase followed by uppercase): **16 files affected**
  - ch009-vn.txt: "nhK" (Harry đập mạnhKẻ Lý Sự)
  - ch010-vn.txt: "ngG" (Huynh trưởngGryffindor)
  - ch013-vn.txt: "arkH" (DarkHeart81. Nhữ)
  - ch019-vn.txt: "arxD" (Anh em nhà MarxDuck Soup)
- Double spaces: **0** (clean)

**Result: FAIL — 16 files with concatenated-word issues**

## Gate 5: Continuity
**Character name presence across 126 chapters:**
| Character | Chapters |
|-----------|----------|
| Quirrell | 95 |
| Harry Potter | 90 |
| Dumbledore | 87 |
| McGonagall | 80 |
| Hermione Granger | 63 |
| Draco Malfoy | 52 |
| Snape | 50 |
| Voldemort | 49 |
| Lucius Malfoy | 28 |

**Closing markers "[—Hết Chương X—]":**
- Chapters with closing marker: **2** (ch101-vn.txt, ch102-vn.txt)
- Chapters without closing marker: **124**

**Result: PASS — All characters present, but closing marker coverage is inconsistent**

## Gate 6: Numbers and Formal Data
- Chapters containing Galleon references: **24**
- Chapters containing year references (1991-1997): **15**
- Chapter title format "Chương X:" issues:
  - Files with "# Chương X:" header: 4 (ch001, ch002, ch003, ch101, ch102)
  - Files with numbered section format (e.g., "7. Sự đối ứng"): varies
  - Title line inconsistency detected but not blocking

**Result: PASS — Numbers and dates preserved**

## Gate 7: Formatting
- Chapters with guillemets «»: **1**
- Chapters with # markdown header: **5** (ch001, ch002, ch003, ch101, ch102)
- Consistent format: Varies by chapter
  - ch001-ch003, ch101-ch102: Use "# Chương X:" header
  - ch004+: Use "Chương X:" without hash
  - Some use numbered section headers (7., 8., etc.)

**Result: PASS — Formatting variation is stylistic, not blocking**

## Gate 8: Residual Risk

**Stub files (<200 bytes):**
- ch101-vn.txt (158 bytes) — stub with minimal content

**Files with missing closing markers:**
- 124 files missing "[—Hết Chương X—]" marker

**Summary of all issues:**
| Category | Count |
|----------|-------|
| Stub files | 1 |
| Missing closing markers | 124 |
| Forbidden term violations | 4 |
| Concatenated-word issues | 16 |
| **Total issues** | **145** |

## Issues
1. **ch081-vn.txt:5** — forbidden term "nợ máu" (should be "món nợ máu")
2. **ch082-vn.txt** — forbidden term "nợ máu"
3. **ch083-vn.txt** — forbidden term "nợ máu"
4. **ch099-vn.txt** — forbidden term "nợ máu"
5. **16 files** — concatenated words (lowercase+uppercase pattern)
6. **ch101-vn.txt** — stub file (158 bytes, incomplete)
7. **124 files** — missing closing marker "[—Hết Chương X—]"

## Residual Risks
- **Terminology inconsistency**: 4 chapters use forbidden "nợ máu" instead of approved "món nợ máu"
- **Stub content**: ch101-vn.txt appears to be placeholder content (158 bytes)
- **Format fragmentation**: Chapter titles use inconsistent formats (# header vs plain text vs numbered sections)
- **Closing markers**: 98% of chapters lack standardized closing markers

## Final Status
**NEEDS_WORK**

**Critical actions required before release:**
1. Fix forbidden term "nợ máu" → "món nợ máu" in ch081, ch082, ch083, ch099
2. Verify/replace stub ch101-vn.txt with actual content
3. Consider standardizing chapter title format
4. Add closing markers "[—Hết Chương X—]" to all 126 chapters

**Passed gates: 5/8 (Gates 2, 5, 6, 7 are clean; Gates 1 partially pass; Gates 3, 4, 8 have issues)**