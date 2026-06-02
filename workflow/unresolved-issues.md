# Unresolved Issues

## Status

**APPROVED 2026-06-01 (post-QA-pass-3)** — no blockers. User-supplied independent
regex scans (`[a-zà-ỹ](và|thì|không|bạn|thực|Những|anh|ấy|có)[a-zà-ỹ]` and
`không\?\w`) plus a 10-item user-listed specific list found a third layer of
fused-word and punctuation issues across 16 chapter files. All closed.

## QA Pass 3 — 2026-06-01

A third QA pass, driven by user-supplied independent regex scans, detected a
third layer of fused-word and punctuation issues across 16 chapter files. They
are now closed.

| ID | Area | Status | Evidence |
|---|---|---|---|
| Q3-001 | ch019:368 "phải không?vàbạn" fused | **CLOSED** | 0 fused occurrences |
| Q3-002 | ch043:49 "chống lạibạn" fused | **CLOSED** | "chống lại bạn" after fix |
| Q3-003 | ch079:176 "Anh ấy cóthực sự không?" | **CLOSED** | 0 fused occurrences |
| Q3-004 | ch079:188 "nếu cô ấy cóthì" | **CLOSED** | 0 fused occurrences |
| Q3-005 | ch087:57 "vàkhông được" | **CLOSED** | 0 fused occurrences |
| Q3-006 | ch088:447 "vàbạn không" | **CLOSED** | 0 fused occurrences |
| Q3-007 | ch099:17 "sáchNhững cuộc" | **CLOSED** | 0 fused occurrences |
| Q3-008 | ch099:82 "thìanh ấynghĩ" | **CLOSED** | 0 fused occurrences |
| Q3-009 | ch103:83 "cócó điều" dedup | **CLOSED** | "có điều" after fix |
| Q3-010 | ch107:250 "vàthực hiện" | **CLOSED** | 0 fused occurrences |
| Q3-011 | Broad regex matches (34 hits across ch010, ch017, ch019, ch021, ch026, ch035, ch043, ch049, ch079, ch088, ch099, ch107, ch111, ch116) | **CLOSED** | broad regex scan = 0 |
| Q3-012 | "không?X" patterns (15 hits across ch009, ch014, ch019, ch035, ch061, ch083, ch088) | **CLOSED** | không?\w scan = 0 |
| Q3-013 | "X.Y" word-merge cases (ch021:61 "đó.có", ch021:120 "giỏi.võ", ch025:27 "yếu đuối.một", ch088 "cậucó") | **CLOSED** | 0 occurrences |
| Q3-014 | "phút.!" / "phải...!" already in desired form per Q2-011 | **DOCUMENTED** | RR-005 in qa-report.md |
| Q3-015 | "X!" + lowercase letter (37 cases: ch017:91, ch019:367, ch035:122, ch043:90, ch049:190) | **CLOSED** | 0 occurrences |
| Q3-016 | "...X" ellipsis-merge (16 cases: ch003, ch014, ch017, ch019, ch021, ch027) | **CLOSED** | 0 occurrences |
| Q3-017 | "chống lại bạn" idiom in ch043 | **CLOSED** | 0 occurrences |
| Q3-018 | sanity_check.py expanded with independent scan check (Check 6) | **CLOSED** | 7/7 checks pass |
| Q3-019 | audit_corpus.py expanded with broad regex + "không?<word>" blockers | **CLOSED** | 0 hits |
| Q3-020 | mechanical_fix.py restricted `\s+!` rule to require letter before space (preserves "phút. !" if user prefers) | **CLOSED** | idempotent |



