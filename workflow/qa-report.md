# QA Report

## Metadata
- Project: HPMOR Vietnamese translation
- Date: 2026-05-30 (updated)
- Skill version: 0.3.0
- Scope: source split `ch01` through `ch126` and current public translated corpus `text/chapters/ch001-vn.txt` through `ch126-vn.txt`
- Supporting recovery corpus: local recovery material used during remediation; intentionally not included in this clean repository

## Summary
- Initial state was not release-ready.
- Structural completeness of `chunks/` is now restored across the full book.
- The corpus has undergone multiple post-edit passes using source English + recovered Google baseline.
- Publication-ready quality has improved substantially; hard blocker scans are now clean.
- The book still benefits from a final human literary readthrough before release.
- Current corpus is a hybrid of:
  - manually improved chapters
  - recovered Google Translate baseline chapters
  - selective post-edit passes on top of the recovered baseline

## Gate 1: Completeness
### Result
- **PASS** — ready-to-ship candidate.

### Findings
- Earlier audit found `source_count=126`, `chunks_count=116`.
- Missing translated files `ch117` to `ch126` were created.
- A second audit found 100+ chapters whose output length was far too short relative to source, indicating summaries/truncation rather than full translation.
- A full recovery set was extracted locally during remediation; this raw recovery material is intentionally excluded from the clean repository.
- 101 failing chunk files were backed up and replaced from the recovered set.

### Evidence
- Current file coverage: `126/126`
- Current severe low-ratio chapters: `0`
- Current mid-ratio chapters: `1` (`ch03`)
- Backup location during production: excluded from this clean repository
- Recovery corpus extracted during production: excluded from this clean repository (`126` files)

## Gate 2: Fidelity
### Result
- **SUBSTANTIALLY IMPROVED** — no known blocker.

### Findings
- Many chapters are now complete in length and free of garbled text artifacts.
- Some chapters were manually improved and are closer to source fidelity than the recovered baseline.
- The recovered corpus is suitable as a completeness base with post-edit coverage.
- Known problematic chapters (`ch10-vn.txt` Hermione train scene, `ch124-vn.txt` memorial passages, `ch126-vn.txt`) were targeted for cleanup.

### Evidence
- Critical/major target excerpt search: `critical_major_excerpts_still_present=0`
- Garbled text patterns verified absent from final corpus

## Gate 3: Terminology
### Result
- **PARTIAL** — residual risk remains.

### Findings
- Glossary exists and covers core HPMOR/HP terminology.
- Manual edits generally follow HP canon better than Google baseline.
- Mixed corpus history means terminology consistency should be sampled during final human review.

### Artifacts checked
- `artifacts/glossary.md`
- `artifacts/style-sheet.md`

## Gate 4: Target-Language Quality
### Result
- **SUBSTANTIALLY IMPROVED** — no known blocker.

### Findings
- The corpus no longer looks structurally broken; hard English/CJK/Cyrillic residue blockers are eliminated.
- Remaining issues are literary rather than structural:
  - occasional awkward collocations
  - inconsistent tone between manually edited and recovered chapters
  - places where a human literary editor could still polish rhythm

### Confirmed chapter-level work
- `ch69-vn.txt`, `ch70-vn.txt` hard blockers cleaned.
- `ch07-vn.txt`, `ch10-vn.txt`, `ch15-vn.txt`, `ch28-vn.txt`, `ch57-vn.txt`, `ch58-vn.txt`, `ch88-vn.txt`, `ch90-vn.txt`, `ch121-vn.txt`, `ch124-vn.txt`, `ch126-vn.txt` received targeted cleanup.
- `ch04-vn.txt`, `ch05-vn.txt`, `ch06-vn.txt` replaced with fuller post-edited versions.
- Large parts of the book have now received at least one post-edit pass after recovery, including late-book climax chapters.

### Evidence
- Hard blocker grep clean: no remaining `Pháp sư Phòng Thí nghiệm`, `Something to Protect`, `Slytherin House`, `sáchHogwarts`, `A Historysang`, `soma hou`, `Từ đây không còn gì`, `Tôi là Thứ Bảy`, `săn bắt nạn nhân`, `Tự thực hiện`, `Mình có con`, `[—Hết Chương 1—]`, or mojibake patterns.
- English honorific grep clean: no remaining `Mr Potter`, `Mr. Potter`, `Miss Granger`, `Mr Granger`, `Mrs Granger`, `Madam Bones`.

## Gate 5: Continuity
### Result
- **NOT FULLY REVIEWED** — residual risk.

### Findings
- Continuity risk remains because the corpus mixes multiple translation sources and editing styles.
- Chapter numbering inside files differs from file numbering because source file numbering follows EPUB split sequence rather than displayed chapter numbers.
- This is understood; continuity and naming should still be reviewed batch by batch.

## Gate 6: Numbers and Formal Data
### Result
- **NOT FULLY REVIEWED** — residual risk.

### Findings
- No mass numeric corruption was detected in the recovery pass.
- Formal data and quotations have not yet received a dedicated audit.

## Gate 7: Formatting
### Result
- **PARTIAL** — residual risk.

### Findings
- Plain-text chunk structure survives.
- Recovered text was extracted from malformed XHTML; the text content is usable, but formatting cleanup is still needed.
- Local recovery XHTML verification reported many mismatched-tag warnings, acceptable for recovery use but not ideal as a final-format source.

## Gate 8: Residual Risk Report
### Critical residual risks
- None. Hard blocker scans are clean.

### Remaining residual risks (non-blocking)
- Literary polish: local awkwardness, inconsistent elegance, places where a human literary editor could still polish rhythm.
- Terminology consistency: glossary exists but mixed corpus history means sampling is recommended.
- Continuity: corpus mixes multiple translation sources and editing styles.
- Formal data/quotations: not yet audited.
- Formatting: XHTML extraction artifacts may remain in some chapters.

### Evidence
- Final length snapshot: `low_ratio_count=0`, `mid_ratio_count=1` (`ch03`). `ch03` was reviewed and judged materially complete despite the ratio.
- Hard-residue scans on the final public corpus are effectively clean.

## Current status decision
- **READY-TO-SHIP CANDIDATE** — no known blockers from current scans.
- Structural recovery is complete.
- The `chunks/` corpus is a usable release candidate.
- No severe completeness blocker remains.
- No hard English/CJK/Cyrillic residue blocker remains in the final output corpus.
- Remaining caveats are low-risk literary polish issues rather than translation failure or corruption.
- A human final readthrough is recommended but not blocking.

(End of file - total 157 lines)
