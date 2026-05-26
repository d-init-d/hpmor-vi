# QA Report

## Metadata
- Project: HPMOR Vietnamese translation
- Date: 2026-05-24
- Skill version: 0.3.0
- Scope: source split `ch01` through `ch126` and current public translated corpus `text/chapters/ch001-vn.txt` through `ch126-vn.txt`
- Supporting recovery corpus: local recovery material used during remediation; intentionally not included in this clean repository

## Summary
- Initial state was not release-ready.
- Structural completeness of `chunks/` is now restored across the full book.
- The corpus has undergone multiple post-edit passes using source English + recovered Google baseline.
- Publication-ready quality has improved substantially, but the book still benefits from a final human literary readthrough before release.
- Current corpus is a hybrid of:
  - manually improved chapters
  - recovered Google Translate baseline chapters
  - selective post-edit passes on top of the recovered baseline

## Gate 1: Completeness
### Result
- PASS after remediation.

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
- FAIL / needs continued review.

### Findings
- Many chapters are now complete in length, but still inherit Google Translate semantic drift and literal phrasing.
- Some chapters were manually improved and are likely closer to source fidelity than the recovered baseline.
- The recovered corpus is suitable as a completeness base, not as final delivery text.

### Known examples
- `ch10-vn.txt`: still contains awkward machine phrasing in Hermione train scene.
- `ch124-vn.txt` in the recovery source had long untranslated English memorial/narrative passages; the public release corpus should still be sampled during final human review.
- `ch126-vn.txt` recovered baseline is much fuller than the original truncated chunk, but still requires stylistic and fidelity post-edit.

## Gate 3: Terminology
### Result
- PARTIAL.

### Findings
- Glossary exists and covers core HPMOR/HP terminology.
- Manual edits generally follow HP canon better than Google baseline.
- Recovered Google chapters still show inconsistent terminology and over-literal renderings.

### Artifacts checked
- `artifacts/glossary.md`
- `artifacts/style-sheet.md`

## Gate 4: Target-Language Quality
### Result
- FAIL.

### Findings
- The corpus no longer looks structurally broken, but many chapters still read as machine translation.
- Common issues:
  - literal phrasing
  - awkward collocations
  - untranslated or partially translated English phrases
  - spacing/punctuation artifacts
  - inconsistent tone between manually edited and recovered chapters

### Confirmed chapter-level issues
- Earlier hard blockers in `ch69-vn.txt` and `ch70-vn.txt` were cleaned.
- `ch07-vn.txt`, `ch10-vn.txt`, `ch15-vn.txt`, `ch28-vn.txt`, `ch57-vn.txt`, `ch58-vn.txt`, `ch88-vn.txt`, `ch90-vn.txt`, `ch121-vn.txt`, `ch124-vn.txt`, and `ch126-vn.txt` received targeted cleanup beyond baseline recovery.
- A small number of chapters still have potential residual style or spacing issues and should be treated as final-pass review candidates rather than structurally broken chapters.

### Progress after report start
- `ch04-vn.txt`, `ch05-vn.txt`, `ch06-vn.txt` were replaced with fuller post-edited versions.
- `ch07-vn.txt` had several obvious nonsense phrases manually corrected.
- `ch10-vn.txt` had its opening Hermione train scene manually cleaned to remove the worst MT artifacts.
- Large parts of the book have now received at least one post-edit pass after recovery, including the late-book climax chapters.

## Gate 5: Continuity
### Result
- NOT FULLY REVIEWED.

### Findings
- Continuity risk remains because the corpus mixes multiple translation sources and editing styles.
- Chapter numbering inside files differs from file numbering because source file numbering follows EPUB split sequence rather than displayed chapter numbers.
- This is understood now, but continuity and naming should still be reviewed batch by batch.

## Gate 6: Numbers and Formal Data
### Result
- NOT FULLY REVIEWED.

### Findings
- No mass numeric corruption was detected in the recovery pass.
- However, formal data and quotations have not yet received a dedicated audit.

## Gate 7: Formatting
### Result
- PARTIAL.

### Findings
- Plain-text chunk structure survives.
- Recovered text was extracted from malformed XHTML; the text content is usable, but formatting cleanup is still needed.
- Local recovery XHTML verification reported many mismatched-tag warnings, which was acceptable for recovery use but not ideal as a final-format source.

## Gate 8: Residual Risk Report
### Critical residual risks
- The current `chunks/` corpus is complete and substantially cleaner than the intake state.
- Remaining risks are now mostly literary rather than structural: local awkwardness, inconsistent elegance, and places where a human literary editor could still polish rhythm.
- Final length snapshot: `low_ratio_count=0`, `mid_ratio_count=1` (`ch03`). `ch03` was reviewed and judged materially complete despite the ratio.
- Hard-residue scans on the final public corpus are now effectively clean; remaining historical scan hits were confined to intermediate split files, which are not delivery artifacts.

### Operational recommendation
1. Treat the excluded local recovery corpus as historical completeness backup only.
2. Use the current `text/chapters/` corpus as the working release candidate.
3. If further work is desired, it should focus on literary polish rather than structural rescue.
4. Recommended but optional: one final human readthrough over representative early, middle, and late chapters for prose rhythm.

## Current status decision
- Structural recovery is complete.
- The `chunks/` corpus is now a usable release candidate.
- No severe completeness blocker remains.
- No hard English/CJK/Cyrillic residue blocker remains in the final output corpus.
- Remaining caveats are low-risk literary polish issues rather than translation failure or corruption.
