# Harry Potter và Phương pháp Tư duy Duy lý

Bản dịch tiếng Việt không chính thức của *Harry Potter and the Methods of Rationality* (HPMOR), đóng gói dưới dạng EPUB và kèm theo các artefact workflow để người đọc có thể kiểm chứng cả kết quả lẫn quy trình.

## Tải nhanh

- EPUB build sẵn: [`dist/hpmor-vi.epub`](dist/hpmor-vi.epub)
- Nội dung chương tiếng Việt: [`text/chapters/`](text/chapters/) (126 chương, ~3,77 triệu ký tự)
- Artefact workflow: [`workflow/`](workflow/)
- Script đóng EPUB: [`scripts/build_epub.py`](scripts/build_epub.py)

## Ghi công

- Nguyên tác: *Harry Potter and the Methods of Rationality* của Eliezer Yudkowsky.
- Ấn bản nguồn để đối chiếu và cấu trúc sách: [`rrthomas/hpmor`](https://github.com/rrthomas/hpmor).
- Workflow dịch: [`d-init-d/d-transcreate-skill`](https://github.com/d-init-d/d-transcreate-skill).
- Cover art gốc được ghi công cho Bogdan Butnaru theo thông tin từ HPMOR.com.

Dự án này không liên kết với J. K. Rowling, Warner Bros., Eliezer Yudkowsky, HPMOR.com hay repository nguồn.

## Trạng thái bản dịch

Bản hiện tại là **commercial-ready**: 126/126 chương đã qua literary proofread cấp NXB, toàn bộ terminology được khoá theo glossary, EPUB build sạch, và 7/7 kiểm tra sanity đều pass.

Quy trình kiểm chứng đã hoàn tất gồm:

- 9-phase remediation plan (xem [`workflow/remediation-status.md`](workflow/remediation-status.md))
- Literary proofread 13 đợt, 126/126 chương (xem [`workflow/literary-proofread-report.md`](workflow/literary-proofread-report.md))
- Adversarial review 25 chương spot-check (xem [`workflow/spot-check-report.md`](workflow/spot-check-report.md))
- Commercial readiness audit (xem [`workflow/commercial-readiness-audit.md`](workflow/commercial-readiness-audit.md))

Báo cáo QA đầy đủ: [`workflow/qa-report.md`](workflow/qa-report.md).

## Tái tạo EPUB

Yêu cầu duy nhất là Python 3.10+.

```powershell
# Build EPUB
python scripts\build_epub.py --check

# Chạy toàn bộ sanity check (7/7)
python scripts\sanity_check.py

# Kiểm tra terminology / mechanical
python scripts\audit_corpus.py
python scripts\mechanical_fix.py --dry-run
```

Lệnh `build_epub.py --check` sẽ tạo lại:

```text
dist/hpmor-vi.epub
```

`--check` thực hiện các kiểm tra cấu trúc cơ bản: file `mimetype` đúng vị trí đầu ZIP, OPF/nav/NCX parse được XML, có cover, có CSS, và số chương trong EPUB khớp với `text/chapters/`.

Nếu đã cài Calibre, có thể đọc metadata:

```powershell
ebook-meta dist\hpmor-vi.epub
```

## Cấu trúc repository

```text
.
|-- assets/
|   `-- cover.jpg
|-- dist/
|   `-- hpmor-vi.epub
|-- scripts/
|   |-- build_epub.py           # Build EPUB
|   |-- mechanical_fix.py       # Fix cơ học: dính chữ, dấu câu, terminology (idempotent)
|   |-- audit_corpus.py         # Audit 73 blocker patterns
|   `-- sanity_check.py         # Bộ 7 kiểm tra cuối (chapters, ch066, idempotency, EPUB...)
|-- text/
|   `-- chapters/
|       |-- ch001-vn.txt ... ch126-vn.txt
|       `-- translation_qa/     # Issue ledger, QA report, structural audit
|-- workflow/
|   |-- translation-brief.md
|   |-- source-map.md
|   |-- glossary.md / glossary.csv
|   |-- style-sheet.md
|   |-- story-bible.md
|   |-- context-plan.md
|   |-- chunk-manifest.md
|   |-- subagent-dispatch-plan.md
|   |-- qa-report.md / qa-report-full.md
|   |-- unresolved-issues.md
|   |-- remediation-status.md
|   |-- literary-proofread-plan.md
|   |-- literary-proofread-ledger.md
|   |-- literary-proofread-report.md
|   |-- spot-check-report.md
|   `-- commercial-readiness-audit.md
`-- NOTICE.md
```

## Workflow D Transcreate

Repository này giữ lại các artefact chính của D Transcreate để người xem không chỉ thấy kết quả EPUB, mà còn thấy cách bản dịch được quản lý:

1. Intake: [`workflow/translation-brief.md`](workflow/translation-brief.md)
2. Scan: [`workflow/source-map.md`](workflow/source-map.md)
3. Research: [`workflow/glossary.md`](workflow/glossary.md), [`workflow/style-sheet.md`](workflow/style-sheet.md), [`workflow/story-bible.md`](workflow/story-bible.md)
4. Plan: [`workflow/context-plan.md`](workflow/context-plan.md), [`workflow/chunk-manifest.md`](workflow/chunk-manifest.md)
5. Coordinate: [`workflow/subagent-dispatch-plan.md`](workflow/subagent-dispatch-plan.md)
6. QA: [`workflow/qa-report.md`](workflow/qa-report.md), [`workflow/unresolved-issues.md`](workflow/unresolved-issues.md)

Các thư mục backup, corpus recovery thô, tệp `_parts`, script sửa tạm và source EPUB tiếng Anh không được đưa vào repo để giữ repository sạch. Nếu cần đối chiếu nguồn, hãy dùng repository gốc [`rrthomas/hpmor`](https://github.com/rrthomas/hpmor).

## Phạm vi pháp lý

Repository này không tuyên bố license mở cho nguyên tác HPMOR, nhân vật Harry Potter, cover art, hay bất kỳ tài sản phái sinh nào không thuộc quyền cấp phép của maintainer repo này. Xem [`NOTICE.md`](NOTICE.md) để biết thông tin ghi công và giới hạn sử dụng.
