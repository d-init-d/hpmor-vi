# HPMOR VI Ready-to-Ship Plan

## Mục tiêu

Hoàn thiện bản dịch tiếng Việt HPMOR trong `hpmor-vi` đến mức có thể phát hành:

- Đủ `126/126` chương.
- Không còn lỗi `critical` hoặc `major` đã xác nhận.
- Thuật ngữ nhất quán theo `workflow/glossary.md` và `workflow/style-sheet.md`.
- Văn phong tiếng Việt tự nhiên, không còn lỗi máy dịch thô dễ thấy.
- `QA Report` cuối phản ánh trung thực trạng thái bản dịch.
- EPUB/package build được nếu repo có script build.

## Bối cảnh hiện tại

- Repo đích: `hpmor-vi`.
- Source tiếng Anh: `hpmor-vn/source/chN.txt`.
- Target tiếng Việt: `hpmor-vi/text/chapters/chNNN-vn.txt`.
- Mapping: `source/ch1.txt` -> `text/chapters/ch001-vn.txt`, tương tự đến `ch126`.
- Repo GitHub: `https://github.com/d-init-d/hpmor-vi.git`.
- Local hiện cùng commit GitHub `413d086` ở phần tracked files.
- Bản dịch hiện đủ chương nhưng chưa ready-to-ship về chất lượng.
- Hiện có `47/126` file review JSON trong `workflow/review/`.
- Còn `79` chương chưa có review JSON vì workflow trước bị throttle/rate limit.

## Nguyên tắc bắt buộc

- Không chạy lại 126 agent cùng lúc. Chạy batch nhỏ `8-12` chương/lần để tránh throttle.
- Không xóa `workflow/review/*.json`; đây là bằng chứng QA.
- Không dùng `git reset --hard`, `git checkout --`, hoặc xóa thay đổi nếu không có yêu cầu rõ ràng.
- Mọi sửa lỗi dịch phải đối chiếu source tiếng Anh trước.
- Chỉ sửa lỗi `uncertain` nếu đã tự xác minh là lỗi thật.
- Không find/replace đại trà nếu thuật ngữ có thể phụ thuộc ngữ cảnh.
- Sau mỗi batch sửa, chạy grep hoặc kiểm tra cụ thể để chứng minh lỗi đã biến mất.
- Cập nhật artifact QA sau khi hoàn tất, không tuyên bố ready-to-ship nếu còn gate fail.

## Phase 0: Baseline Safety

1. Vào thư mục `hpmor-vi`.
2. Chạy `git status --short` và ghi lại trạng thái.
3. Xác nhận số file chương:
   - `text/chapters/ch001-vn.txt` đến `text/chapters/ch126-vn.txt`.
   - Kỳ vọng: `126` file.
4. Xác nhận số review JSON hiện có:
   - Kỳ vọng hiện tại: `47` file trong `workflow/review/`.
5. Tạo snapshot ngắn trong log làm việc:
   - số chương
   - số review JSON
   - số chương thiếu review
   - số findings theo severity nếu có thể tổng hợp

## Phase 1: Sửa Known Confirmed Blockers

Ưu tiên sửa các lỗi đã xác nhận còn tồn tại trong bản hiện tại.

### `ch002-vn.txt`

Source: `hpmor-vn/source/ch2.txt`

Target: `hpmor-vi/text/chapters/ch002-vn.txt`

Việc cần làm:

- Sửa `bay chổng` thành `bay chổi`.
- Sửa đoạn cuối bị cắt ở line có `xin hãy cân nhắc việc viết blog...`.
- Đối chiếu source để khôi phục đầy đủ ý: `blogging it or tweeting it` và câu `A work like this only does as much good as there are people who read it.`
- Cân nhắc dịch `logarithm` thành `logarit` nếu phù hợp.

### `ch124-vn.txt`

Source: `hpmor-vn/source/ch124.txt`

Target: `hpmor-vi/text/chapters/ch124-vn.txt`

Việc cần làm:

