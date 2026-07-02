# AI Audit Report - Nguyễn Tấn Thắng Nhóm 08 mssv 23127259 - HW02

**Khai báo:** Tôi sử dụng AI tools cho các tác vụ sau trong bài HW02 Domain Testing.

**Công cụ sử dụng:** Codex / ChatGPT

---

## Interaction 001

| Field | Nội dung |
|-------|----------|
| Tool | Codex |
| Date & Time | 2026-06-26 ~21:38 |
| Feature | Homework PDF |
| Task | Đọc đề HW02 và xác định deliverables |

### Prompt

```text
Bạn hãy làm bài tập trong file này cho tôi nhé dưới tư cách là 1 sinh viên đang làm bài môn Kiểm thử phần mềm
```

### AI Output

- Đọc PDF đề bài.
- Xác định cần chọn 4 feature, làm Domain Testing, BVA, bug report, AI audit, AI critique, git log, README và zip.

### Human Review

- Kiểm tra lại đề PDF để đảm bảo không thiếu phần bắt buộc.

---

## Interaction 002

| Field | Nội dung |
|-------|----------|
| Tool | Codex |
| Date & Time | 2026-07-01 ~20:03 |
| Feature | FR-02, FR-07, FR-16, Mobile Product listing/search |
| Task | Cập nhật feature theo lựa chọn cuối cùng |

### Prompt

```text
Giờ tôi chọn các feature sau để tôi làm:
Pool A: FR-02 – Login and account lockout
Pool B: FR-07 – Shopping cart
Pool C: FR-16 – Product import from CSV
Pool D: Mobile App – Product listing/search hoặc Product detail.
```

### AI Output

- Thay Pool B sang FR-07 Shopping cart.
- Thay Pool D sang Mobile Product listing/search.
- Tạo lại report, test cases, bug report, evidence và zip theo feature mới.

### Human Review

- Chọn Mobile Product listing/search vì ít trùng với login/cart/checkout.

---

## Interaction 003

| Field | Nội dung |
|-------|----------|
| Tool | Codex |
| Date & Time | 2026-07-03 ~06:50 |
| Feature | Report format |
| Task | Làm lại thư mục `23127259` theo format mẫu `23127195` |

### Prompt

```text
Bạn làm lại thư mục 23127259 format y chang và các file cần cso như thư mục 23127195, chả qua làm cho tôi mấy này khác thôi:
Pool A: FR-02 – Login and account lockout
Pool B: FR-07 – Shopping cart
Pool C: FR-16 – Product import from CSV
Pool D: Mobile App – Product listing/search
```

### AI Output

- Đọc cấu trúc mẫu `23127195`.
- Tạo lại `23127259` với `README.md`, `install-skills.ps1`, `reports/`, `skills/`, `templates/`.
- Viết `Main_Report.md`, `Bug_Report.md`, `AI_Critique.md`, `AI_Audit_Report.md`, `git_commit_log.txt`.
- Tạo thư mục ảnh bug cho 4 feature.

### Human Review

- Rà soát lại tên feature và cấu trúc thư mục đúng với mẫu.
- Các ảnh bug hiện là placeholder, cần thay bằng screenshot thật khi tạo GitHub Issue.
