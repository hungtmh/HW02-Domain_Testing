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

1. Chụp screenshot / screen recording
2. Ghi báo cáo Markdown trong `23127195/reports/FR-XX_bugs/`
3. Tạo **GitHub Issue** trên repo nhóm — đính kèm screenshot
4. Git commit: `test(FR-XX): report bug — [tóm tắt ngắn]`

## Template Markdown

Lưu `23127195/reports/FR-XX_bugs/BUG-NNN.md`:

```markdown
# BUG-NNN: [Tiêu đề ngắn]

## Metadata
| Field | Value |
|-------|-------|
| Feature | FR-XX |
| Severity | Critical / Major / Minor / Trivial |
| Priority | High / Medium / Low |
| Component | Web / Admin / Mobile / API |
| Test Case | DT-05 / BV-03 |
| Status | Open |

## SRS Reference
> Trích dẫn yêu cầu đúng từ README.md

## Environment
- OS: Windows 10
- Browser/App: Chrome / Expo Go
- Backend: localhost:3000

## Steps to Reproduce
1. ...
2. ...
3. ...

## Expected Result (SRS)
...

## Actual Result
...

## Evidence
![screenshot](./BUG-NNN_screenshot.png)

## Notes
- Có thể liên quan file: `frontend-web/src/pages/Login.jsx`
```

## Template GitHub Issue

**Title:** `[FR-XX] Mô tả bug ngắn`

**Body:**

```markdown
## Mô tả
...

## Liên quan SRS
FR-XX: ...

## Các bước tái hiện
1. ...
2. ...

## Kết quả mong đợi
...

## Kết quả thực tế
...

## Test case
DT-05 / BV-03

## Screenshot
(đính kèm ảnh)
```

Tạo issue bằng CLI (nếu có `gh`):

```powershell
gh issue create --title "[FR-02] Account not locked after 3 failed logins" --body-file 23127195/reports/FR-02_bugs/BUG-001.md
```

## Phân loại Severity

| Level | Tiêu chí ví dụ EShop |
|-------|----------------------|
| Critical | Bypass auth, SQLi, thanh toán sai tiền |
| Major | Lockout không hoạt động, coupon logic sai |
| Minor | Label sai ("Tổng tạm tính"), thiếu step indicator |
| Trivial | Typo, màu nút không nhất quán |

## Liên kết với test execution

Cập nhật `FR-XX_test-execution.md`:

```
| TC-ID | Expected | Actual | Status | Bug-ID |
| BV-03 | Lock 30s | No lock | FAIL | BUG-001 |
```
