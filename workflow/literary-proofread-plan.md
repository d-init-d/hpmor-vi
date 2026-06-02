# Literary Proofread Plan — HPMOR-VI

> **Mục đích:** Vòng "NXB-level literary proofread" toàn bộ 126 chương HPMOR tiếng Việt, sau khi bản hiện tại đã APPROVED về kỹ thuật.
> **Phạm vi:** Văn phong, nhịp câu, thoại, xưng hô, thuật ngữ (KHÔNG đổi glossary), humor timing. Không sửa regex, không chạm số liệu.
> **Ngày:** 2026-06-01
> **Trạng thái kỹ thuật đầu vào:** APPROVED (sanity_check 7/7, audit_corpus 0 blocker, mechanical_fix idempotent, build_epub OK).

---

## 1. Baseline đã xác nhận (2026-06-01, trước khi proofread)

| Lệnh | Kết quả | Ghi chú |
|---|---|---|
| `py -X utf8 scripts/mechanical_fix.py --dry-run` | no changes — corpus is clean | 1819 fused-word fixes đã apply trước đó |
| `py -X utf8 scripts/audit_corpus.py` | 0 blockers | Patronus ch051 đã dịch sang "Bùa Hộ Mệnh" |
| `py -X utf8 scripts/sanity_check.py` | 7/7 PASS | All checks green |
| `py -X utf8 scripts/build_epub.py --check` | `Built dist/hpmor-vi.epub` ✅ | OK |

**Trạng thái corpus thực tế:** ĐÃ SẠCH. 7/7 checks pass. 1819 fused-word fixes đã apply. 1 Patronus blocker đã fix.

**Kết luận baseline:** Có thể tiến hành literary polish ngay.

**Approved term counts (informational, từ audit_corpus):**
- 652 Hiệu trưởng, 306 Thần sáng, 289 Biến hình, 25 Bàn Trưởng
- 334 Giám ngục, 147 Bùa hộ mệnh, 531 Chúa tể Hắc ám
- 34 Mr Potter (preserved in formal voice — KHÔNG bulk-rewrite)

**Source-intentional residue (giữ nguyên):**
- 2 "awkward" (narrative, author's meta-commentary ch062)
- 1 "poor Harry" (Hermione's voice ch064)
- 1 "Tolkien's wizard" (author intentional ch062)
- 1 "Patronus" (book title in footnote ch051:53)

---

## 2. Glossary đã chốt (KHÔNG đổi)

| EN | VN đã chốt |
|---|---|
| Dementor | Giám ngục |
| Auror | Thần sáng |
| Patronus | Bùa hộ mệnh |
| Head Table | Bàn Trưởng |
| Headmaster | Hiệu trưởng |
| Transfiguration | Biến hình |
| Dark Lord | Chúa tể Hắc ám |
| Mrs Norris | Bà Norris |
| Madam Pomfrey/Malkin/Bones | Madam Pomfrey/Malkin/Bones (giữ nguyên) |
| Mr Potter | chỉ giữ khi speaker là Quirrell/Voldemort/formal-cold |

---

## 3. Phân chia 13 batch

| Batch | Chương | Độ ưu tiên |
|---|---|---|
| 01 | ch001-ch010 | **Cao** (first impression) |
| 02 | ch011-ch020 | **Cao** (early hook) |
| 03 | ch021-ch030 | Trung bình |
| 04 | ch031-ch040 | Trung bình |
| 05 | ch041-ch050 | Trung bình |
| 06 | ch051-ch060 | Trung bình |
| 07 | ch061-ch070 | **Cao** (ch062-ch066 narrative-heavy) |
| 08 | ch071-ch080 | Trung bình |
| 09 | ch081-ch090 | **Cao** (đã có nhiều artifact) |
| 10 | ch091-ch100 | Trung bình |
| 11 | ch101-ch110 | Trung bình |
| 12 | ch111-ch120 | **Cao** (build-up climax) |
| 13 | ch121-ch126 | **Cao** (finale) |

---

## 4. Quy trình cho mỗi batch Literary Editor

1. **Đọc toàn văn** từng chương (không chỉ scan).
2. **Phân loại lỗi văn chương**:
   - Literal English structure
   - Awkward Vietnamese rhythm
   - Dialogue unnatural
   - Repeated pronoun / repeated phrase
   - Wrong register
   - Xưng hô off
   - Humor timing weak
   - Technical reasoning unclear
3. **Sửa trực tiếp** nếu chắc chắn. **Mở source đối chiếu** nếu có nguy cơ đổi nghĩa.
4. **Báo cáo** ledger: batch, chương, số chỉnh sửa, kiểu, fidelity-check, rủi ro còn lại.

## 5. Mức sửa được phép

✅ Tách câu dài nếu giữ nghĩa
✅ Đảo trật tự câu nếu không đổi logic
✅ Thay từ cứng bằng từ tự nhiên
✅ Giảm lặp "anh ấy/cô ấy/cậu ấy" nếu rõ referent
✅ Sửa thoại cho "nói được bằng miệng"
✅ Giữ câu hơi lạ nếu đó là giọng tác giả / joke intentional
❌ KHÔNG thêm tình tiết, giải thích ngoài source
❌ KHÔNG rút gọn chương
❌ KHÔNG rewrite quá đà làm mất giọng HPMOR
❌ KHÔNG đổi thuật ngữ đã chốt
❌ KHÔNG normalize toàn bộ `Mr Potter`
❌ KHÔNG search/replace mù

---

## 6. Sau khi tất cả batch xong

- Chạy 4 lệnh verification lại
- Chạy 5-pattern independent scan (broad_fused, khong_question, space_before_punct, bad_punct_sequence, english_bleed)
- Adversarial QA: chọn ngẫu nhiên 20+ chương, đọc kỹ opening + 2 đoạn dài + kết
- Cập nhật 5 báo cáo: literary-proofread-report.md, literary-proofread-ledger.md, qa-report.md, commercial-readiness-audit.md, unresolved-issues.md

---

## 7. Acceptance

- 126/126 chương đã được literary proofread (không batch nào bỏ)
- sanity_check.py pass
- audit_corpus.py pass
- mechanical_fix.py --dry-run no changes
- EPUB build pass
- Không còn lỗi cơ học/dính chữ/dấu câu
- Không sửa đổi nào lệch nghĩa
- Báo cáo cuối ghi rõ đã đọc toàn văn, không chỉ scan
- Verdict: **APPROVED — NXB-level literary proofread completed** hoặc **NEEDS HUMAN LITERARY REVIEW**
