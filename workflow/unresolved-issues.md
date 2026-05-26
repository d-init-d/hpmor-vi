# Unresolved Issues

## Status

The release candidate is structurally complete and packaged as EPUB, but it still benefits from human literary review.

## Open Items

| ID | Area | Priority | Notes |
|---|---|---|---|
| UI-001 | Literary polish | Medium | Some chapters may retain literal or machine-translation-like phrasing. A representative early/middle/late readthrough is recommended. |
| UI-002 | Terminology consistency | Medium | Glossary exists, but mixed corpus history means terms of address and HP canon terminology should be sampled across the book. |
| UI-003 | Formal data and quotations | Low | No mass numeric corruption was found, but a dedicated audit of numbers, quotes, and special formatting has not been completed. |
| UI-004 | Chapter headings | Low | Source split order and displayed chapter numbering are not identical in every file; EPUB preserves the corpus order and visible headings. |

## Closed / Not Included

- Missing-chapter blocker: closed. The release corpus contains 126 chapter files.
- Low-ratio completeness blocker: closed. No severe low-ratio chapters remain according to the QA snapshot.
- Raw recovery corpus: not included. It was used only as a completeness aid and is intentionally excluded from the clean repository.

