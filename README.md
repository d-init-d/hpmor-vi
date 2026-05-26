# Harry Potter và Phương pháp Tư duy Duy lý

Bản dịch tiếng Việt không chính thức của *Harry Potter and the Methods of Rationality* (HPMOR), đóng gói dưới dạng EPUB và kèm theo các artefact workflow để người đọc có thể kiểm chứng cả kết quả lẫn quy trình.

## Tải nhanh

- EPUB build sẵn: [`dist/hpmor-vi.epub`](dist/hpmor-vi.epub)
- Nội dung chương tiếng Việt: [`text/chapters/`](text/chapters/)
- Artefact workflow: [`workflow/`](workflow/)
- Script đóng EPUB: [`scripts/build_epub.py`](scripts/build_epub.py)

## Ghi công

- Nguyên tác: *Harry Potter and the Methods of Rationality* của Eliezer Yudkowsky.
- Ấn bản nguồn để đối chiếu và cấu trúc sách: [`rrthomas/hpmor`](https://github.com/rrthomas/hpmor).
- Workflow dịch: [`d-init-d/d-transcreate-skill`](https://github.com/d-init-d/d-transcreate-skill).
- Cover art gốc được ghi công cho Bogdan Butnaru theo thông tin từ HPMOR.com.

Dự án này không liên kết với J. K. Rowling, Warner Bros., Eliezer Yudkowsky, HPMOR.com hay repository nguồn.

## Trạng thái bản dịch

Bản hiện tại là **release candidate**: cấu trúc đã đủ 126 tệp chương, EPUB build sạch và có thể đọc trên các reader hỗ trợ EPUB 3. Báo cáo QA vẫn giữ caveat về việc cần đọc soát văn chương cuối cùng, vì corpus có lịch sử kết hợp giữa bản dịch đã biên tập và các phần phục hồi để bảo đảm đầy đủ.

Xem chi tiết tại [`workflow/qa-report.md`](workflow/qa-report.md).

## Tái tạo EPUB

Yêu cầu duy nhất là Python 3.10+.

```powershell
python scripts\build_epub.py --check
```

Lệnh này sẽ tạo lại:

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
|   `-- build_epub.py
|-- text/
|   `-- chapters/
|-- workflow/
|   |-- translation-brief.md
|   |-- source-map.md
|   |-- glossary.md
|   |-- glossary.csv
|   |-- style-sheet.md
|   |-- story-bible.md
|   |-- context-plan.md
|   |-- chunk-manifest.md
|   |-- subagent-dispatch-plan.md
|   |-- unresolved-issues.md
|   `-- qa-report.md
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