- Xóa câu lặp: `Và tôi không muốn ngừng làm bạn với bạn nữa.` bị lặp hai lần.
- Sửa `hack thứ gì đó ra khỏi não mình` theo nghĩa source `hacking something out of her brain`.
- Sửa các câu MT thô đã xác minh, ví dụ `rất nhiều mạnh mẽ hơn`.
- Kiểm tra nhất quán đại từ trong đoạn Draco/Harry/Nancy.

### `ch125-vn.txt`

Source: `hpmor-vn/source/ch125.txt`

Target: `hpmor-vi/text/chapters/ch125-vn.txt`

Việc cần làm:

- Dịch heading `122. Something to Protect: Severus Snape` thành `122. Điều Cần Bảo Vệ: Severus Snape` hoặc quyết định nhất quán với các heading cùng cụm.
- Sửa toàn bộ lỗi `Potions Master` bị dịch thành `Pháp sư Phòng Thí nghiệm`.
- Cách dịch đề xuất theo ngữ cảnh: `Giáo sư Độc Dược` hoặc `Bậc thầy Độc dược`, nhưng phải nhất quán với glossary.
- Sửa `Slytherin House` thành `Nhà Slytherin`.
- Sửa `Mr Potter` nếu style tiếng Việt yêu cầu Việt hóa cách xưng hô.
- Sửa `Dấu ấn Tối thượng` thành `Dấu Ấn Hắc Ám` nếu source là `Dark Mark`.
- Sửa các câu MT thô đã xác minh như `qua cái kịch cổ họng của mình`.

## Phase 2: Tổng hợp Findings Hiện Có

1. Đọc toàn bộ `workflow/review/*.json` hiện có.
2. Tạo bảng findings nội bộ theo cột:
   - chapter
   - severity
   - category
   - target excerpt
   - suggested fix
   - verdict
   - status: `open`, `fixed`, `rejected`, `needs-source-check`
3. Sửa theo thứ tự:
   - `critical` + verdict `real`
   - `major` + verdict `real`
   - `minor` + verdict `real` nếu sửa chắc chắn và ít rủi ro
   - `uncertain` chỉ sửa sau khi tự đối chiếu source
4. Sau mỗi chương đã sửa, grep lại target excerpt cũ để xác nhận lỗi không còn.

## Phase 3: Review 79 Chương Còn Thiếu

Không chạy fan-out lớn. Chia batch nhỏ để tránh throttle.

### Batch đề xuất

Batch 1:
`ch009, ch010, ch011, ch012, ch013, ch014, ch015, ch016, ch017, ch018`

Batch 2:
`ch019, ch020, ch021, ch022, ch023, ch024, ch025, ch026, ch027, ch028`

Batch 3:
`ch029, ch030, ch031, ch032, ch036, ch037, ch038, ch040, ch041, ch043`

Batch 4:
`ch045, ch048, ch049, ch051, ch052, ch057, ch058, ch059, ch060, ch061`

Batch 5:
`ch067, ch071, ch072, ch073, ch074, ch075, ch076, ch077, ch079, ch080`

Batch 6:
`ch081, ch082, ch083, ch087, ch088, ch089, ch091, ch092, ch093, ch094`

Batch 7:
`ch097, ch098, ch099, ch100, ch103, ch105, ch106, ch107, ch108, ch110`

Batch 8:
`ch111, ch112, ch114, ch116, ch118, ch119, ch120, ch123, ch126`

### Contract cho mỗi reviewer

Mỗi reviewer chỉ xử lý chương được giao:

- Đọc source EN tương ứng.
- Đọc target VI tương ứng.
- Tìm lỗi thật về:
  - omission
  - mistranslation
  - untranslated English
  - terminology inconsistency
  - duplicated text
  - broken punctuation/spacing
  - obvious machine-translation artifact
- Không báo lỗi nếu chỉ là lựa chọn văn phong hợp lệ.
- Không bịa lỗi; mọi finding phải có `source_excerpt` và `target_excerpt` nguyên văn.
- Ghi kết quả vào `workflow/review/chNNN.json`.

### JSON schema khuyến nghị

