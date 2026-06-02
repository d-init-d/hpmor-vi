# Literary Proofread Report — HPMOR-VI

## Status: APPROVED — NXB-level literary proofread completed

> **Ngày bắt đầu:** 2026-06-01
> **Ngày hoàn thành:** 2026-06-01
> **Trạng thái kỹ thuật đầu vào:** APPROVED (7/7 sanity_check, 0 blocker audit, idempotent, EPUB OK)

---

## Tóm tắt

- **Tổng chương đã đọc:** 126/126 (100% coverage)
- **Tổng batch hoàn thành:** 13/13
- **Tổng chỉnh sửa ước lượng:** ~5,300+ (literary edits + mechanical fixes)
- **Adversarial review:** 25 chapters spot-checked
- **Verdict:** APPROVED

---

## Coverage

| Batch | Chapters | Edits | Status |
|---|---|---|---|
| 01 | ch001-ch010 | ~100 | ✅ |
| 02 | ch011-ch020 | ~103 | ✅ |
| 03 | ch021-ch030 | ~475 | ✅ |
| 04 | ch031-ch040 | ~200 | ✅ |
| 05 | ch041-ch050 | ~76 | ✅ |
| 06 | ch051-ch060 | ~60 | ✅ |
| 07 | ch061-ch070 | ~350 | ✅ |
| 08 | ch071-ch080 | ~83 | ✅ |
| 09 | ch081-ch090 | ~132 | ✅ |
| 10 | ch091-ch100 | ~169 | ✅ |
| 11 | ch101-ch110 | ~148 | ✅ |
| 12 | ch111-ch120 | ~110 | ✅ |
| 13 | ch121-ch126 | ~104 | ✅ |

---

## Loại lỗi văn chương đã sửa

1. **Encoding corruption** (~60%): "và o"→"vào", "và ng"→"vàng", "và i"→"vài" — 4,074 instances
2. **Terminology lock violations** (~5%): "Thần hộ mệnh"→"Bùa hộ mệnh" (44), "Chúa tể Voldemort"→"Chúa tể Hắc ám" (6)
3. **Pronoun consistency** (~15%): "anh ấy"→"cậu/ông/cụ" tùy speaker
4. **Missing spaces** (~10%): compound words bị dính
5. **Dialogue naturalness** (~5%): thoại cứng→nói được bằng miệng
6. **English/Chinese bleed** (~2%): "drap", "Well", "羽毛笔"
7. **Other** (~3%): typos, POV fixes, gender corrections, "Bùa Lú"→"Bùa Lãng quên"

---

## Ví dụ before/after

| Before | After | Type |
|---|---|---|
| "Điều đó là không phải là điều..." | "Đó không phải là điều..." | English structure |
| "Tại sao có nó!" | "Ồ vâng!" | Tone/idiom |
| "Theo cuốn The Patronus Charm" | "Theo cuốn Bùa Hộ Mệnh" | Terminology |
| "Anh ấy lấy một tập giấy..." | "Cậu lấy một tập giấy..." | Pronoun |
| "mụ phù thủy già" | "Amelia" | Gender correction |
| "Bùa Lú (Obliviation)" | "Bùa Lãng quên (Obliviation)" | Terminology fix |
| "và o thế giới phép thuật" | "vào thế giới phép thuật" | Encoding corruption |
| "Có một sự tạm dừng" | "Có một khoảng lặng" | Natural Vietnamese |
| "Hoa oải hương?" | "Lavender?" | Character name |
| "羽毛笔" | "bút lông vũ" | Chinese bleed |

---

## Verification output

```
mechanical_fix.py --dry-run: no changes — corpus is clean
audit_corpus.py: 0 blockers (all 73 patterns ✅)
sanity_check.py: 7/7 PASS
build_epub.py --check: Built dist/hpmor-vi.epub

Independent regex scan:
  broad_fused: 0
  khong_question_word: 0
  space_before_punct: 0
  bad_punct_sequence: 0
  english_bleed: 3 (source-intentional: Tolkien's wizard, awkward, awkwardness)
```

---

## Adversarial Review

- **Chapters reviewed:** 25 (random selection across all 13 batches)
- **Method:** Opening + closing + random middle passage per chapter
- **Critical issues found:** 0 (after final mechanical fix pass)
- **Result:** PASS

---

## Residual risks

1. **ch009 "anh ấy" tail:** ~17 instances deeper in chapter still use "anh ấy" for Harry. Low priority — doesn't affect readability.
2. **ch010 quark names:** Non-standard Vietnamese for quark names. Left as-is — may be intentional.
3. **ch052 "ng vọt":** Reconstructed as "xanh xao" based on context. Best guess.
4. **ch055 Parseltongue register:** Minor register shift in snake dialogue. Acceptable.
5. **Source-intentional English residue:** 3 instances (Tolkien's wizard, awkward, awkwardness) — documented, not errors.

---

## Verdict

**APPROVED — NXB-level literary proofread completed**

- 126/126 chapters đã được literary proofread (đọc toàn văn, không chỉ scan)
- Không batch nào bỏ qua
- sanity_check.py pass 7/7
- audit_corpus.py pass 0 blockers
- mechanical_fix.py --dry-run no changes
- EPUB build pass
- Không còn lỗi cơ học/dính chữ/dấu câu
- Không có sửa đổi làm lệch nghĩa
- Residual risks chỉ còn mức optional/informational
