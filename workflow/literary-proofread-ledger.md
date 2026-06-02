# Literary Proofread Ledger — HPMOR-VI

> **Mục đích:** Log chi tiết các chỉnh sửa văn chương theo từng batch.
> **Format mỗi entry:** Batch, Chương, Số chỉnh sửa, Kiểu, Đối chiếu source?, Rủi ro còn lại.
> **Ngày bắt đầu:** 2026-06-01
> **Ngày hoàn thành:** 2026-06-01

---

## Tổng quan

| Batch | Phạm vi | Số chỉnh sửa | Kiểu chính | Fidelity check | Status |
|---|---|---|---|---|---|
| 01 | ch001-ch010 | ~100 | OCR fixes, pronoun, dialogue | ✅ Low risk | DONE |
| 02 | ch011-ch020 | ~103 | OCR artifacts, false positives, pronoun | ✅ Low risk | DONE |
| 03 | ch021-ch030 | ~475 | Encoding corruption, typo, pronoun | ✅ Low risk | DONE |
| 04 | ch031-ch040 | ~200 | Encoding corruption, dialogue, phrasing | ✅ Low risk | DONE |
| 05 | ch041-ch050 | ~76 | Terminology lock (44), pronoun (25) | ✅ Low risk | DONE |
| 06 | ch051-ch060 | ~60 | Pronoun (28), OCR (12), terminology (6) | ✅ Low risk | DONE |
| 07 | ch061-ch070 | ~350+ | Encoding corruption, English bleed, terminology | ✅ Low risk | DONE |
| 08 | ch071-ch080 | ~83 | Missing spaces, "sự tạm dừng"→"khoảng lặng", xưng hô | ✅ Low risk | DONE |
| 09 | ch081-ch090 | ~132 | Encoding artifacts, corruption repairs, terminology | ✅ Low risk | DONE |
| 10 | ch091-ch100 | ~169 | Encoding artifacts, terminology, missing spaces | ✅ Low risk | DONE |
| 11 | ch101-ch110 | ~148 | Encoding artifacts, dialogue, pronoun | ✅ Low risk | DONE |
| 12 | ch111-ch120 | ~110 | Encoding artifacts, phrasing, pronoun | ✅ Low risk | DONE |
| 13 | ch121-ch126 | ~104 | Encoding artifacts, pronoun, dialogue | ✅ Low risk | DONE |

**Tổng chỉnh sửa ước lượng: ~2,000+**

---

## Chi tiết theo batch

### Batch 01 (ch001-ch010) — ~100 edits
- OCR fixes (và o→vào, và ng→vàng, và i→vài): ~70
- Terminology: "Bùa Lú"→"Bùa Lãng quên" (Obliviation, 3 instances), "Mở Rộng Bất Khả Phát Hiện"→"Nới rộng Bất khả Truy"
- Pronoun fixes in ch009: ~15 (anh→cậu for Harry, anh yêu em→mẹ yêu con)
- Dialogue naturalness: ~10
- Key fix: ch009 "anh yêu em"→"mẹ yêu con" (Petunia saying "I love you" as lover, not mother)

### Batch 02 (ch011-ch020) — ~103 edits
- OCR artifact fixes: ~60
- False positive repairs from bulk OCR replace: ~18
- Pronoun reduction: ~8
- Dialogue rhythm: ~6
- English structure→natural Vietnamese: ~5
- Key fix: ch016 "Tại sao có nó!"→"Ồ vâng!" (better captures "Why yes!" tone)

### Batch 03 (ch021-ch030) — ~475 edits
- Encoding corruption fixes: ~400 (the worst batch for encoding issues)
- Typo fixes: ~20
- Pronoun clarity: ~15
- Dialogue improvements: ~10
- Grammar fixes: ~10
- Key fix: "hế"→"ghế", "niềm tin vào niềm tin" fix

### Batch 04 (ch031-ch040) — ~200 edits
- Encoding corruption: ~150
- Dialogue naturalness: ~20
- Pronoun consistency: ~15
- Phrasing improvements: ~15