```json
{
  "chapter": 0,
  "findings": [
    {
      "category": "fidelity-omission | fidelity-distortion | terminology | untranslated-english | duplication | spelling | punctuation | mt-awkwardness | formatting",
      "severity": "critical | major | minor",
      "location": "line or approximate paragraph",
      "source_excerpt": "exact source text",
      "target_excerpt": "exact target text",
      "description": "why this is a real issue",
      "suggested_fix": "Vietnamese fix",
      "verdict": "real | uncertain"
    }
  ],
  "clean": false,
  "summary": "short chapter QA summary"
}
```

Nếu chương sạch, vẫn tạo JSON:

```json
{
  "chapter": 0,
  "findings": [],
  "clean": true,
  "summary": "No confirmed critical or major defects found in this pass."
}
```

## Phase 4: Remediation Batch-by-Batch

Sau mỗi batch review:

1. Sửa ngay các findings `critical/major` verdict `real`.
2. Đối chiếu source trước khi sửa.
3. Với mỗi file sửa, ghi lại:
   - lỗi nào đã sửa
   - line hoặc excerpt cũ
   - excerpt mới
4. Không sửa hàng loạt toàn repo nếu chưa chắc.
5. Sau khi sửa batch, chạy grep những target excerpt cũ để xác nhận biến mất.

## Phase 5: Automated Scans Cuối

Chạy các kiểm tra toàn corpus:

- Tìm từ/đoạn tiếng Anh sót bất thường.
- Tìm các lỗi đã biết:
  - `bay chổng`
  - `Pháp sư Phòng Thí nghiệm`
  - `Something to Protect`
  - `Slytherin House`
  - `hack thứ gì đó`
  - `truyềi hình`
  - `sáchHogwarts`
  - lặp câu nguyên văn rõ ràng
- Tìm spacing artifacts:
  - chữ dính nhau quanh tên thần chú
  - thiếu khoảng trắng sau dấu câu
  - HTML/XML residue nếu có
- Tìm inconsistency thuật ngữ trọng yếu:
  - `Dark Lord`
  - `Dark Mark`
  - `Death Eater`
  - `Defense Professor`
  - `Potions Master`
  - `House Slytherin/Ravenclaw/Gryffindor/Hufflepuff`

## Phase 6: QA Gates

Cập nhật `workflow/qa-report.md` theo 8 gate:

1. Completeness
2. Fidelity
3. Terminology
4. Target-Language Quality
5. Continuity
6. Numbers and Formal Data
7. Formatting
8. Residual Risk Report

Không ghi `PASS` nếu chưa có bằng chứng. Nếu còn rủi ro, ghi rõ rủi ro còn lại.

## Phase 7: Build và Package Verification

1. Xác định script build trong repo.
2. Build EPUB hoặc artifact release nếu repo hỗ trợ.
3. Xác nhận build không lỗi.
4. Nếu có output EPUB, kiểm tra file được tạo và kích thước hợp lý.
5. Không commit/push nếu user chưa yêu cầu.

## Definition of Done

Bản dịch chỉ được coi là ready-to-ship khi đạt đủ các điều kiện:

- `126/126` chương tồn tại.
- `126/126` chương có review JSON hoặc log review tương đương.
- Không còn finding `critical` verdict `real` chưa sửa.
- Không còn finding `major` verdict `real` chưa sửa, trừ khi có lý do rõ trong `unresolved-issues.md`.
- Các grep blocker trả về `0` kết quả cho lỗi đã biết.
- `workflow/qa-report.md` được cập nhật sau remediation.
- Build EPUB/package thành công.
- `git status --short` được báo lại rõ ràng để user biết file nào đã thay đổi.

## Prompt ngắn để chạy tiếp với Claude

```markdown
Đọc `hpmor-vi/workflow/ready-to-ship-plan.md` và thực hiện từ Phase 0. Không xóa review JSON hiện có. Không chạy 126 agent cùng lúc; xử lý batch nhỏ 8-12 chương. Sửa trước known confirmed blockers ở ch002, ch124, ch125, sau đó tiếp tục review 79 chương còn thiếu và remediate critical/major findings. Cập nhật QA report cuối và build verify nếu repo có script.
```
