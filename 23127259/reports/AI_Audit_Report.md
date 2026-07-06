# AI Audit Report - Nguyễn Tấn Thắng Nhóm 08 mssv 23127259 - HW02

**Khai báo sử dụng AI:** Em sử dụng AI như một công cụ hỗ trợ trong quy trình kiểm thử phần mềm. AI được dùng để phân tích yêu cầu, xác định miền dữ liệu, gợi ý boundary values, rà soát checklist thực thi, kiểm tra cấu trúc báo cáo và nhắc các điểm cần evidence. Em không dùng AI để tự tạo kết quả kiểm thử không có căn cứ. Các actual results, ảnh/video minh chứng, mức độ nghiêm trọng và kết luận bug đều được em kiểm tra lại trước khi đưa vào bài.

**Công cụ sử dụng:** Codex / ChatGPT  
**SUT:** EShop Web Client, Web Admin, Mobile App và API Backend  
**Feature kiểm thử:** FR-02 Login and account lockout, FR-07 Shopping cart, FR-16 Product import from CSV, Mobile Product listing/search  

---

## Interaction 001 - 2026-06-26

| Field | Nội dung |
|-------|----------|
| Tool | Codex |
| Date & Time | 2026-06-26 ~21:38 |
| Phase | Requirement review |
| Task | Phân tích đề HW02 và xác định deliverables cần nộp |

### Prompt

```text
Tôi đang thực hiện HW02 môn Kiểm thử phần mềm với vai trò tester. Hãy hỗ trợ tôi đọc yêu cầu đề bài và lập checklist deliverables cần nộp. Kết quả mong muốn gồm: báo cáo chính, phần Domain Testing, phần Boundary Value Analysis, bug report kèm evidence, AI audit report, AI critique, README self-assessment, git commit log và các tài liệu hỗ trợ. Chỉ liệt kê checklist và tiêu chí kiểm tra; không viết thay kết quả kiểm thử khi chưa có evidence.
```

### AI Output tóm tắt

- Tóm tắt các tài liệu bắt buộc trong file nộp.
- Nhắc các báo cáo chính cần có cả Markdown và PDF.
- Nhắc README phải có self-assessment table và test summary.
- Nhắc bug report phải liên kết screenshot/video evidence rõ ràng.

### Human Review

- Tôi đối chiếu checklist với file đề HW02.
- Tôi dùng checklist này làm tiêu chí kiểm tra cuối, không dùng làm kết quả kiểm thử.

---

## Interaction 002 - 2026-06-27

| Field | Nội dung |
|-------|----------|
| Tool | Codex |
| Date & Time | 2026-06-27 ~22:10 |
| Phase | Test scope definition |
| Task | Chọn feature và xác định phạm vi kiểm thử |

### Prompt

```text
Tôi chọn các feature sau để làm Domain Testing: FR-02 Login and account lockout, FR-07 Shopping cart, FR-16 Product import from CSV và Mobile Product listing/search. Hãy hỗ trợ tôi như một test analyst: xác định test objectives, input variables, valid/invalid domains, boundary candidates, observable outputs và loại evidence phù hợp cho từng feature. Không kết luận bug ở bước này; chỉ chuẩn bị test conditions.
```

### AI Output tóm tắt

- Gợi ý biến kiểm thử cho login, cart, CSV import và mobile search/listing.
- Phân loại valid domain, invalid domain và edge cases.
- Nhắc expected result phải bám SRS trước khi đối chiếu actual result.
- Gợi ý cách quan sát actual result qua UI, API response, database state và source review.

### Human Review

- Tôi chốt Mobile Product listing/search là feature thuộc Pool D.
- Tôi rà lại source SUT để xác định đúng API endpoint, component UI và dữ liệu liên quan.

---

## Interaction 003 - 2026-06-28

| Field | Nội dung |
|-------|----------|
| Tool | Codex |
| Date & Time | 2026-06-28 ~14:30 |
| Phase | Test design |
| Task | Thiết kế test cases Domain Testing và Boundary Value Analysis |

### Prompt

```text
Hãy hỗ trợ tôi thiết kế test cases theo kỹ thuật Domain Testing và Boundary Value Analysis cho 4 feature đã chọn. Với mỗi test case, cần có test case ID, test condition, input/domain, expected result theo SRS, cách quan sát actual result, loại evidence cần thu thập và bug ID nếu fail. Ưu tiên các test có thể xác minh bằng UI screenshot, API response, DB state hoặc source line review.
```

### AI Output tóm tắt

- Gợi ý test cases theo nhóm valid, invalid, boundary và error handling.
- Gợi ý bảng BVA cho failed login attempts, cart quantity, CSV fields và search query.
- Nhắc phân biệt test đã thực thi, test review bằng source và test chưa chạy trực tiếp.

### Human Review

- Tôi chỉnh lại expected result theo wording của SRS.
- Tôi chỉ đánh dấu FAIL khi có actual result và evidence tương ứng.

---

## Interaction 004 - 2026-07-03

