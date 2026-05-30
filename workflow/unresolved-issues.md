# Unresolved Issues

## Status

**Release candidate: ready-to-ship** (no known blockers from current scans).
Human literary final readthrough is recommended but not blocking.

## Open Items (Residual Risks)

| ID | Area | Priority | Notes |
|---|---|---|---|
| UI-001 | Literary polish | Medium | Some chapters may retain literal or machine-translation-like phrasing. A representative early/middle/late readthrough is recommended. |
| UI-002 | Terminology consistency | Medium | Glossary exists, but mixed corpus history means terms of address and HP canon terminology should be sampled across the book. |
| UI-003 | Formal data and quotations | Low | No mass numeric corruption was found, but a dedicated audit of numbers, quotes, and special formatting has not been completed. |
| UI-004 | Chapter headings | Low | Source split order and displayed chapter numbering are not identical in every file; EPUB preserves the corpus order and visible headings. |

## Closed Blockers

| ID | Area | Status | Evidence |
|---|---|---|---|
| CB-001 | Missing chapters (ch117–ch126) | **CLOSED** | 126/126 files present |
| CB-002 | Low-ratio completeness (101 chapters) | **CLOSED** | 0 severe low-ratio chapters remain |
| CB-003 | Garbled text critical findings (ch093, ch096) | **CLOSED** | `critical_major_excerpts_still_present=0`; verified absent from final corpus |
| CB-004 | Hard blocker grep (CJK/Cyrillic mojibake) | **CLOSED** | All 12 targeted patterns confirmed absent |
| CB-005 | English honorific residue | **CLOSED** | No `Mr Potter`, `Mr. Granger`, `Mrs Granger`, `Miss Granger`, `Madam Bones` found |
| CB-006 | Major excerpt residue | **CLOSED** | `critical_major_excerpts_still_present=0` |
| CB-007 | Specific garbled patterns (ch003, ch042, ch062, ch064, ch084, ch094, ch109, ch125) | **CLOSED** | All verified absent |

---

*Low-priority open items (UI-001 through UI-004) are advisory and do not block release. They represent recommended polish rather than known defects.*
