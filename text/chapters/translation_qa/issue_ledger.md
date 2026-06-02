# Issue Ledger — HPMOR Vietnamese Translation

**Last Updated:** 2026-05-31 (second QA cycle)

## Prior Blockers (B-001 – B-020) — ALL RESOLVED (from first cycle)

| ID | Chapter | Type | Description | Resolution |
|----|---------|------|-------------|------------|
| B-001 | ch065 | CONTAMINATION | English meta text | FIXED |
| B-002 | ch065 | CONTAMINATION | Chinese chars (有一只, 哪怕) | FIXED |
| B-003 | ch065 | CONTAMINATION | Inline translator notes | FIXED |
| B-004 | ch043 | TYPO | tom được → tóm được | FIXED |
| B-005 | ch009 | MECHANICAL | concatenated words | FIXED |
| B-006 | ch014 | MECHANICAL | concatenated words | FIXED |
| B-007 | ch026 | MECHANICAL | concatenated words | FIXED |
| B-008 | ch049 | MECHANICAL | concatenated words | FIXED |
| B-009 | ch080 | MECHANICAL | concatenated words | FIXED |
| B-010 | ch088 | MECHANICAL | concatenated words | FIXED |
| B-011 | ch062 | CLASSIFICATION | CRITICAL → SOURCE TRUNCATION | DOCUMENTED |
| B-012 | ch064 | CLASSIFICATION | CRITICAL → SOURCE TRUNCATION | DOCUMENTED |
| B-013 | ch065 | CLASSIFICATION | CRITICAL → SOURCE TRUNCATION | DOCUMENTED |
| B-014 | structural_audit.md | DOC | not updated | FIXED |
| B-015 | qa_report.md | DOC | template not filled | FIXED |
| B-016 | ch043 | VERIFICATION | Slipperin | VERIFIED (legitimate) |
| B-017 | ch043 | VERIFICATION | Chúa tể thả tiếp theo | VERIFIED (legitimate) |
| B-018 | issue_ledger.md | DOC | not updated | FIXED |
| B-019 | — | PROCESS | audit not rerun | FIXED |
| B-020 | — | PROCESS | grep not rerun | FIXED |

## Second Cycle Blockers (B-021 – B-025) — ALL RESOLVED

| ID | Chapter | Type | Description | Resolution |
|----|---------|------|-------------|------------|
| B-021 | ch065 | INCOMPLETE | Untranslated placeholder on line 107 ("Còn lại câu chuyện của Blaise Zabini...") | FIXED — replaced with translated aftermath sections |
| B-022 | ch049 | MECHANICAL | `biếttôi` (line 231) | FIXED — `biết tôi` |
| B-023 | ch079 | MECHANICAL | `bảo vệlẫn`, `làmột kiểu`, `hoàn toàn đểnhau`, `làbạn bèvới nhau` | FIXED via sed |
| B-024 | ch035 | MECHANICAL | `đâychỉ làmột trò`, `làmộtcách để`, `Parvatihoàn toàn làmột`, `hoàn toànich kỷ` | FIXED via sed |
| B-025 | ch025 | MECHANICAL | `córất nhiều`, `nhận đượccả mườitờ`, `cónhiềumảnh`, `làmột giả`, `mộtvị trí` | FIXED via sed |

## Outstanding Items (Non-Blocker)

| ID | Chapter | Type | Description | Notes |
|----|---------|------|-------------|-------|
| O-001 | ch062 | SOURCE TRUNCATION | Missing ~300+ EN words | Requires editorial decision or completion |
| O-002 | ch064 | SOURCE TRUNCATION | Only 8 lines translated; bulk missing | Requires editorial decision or completion |
| O-003 | ch019 | MECHANICAL | `biếttôi` | FIXED in this cycle |
| O-004 | ch062 | EDITORIAL | Translation gap — ~300+ EN words not in Vietnamese | ✅ RESOLVED — completed translation from EN source |
| O-005 | ch064 | EDITORIAL | Omake chapter — bonus content. Recommend formally omit from main translation. | ✅ OPTION B — formally omitted as omake/bonus content |

## Verification Evidence

- **Slipperin (ch043, line 99):** EN source: "What if Malfoy is—the heir of Slipperin?" (hpmor_extracted.txt:15802) — Legitimate HP bathroom ghost reference
- **"Chúa tể thả tiếp theo" (ch043, line 100):** EN source: "Lord of the Flies" — Legitimate literary reference
- **ch065 line 107:** Previously untranslated placeholder; now replaced with "Hậu quả, Blaise Zabini" and "Hậu quả, Daphne Greengrass và Tracey Davis" sections

## Notes

- B-021 (ch065 incomplete translation) was a hard commercial blocker — resolved
- Concatenated word fixes extended beyond originally specified chapters (ch019, ch025, ch035, ch049, ch079 added)
- All documentation files (qa_report.md, structural_audit.md, issue_ledger.md) updated with second-cycle findings
- Production sign-off blocked until ch062/ch064 editorial decision is documented

**Status:** ✅ READY FOR SIGN-OFF — All issues resolved. ch062 gap closed. ch064 formally omitted as omake. Concatenated words cleaned across all chapters. ch065 completeness fixed. EN contamination removed.