| Field | Nội dung |
|-------|----------|
| Tool | Codex |
| Date & Time | 2026-07-03 ~06:50 |
| Phase | Repository and evidence organization |
| Task | Kiểm tra cấu trúc thư mục bài nộp |

### Prompt

```text
Trong repo nhóm HW02-Domain_Testing đã có thư mục mẫu của sinh viên khác. Hãy giúp tôi kiểm tra thư mục 23127259 theo góc nhìn QA submission review: README.md, reports hoặc report files, evidence folders, skills/templates nếu cần, git_commit_log.txt và các file PDF tương ứng. Chỉ ra file rác, file trùng hoặc file không phục vụ bài nộp để tôi loại bỏ, nhưng không xóa evidence khi chưa kiểm tra link trong report.
```

### AI Output tóm tắt

- Gợi ý cấu trúc thư mục nhất quán theo format nhóm.
- Nhắc đặt evidence theo từng feature và bug ID.
- Nhắc kiểm tra link ảnh/video từ Markdown trước khi render PDF.

### Human Review

- Tôi giữ cấu trúc theo yêu cầu nộp bài và repo nhóm.
- Tôi loại các file rác/trùng sau khi chắc chắn report không còn tham chiếu đến chúng.

---

## Interaction 005 - 2026-07-04

| Field | Nội dung |
|-------|----------|
| Tool | Codex |
| Date & Time | 2026-07-04 ~20:25 |
| Phase | Test execution preparation |
| Task | Lập checklist chạy test local và thu thập evidence |

### Prompt

```text
Tôi chuẩn bị chạy test thật trên EShop local. Hãy lập checklist thực thi như một tester: service cần chạy, tài khoản test cần dùng, API cần gọi, dữ liệu test cần tạo, trạng thái DB cần kiểm tra, thao tác UI cần chụp màn hình/quay video và bước cleanup sau test. Không tạo actual result giả định; chỉ nêu cách kiểm chứng và tiêu chí pass/fail.
```

### AI Output tóm tắt

- Nhắc kiểm tra backend, web client, web admin và mobile source.
- Gợi ý dùng test data prefix để dễ cleanup.
- Nhắc lưu evidence ngay tại thời điểm actual result khác expected result.
- Nhắc kiểm DB state cho FR-02 lockout và FR-16 import.

### Human Review

- Tôi dùng checklist này khi chạy test local.
- Actual result trong report chỉ được ghi khi đã kiểm tra UI/API/DB/source.

---

## Interaction 006 - 2026-07-06

| Field | Nội dung |
|-------|----------|
| Tool | Codex |
| Date & Time | 2026-07-06 ~16:40 |
| Phase | Final QA review |
| Task | Rà soát report, evidence, PDF và package nộp bài |

### Prompt

```text
Tôi đã hoàn tất Markdown reports và evidence. Hãy hỗ trợ tôi kiểm tra như bước QA cuối trước khi nộp: mỗi bug có đủ expected, actual, severity, priority, related test case và evidence chưa; ảnh/video có link đúng chưa; PDF có render được ảnh preview của video không; README có self-assessment và test summary chưa; file Markdown nào còn thiếu PDF tương ứng không; và cấu trúc thư mục/ZIP có file trùng hoặc file rác không.
```

### AI Output tóm tắt

- Nhắc dùng preview image trong PDF cho FR-07 BUG-003 vì PDF không phát `.mov` ổn định.
- Nhắc render lại PDF sau khi chỉnh Markdown.
- Nhắc kiểm tra duplicate files bằng tên file và checksum.
- Nhắc README cần nêu rõ số feature, số test case, số bug và demo video.

### Human Review

- Tôi kiểm tra lại preview video FR-07 BUG-003 trong PDF.
- Tôi xác nhận evidence cuối cùng nằm đúng thư mục, được report tham chiếu và được liên kết từ GitHub Issues.
- Tôi cập nhật link GitHub Issues thật (#27-#42) vào bug report sau khi tạo issue trên repo nhóm.

---

## Tổng kết việc sử dụng AI

| Hạng mục | AI hỗ trợ | Tôi tự kiểm chứng |
|----------|-----------|-------------------|
| Đọc đề và lập checklist nộp bài | Có | Đối chiếu lại với file đề HW02 |
| Xác định test scope | Có | Chốt feature và phạm vi theo SRS |
| Thiết kế domain/BVA test cases | Có | Sửa expected result và boundary theo SUT |
| Chạy test và ghi actual result | Chỉ hỗ trợ checklist | Tự kiểm UI, API, DB và source |
| Viết bug report | Hỗ trợ format và review thiếu sót | Tự gắn evidence, severity và conclusion |
| Render PDF và kiểm package | Có | Tự kiểm file cuối trước khi nộp |

**Kết luận:** AI được sử dụng như công cụ hỗ trợ kiểm thử và rà soát tài liệu. Kết quả kiểm thử trong bài chỉ được giữ lại khi có bằng chứng tương ứng trong các thư mục `reports/*_bugs/`, video evidence hoặc nội dung source/API/DB đã được kiểm tra.