| ID | Area | Status | Evidence |
|---|---|---|---|
| Q2-001 | `làsự`, `làmột`, `lànguy`, `làbạn`, `làanh`, `làcô`, `làkhông`, `làcó`, `làrất` | **CLOSED** | 0 fused occurrences corpus-wide |
| Q2-002 | `córất`, `cómột`, `cókhông`, `cósự`, `cóbạn` | **CLOSED** | 0 fused occurrences |
| Q2-003 | `khôngthực`, `khôngphải`, `khôngthể`, `khôngcó` | **CLOSED** | 0 fused occurrences |
| Q2-004 | `rấtthực sự`, `rấtnguy`, `rấtlâu` | **CLOSED** | 0 fused occurrences |
| Q2-005 | `thực sựrất`, `thực sựkhông`, `thực sựlà`, `thực sựcó`, `thực sựđã`, `thực sựrằng` | **CLOSED** | 0 fused occurrences |
| Q2-006 | `mộtsự`, `mộtcách`, `mộtthứ`, `mộtkhoảng`, `mộtbạn` | **CLOSED** | 0 fused occurrences |
| Q2-007 | `lạivà`, `lạithì`, `lạinói`, `lạicó`, `lạikhông`, `lạimột`, `lạiđể` | **CLOSED** | 0 fused occurrences |
| Q2-008 | `talà`, `taxin`, `tathì`, `tavẫn`, `takhông`, `tacũng` | **CLOSED** | 0 fused occurrences |
| Q2-009 | `bỏtôi`, `thứMuggle`, `thứcon`, `thứWizard`, `thứmỗi` | **CLOSED** | 0 fused occurrences |
| Q2-010 | `sống sótkhông`, `tin tưởngthực`, `như vậynghe`, `có vẻhay`, `cảnh sátnêncố`, `thêmkẻ`, `vàthêm`, `nhìn nhậnnó`, `đề phòngthầy`, `ấyđến`, `đócólà`, `Đó lànội`, `bất tiệnkẻ`, `ăn trộmthứ` | **CLOSED** | 0 fused occurrences |
| Q2-011 | `khoảng một phút. !"` (ch116:36) | **CLOSED** | `phút.!"` after fix |
| Q2-012 | `gì ?` (ch009) | **CLOSED** | `gì?` after fix |
| Q2-013 | `hobgit` typo (ch066:27) | **CLOSED** | `hobbit` everywhere |
| Q2-014 | `Bạn nói tốt đẹp về Kẻ Thù` (ch066:23, awkward Boromir line) | **CLOSED** | Naturalized to `Ngươi tô vẽ Kẻ Thù đẹp đẽ quá nhỉ` |
| Q2-015 | `sai khiến gửi Chiếc Nhẫn` (ch066:13) | **CLOSED** | Naturalized to `chọn gửi Chiếc Nhẫn` |
| Q2-016 | `mechanical_fix.py` reporting 66 false-positive changes (idempotence bug) | **CLOSED** | dry-run reports `(no changes — corpus is clean)`; stable across repeated runs |
| Q2-017 | `mechanical_fix.py` main() never wrote files | **CLOSED** | main() now calls `process_file(path)` in non-dry-run mode |
| Q2-018 | `audit_corpus.py` only counted, did not show file/line | **CLOSED** | Now lists up to 5 file:line:snippet examples per blocker |

## Open Items (Low Risk)

| ID | Area | Priority | Notes |
|---|---|---|---|
| UI-001 | Literary polish (optional) | Low | A human literary proofread can still smooth rhythm in some hybrid-history chapters. Not blocking. |
| UI-002 | Mr H. Potter in letter (ch003) | Low | Kept as English-style letter address per glossary decision. Could be "Cậu H. Potter" if a future edition wants to fully localize. |
| UI-003 | Source-intentional residue (ch062 awkward ×2, ch064 poor Harry, ch062 Tolkien's wizard) | Informational | These are author-intentional meta-references preserved as faithful translation. Not errors. |
| UI-004 | Some early chapter rhythm may benefit from manual literary pass | Low | ch001, ch003, ch005, ch010 spot-checked — all read naturally. Optional polish possible. |
| UI-005 | Mechanical script does not cover every Vietnamese fused-word pattern | Informational | New patterns may surface in future chapters. Run `scripts/sanity_check.py` after any new translation. |

## Closed Blockers (Original 9-phase plan, 2026-05-30 / 2026-06-01)

| ID | Area | Status | Evidence |
|---|---|---|---|
| CB-001 | ch066 truncated (2,897 chars) | **CLOSED** | 32,592 chars, 16 parodies present |
| CB-002 | Dementor (English) residue | **CLOSED** | 0 instances; 334 Giám ngục |
| CB-003 | Auror (English) residue | **CLOSED** | 0 instances; 306 Thần sáng |
| CB-004 | Patronus (English) residue | **CLOSED** | 0 instances; 148 Bùa hộ mệnh |
| CB-005 | Thần Sáng (wrong cap) | **CLOSED** | 0 instances |
| CB-006 | Hiệu Trưởng (wrong cap) | **CLOSED** | 0 instances |
| CB-007 | Biến Hình (wrong cap) | **CLOSED** | 0 instances |
| CB-008 | Bàn Chính (legacy) | **CLOSED** | 0 instances; 25 Bàn Trưởng |
| CB-009 | URL spacing `https: //` | **CLOSED** | 0 instances |
| CB-010 | Time spacing `7: 24` | **CLOSED** | 0 instances |
| CB-011 | Word concatenation (làkhông, córất, khôngthực) | **CLOSED** | 0 instances |
| CB-012 | Mrs Norris (English) | **CLOSED** | 1 instance → Bà Norris |
| CB-013 | `. "` / `, "` dialogue punctuation | **CLOSED** | 226 instances fixed |
| CB-014 | Mr. Potter (stray period) | **CLOSED** | 0 instances |
| CB-015 | EPUB build | **CLOSED** | 1.75 MB, 126 chapters, ZIP OK, all structure valid |

---

*All blockers from the 9-phase plan and the second QA pass are closed. The corpus
passes the new `scripts/sanity_check.py` (7/7 checks) on 2026-06-01.*
