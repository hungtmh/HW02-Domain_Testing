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
2. Với các lỗi tầng API, ghi rõ câu lệnh chạy test (PowerShell hoặc curl) để người dùng có thể tự chạy và tái hiện lỗi.
3. Tổng hợp toàn bộ lỗi tìm được vào một file duy nhất: `23127195/reports/FR-XX_bug-report.md`.
4. Tạo **GitHub Issues** trên repo nhóm cho từng bug phát hiện được.
5. Git commit: `test(FR-XX): report bugs for [feature name]`

## Template Markdown báo cáo gộp

Lưu vào file duy nhất `23127195/reports/FR-XX_bug-report.md`:

```markdown
# Consolidated Bug Report — FR-XX: [Tên feature]

**MSSV:** 23127195  
**SUT:** [Frontend Web / API / Admin]

## Tổng hợp danh sách lỗi phát hiện (Bypass & UI Bugs)

---

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

## Tạo Issue bằng CLI (nếu có `gh`)

```powershell
gh issue create --title "[FR-XX] [BUG-001] Short description" --body "Mô tả lỗi, các bước tái hiện và kết quả thực tế..."
```
