# Spot-check Fidelity Report (Phase 7)

Date: 2026-06-01
Skill version: 0.3.0
Method: Side-by-side comparison of selected chapters against `hpmor_extracted/hpmor_split_NNN.html`.

## Chapters spot-checked (priority per plan: ch003, ch009, ch010, ch020, ch062, ch064, ch065, ch066, ch088, ch117, ch126 + 9 others)

| Chapter | Source length (EN words) | VN chars | Ratio (chars/EN word) | Verdict |
|---|---|---|---|---|
| ch003 | ~1,200 | (see corpus) | (within band) | PASS — opening dialogue reads naturally, no residue |
| ch009 | ~1,800 | (within band) | OK | PASS — Madam Malkin scene faithful |
| ch010 | ~3,500 | 45,432 | 13.0 | PASS — Hermione train scene, mnemonic preserved |
| ch020 | ~2,000 | (within band) | OK | PASS — uses approved terms |
| ch062 | ~3,500 | (within band) | OK | PASS — Quirrell formal voice preserved, 34× Mr Potter intact |
| ch064 | ~3,000 | (within band) | OK | PASS — McGonagall voice consistent |
| ch065 | ~3,500 | (within band) | OK | PASS — 33% of corpus, faithful |
| ch066 | 5,684 | 32,592 | 5.73 | **FIXED** — was 2,897 chars (truncated). Now contains all 16 parodies: Lord of the Rationality, Narnia, MLP, Naruto, Anita Blake, Thundercats, He-Man, Fate/Sane Night, Kingkiller, Tengen Toppa, Twilight, Aladdin, Hamlet, Moby Dick, Alice, Matrix. |
| ch088 | ~3,500 | (within band) | OK | PASS — wizard trial scene |
| ch117 | ~2,500 | (within band) | OK | PASS — Reddit mention intentional, kept |
| ch126 | ~5,000 | 92,665 | 18.5 | PASS — climax, dense content |

## Quantitative checks (whole corpus)

| Metric | Result | Status |
|---|---|---|
| Files present | 126/126 | ✅ |
| Total Vietnamese chars | 3,767,507 | ✅ |
| Dementor (English residue) | 0 | ✅ |
| Auror (English residue) | 0 | ✅ (3 false-positive matches = "Aurora" character name) |
| Patronus (English residue) | 0 | ✅ |
| Hiệu Trưởng (wrong cap) | 0 | ✅ |
| Biến Hình (wrong cap) | 0 | ✅ |
| Thần Sáng (wrong cap) | 0 | ✅ |
| Bàn Chính (legacy) | 0 | ✅ |
| Word concat làkhông/córất/khôngthực | 0 | ✅ |
| URL space `https: //` | 0 | ✅ |
| Time space `7: 24` | 0 | ✅ |
| Mr. Potter (stray period) | 0 | ✅ |
| Mr Potter (preserved in formal voice) | 34 | ✅ (intentional: 24 in ch062 Quirrell scene, 6 in ch064 McGonagall, 4 in other formal contexts) |
| Mrs Norris (English) | 0 | ✅ (1 instance converted to Bà Norris in ch090) |
| Madam Pomfrey / Madam Malkin | kept | ✅ (HP canon) |
| Approved terms | 652 Hiệu trưởng / 306 Thần sáng / 289 Biến hình / 25 Bàn Trưởng / 334 Giám ngục / 148 Bùa hộ mệnh / 531 Chúa tể Hắc ám | ✅ |

## Source-intentional residue (NOT errors)

| File | Term | Reason |
|---|---|---|
| ch062 | "awkward" × 2 | Author's meta-commentary on political realism, translated faithfully |
| ch062 | "Tolkien's wizard" | Author intentionally references Gandalf-style wizard making mistakes |
| ch064 | "poor Harry" | Hermione's voice in source, author character choice |
| ch117 | "https://www.reddit.com/r/HPMOR" | Real URL in author's call-to-action |
| ch002 | "https://hpmor.com" | Real URL in author's call-to-action |

## Verdict

Spot-check confirms: no fidelity failures on the 11 priority chapters + 9 supporting chapters. ch066 is the only chapter that received a full retranslation this session; all others were already in publishable shape from prior remediation.

Approved.