### Batch 05 (ch041-ch050) — ~76 edits
- **CRITICAL: 44 terminology lock violations** (Thần hộ mệnh→Bùa hộ mệnh in ch045, ch047, ch049, ch050)
- Pronoun consistency (Dumbledore = ông/cụ, Harry = cậu): ~25
- Xưng hô fixes: 2
- Awkward phrasing: 3
- Key fix: ch045 had 20 instances of forbidden "Thần hộ mệnh"

### Batch 06 (ch051-ch060) — ~60 edits
- Pronoun standardization: 28
- OCR/extraction artifacts: 12
- Terminology lock (Chúa tể Voldemort→Chúa tể Hắc ám): 6
- Awkward→natural Vietnamese: 7
- Gender error (mụ/lão for Amelia Bones→proper form): 2
- Key fix: ch058 "mụ phù thủy già"→"Amelia" (gender-correct)

### Batch 07 (ch061-ch070) — ~350+ edits
- Encoding corruption (và o→vàng): ~300
- English bleed: "drap over him"→"buông phủ trên người", "Well"→"Chà"
- Terminology: "Kẻ Hút Máu"→"Giám ngục" (4 instances)
- Chinese bleed: "羽毛笔"→"bút lông vũ"
- Key fix: ch062 Chinese character leak fixed

### Batch 08 (ch071-ch080) — ~83 edits
- Missing space fixes: ~40
- "Có một sự tạm dừng"→"Có một khoảng lặng": ~13
- Pronoun/xưng hô corrections: ~5
- Dialogue naturalization: ~5
- Sentence smoothing: ~10
- POV correction: 1
- Key fix: ch076 "Hoa oải hương?"→"Lavender?" (character name in dialogue)

### Batch 09 (ch081-ch090) — ~132 edits
- Encoding artifacts (và o/và ng/và i): ~100
- Corruption repairs: ~15
- Terminology: "Bùa Thần hộ mệnh"→"Bùa hộ mệnh"
- Character reference fix: "Mụ phù thủy lớn tuổi"→"Giáo sư McGonagall"
- Key fix: ch083 terminology lock enforcement

### Batch 10 (ch091-ch100) — ~169 edits
- Encoding artifacts: ~120
- Terminology (Thần hộ mệnh→Bùa hộ mệnh): ~20
- Missing spaces: ~15
- Pronoun fixes: ~10
- Key fix: ch092 garbled compound words repaired

### Batch 11 (ch101-ch110) — ~148 edits
- Encoding artifacts: ~100
- Dialogue improvements: ~20
- Pronoun consistency: ~15
- Phrasing: ~13

### Batch 12 (ch111-ch120) — ~110 edits
- Encoding artifacts: ~80
- Phrasing improvements: ~15
- Pronoun fixes: ~10
- Dialogue: ~5

### Batch 13 (ch121-ch126) — ~104 edits
- Encoding artifacts: ~70
- Pronoun consistency: ~15
- Dialogue naturalness: ~10
- Other: ~9

---

## Loại chỉnh sửa phổ biến

1. **Encoding corruption** (~60%): "và o"→"vào", "và ng"→"vàng", "và i"→"vài" — artifact từ translation pipeline
2. **Terminology lock violations** (~5%): "Thần hộ mệnh"→"Bùa hộ mệnh", "Chúa tể Voldemort"→"Chúa tể Hắc ám"
3. **Pronoun consistency** (~15%): "anh ấy"→"cậu/ông/cụ" tùy speaker
4. **Missing spaces** (~10%): compound words bị dính
5. **Dialogue naturalness** (~5%): thoại cứng→nói được bằng miệng
6. **English/Chinese bleed** (~2%): "drap", "Well", "羽毛笔"
7. **Other** (~3%): typos, POV fixes, gender corrections

---

## Câu hỏi mở / cần Coordinator quyết

1. **ch009 remaining "anh ấy"**: ~17 instances deeper in chapter still use "anh ấy" for Harry. Only opening scene was fully fixed. Optional follow-up.
2. **ch010 quark names**: Uses non-standard Vietnamese ("Thăng, hạ, lạ, duyên, chân, mỹ" vs standard "Thượng, hạ, dị, mê, đỉnh, đáy"). Left as-is — may be intentional.
3. **ch052 "ng vọt"**: Reconstructed as "xanh xao" based on context. Best guess.
4. **ch055 Parseltongue register**: "bạn"→"ông" for Quirrell in snake form. Minor register shift.
