# Subagent Dispatch Plan

## Project
- Project: HPMOR Vietnamese translation
- Workflow: D Transcreate Skill
- Execution mode: Sequential coordinator workflow with targeted reviewer roles emulated by the primary agent
- Reason: The working environment did not require persistent parallel workers for this release-candidate packaging pass.

## Role Coverage

| Role | Coverage in this repo | Artifact evidence |
|---|---|---|
| Transcreate Coordinator | Maintained the release-candidate corpus, terminology decisions, workflow artifacts, and EPUB packaging | `translation-brief.md`, `context-plan.md`, `chunk-manifest.md`, `qa-report.md` |
| Terminology Researcher | Captured core HP/HPMOR terms and Vietnamese conventions | `glossary.md`, `glossary.csv` |
| Style Researcher | Captured register, punctuation, naming, and prose conventions | `style-sheet.md` |
| Continuity Reviewer | Tracked core characters, timeline, terms of address, and reveal risks | `story-bible.md`, `source-map.md` |
| Fidelity Reviewer | Audited completeness and residual fidelity risks | `qa-report.md` |
| Formatting Reviewer | Verified plain-text corpus completeness and EPUB packaging structure | `qa-report.md`, `scripts/build_epub.py` |

## Dispatch Notes

- No external subagent output is vendored in this repository.
- Intermediate recovery files and local backups are intentionally excluded.
- Remaining review work is tracked in `unresolved-issues.md`.

