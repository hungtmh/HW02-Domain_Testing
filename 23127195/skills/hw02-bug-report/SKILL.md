---
name: hw02-bug-report
description: >-
  Writes structured bug reports for EShop HW02 in Markdown and GitHub Issues
  format. Use when a test fails, defect found, or user needs bug report template
  with steps to reproduce and SRS reference.
---

# Bug Report — EShop HW02

## Khi nào tạo bug report

Test **Actual ≠ Expected (theo SRS)** → bug. Ghi cả UI bug, logic bug, security bug.

## Quy trình

1. Chạy test và ghi nhận các lỗi (Defects) phát hiện được.
2. Xác định đường dẫn ảnh screenshot lỗi là `23127195/reports/FR-XX_bugs/BUG-NNN.png`. **LƯU Ý QUAN TRỌNG:** Không tự động chạy công cụ tạo ảnh hoặc sinh ảnh giả lập/tầm bậy, hãy để trống/giữ nguyên định dạng đường dẫn để sinh viên tự chụp và chèn ảnh thật vào sau.
3. Với các lỗi tầng API, ghi rõ câu lệnh chạy test (PowerShell hoặc curl) để người dùng có thể tự chạy và tái hiện lỗi.
4. Tổng hợp toàn bộ lỗi tìm được vào một file báo cáo lỗi gộp duy nhất của dự án: **`23127195/reports/Consolidated_Bug_Report.md`**.
5. **Tự động tạo GitHub Issues** trên repo nhóm cho từng bug phát hiện bằng cách chạy lệnh:
```powershell
gh issue create --repo [repo_name] --title "[FR-XX] [BUG-NNN] Title" --body-file [body_markdown_file]
```
Trong đó, file markdown thân của Issue phải chứa đường dẫn ảnh screenshot dự kiến sẽ được push lên GitHub (như `![BUG-NNN](https://raw.githubusercontent.com/[username]/[repo]/main/23127195/reports/FR-XX_bugs/BUG-NNN.png)`) để hiển thị hình ảnh tự động sau khi sinh viên chụp ảnh thật.
6. Git commit: `test(FR-XX): report bugs for [feature name]`


## Cấu trúc ghi nhận vào Consolidated_Bug_Report.md

Mở file **`Consolidated_Bug_Report.md`** và ghi nhận vào dưới phần của feature tương ứng:

```markdown
# FEATURE: FR-XX — [Tên feature]

### BUG-001: [Tiêu đề ngắn gọn]

- **Độ nghiêm trọng (Severity):** Critical / Major / Minor / Trivial
- **Độ ưu tiên (Priority):** High / Medium / Low
- **Thành phần ảnh hưởng (Component):** Web / API / DB
- **Test Case liên quan:** DT-XX / BV-XX
- **Liên quan SRS:** [Trích dẫn yêu cầu của SRS từ README.md]

#### Các bước tái hiện / Lệnh chạy test thực tế:
1. [Nếu là API, ghi rõ câu lệnh chạy, ví dụ:]
```powershell
Invoke-RestMethod -Uri "http://localhost:3000/api/..." -Method Post -ContentType "application/json" -Body '{"key":"value"}'
```
2. [Nếu là UI, ghi rõ các bước thao tác trên màn hình]

#### Kết quả mong đợi (Expected Result):
- ...

#### Kết quả thực tế (Actual Result):
- ...

#### Bằng chứng kiểm thử (Evidence / Screenshot):
- [Chèn ảnh chụp màn hình tại đây: `![BUG-001](./FR-XX_bugs/BUG-001.png)`]

#### Thông tin GitHub Issue:
- **Title:** `[FR-XX] [BUG-001] Mô tả ngắn`
- **Link Issue:** [Link GitHub Issue hoặc trạng thái Issue]

---
```

## Phân loại Severity

| Level | Tiêu chí ví dụ EShop |
|-------|----------------------|
| Critical | Bypass auth, SQLi, thanh toán sai tiền, lưu plaintext mật khẩu |
| Major | Lockout không hoạt động, trùng lặp trường bắt buộc unique, sai regex chặn nghiêm trọng |
| Minor | Trường email sai input type, label sai tên, thiếu trường xác nhận trên UI |
| Trivial | Typo chữ, nút submit sai màu sắc giao diện |
