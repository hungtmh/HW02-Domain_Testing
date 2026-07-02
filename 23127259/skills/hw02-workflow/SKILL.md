---
name: hw02-workflow
description: >-
  Orchestrates the full HW02 Domain Testing assignment workflow for EShop features.
  Use when starting HW02 work, testing a new FR feature, or when the user asks to
  complete domain testing homework step by step.
---

# HW02 Workflow — EShop Domain Testing

## Prerequisites

- Đọc SRS: `README.md` (root repo)
- Chọn 4 feature: 1 từ Pool A, B, C, D — không trùng nhóm
- Áp dụng skill `hw02-eshop-setup` nếu chưa chạy được SUT

## Workflow cho MỖI feature

Copy checklist và đánh dấu tiến độ:

```
Feature: FR-XX — [Tên]
- [ ] B1: Đọc SRS + đọc code liên quan (frontend + backend API)
- [ ] B2: Domain Testing (@hw02-domain-testing) → ghi nhận vào Main_Report.md
- [ ] B3: Boundary Value Analysis (@hw02-boundary-value-analysis) → ghi nhận vào Main_Report.md
- [ ] B4: Human review — sửa/bổ sung test case AI bỏ sót
- [ ] B5: Thực thi test trên SUT, ghi kết quả vào Main_Report.md
- [ ] B6: Bug found → @hw02-bug-report + GitHub Issue + screenshot (ghi nhận vào Bug_Report.md)
- [ ] B7: AI gap analysis → ghi nhận vào Main_Report.md
- [ ] B8: Git commit cho từng bước (design, execute, bug report...)
- [ ] B9: Ghi AI Audit log (@hw02-ai-audit-report) (AI TỰ ĐỘNG thực hiện ghi nhận)
```

## Output files (lưu vào `23127259/reports/`)

```
23127259/reports/
  Main_Report.md (Gồm Domain Testing, BVA, Test Execution, AI Gap Analysis cho tất cả feature)
  Bug_Report.md (Gồm thông tin lỗi, mã lệnh test, issue link cho tất cả feature)
```

**LƯU Ý QUAN TRỌNG KHI TEST:** 
- Mọi test case trên tầng API phải ghi rõ **câu lệnh test chạy thực tế** (ví dụ: lệnh PowerShell `Invoke-RestMethod` hoặc lệnh `curl` cụ thể kèm header/body).
- Ghi nhận chi tiết kết quả trả về thực tế từ server để sinh viên dễ dàng chạy lại kiểm chứng và chụp màn hình bằng chứng (evidence).

## Commit message convention

```
test(FR-XX): [step] — mô tả ngắn

Ví dụ:
test(FR-02): design domain test cases for login
test(FR-02): execute BVA TC-07 account lockout boundary
test(FR-02): report bugs for login feature
```

## Test summary (cho README nộp bài)

Sau khi xong các feature, tổng hợp:

| Metric | Giá trị |
|--------|---------|
| Số feature | 2 |
| Test case thiết kế | ? |
| Đã thực thi | ? |
| Pass | ? |
| Fail | ? |
| Chưa chạy | ? |
| Bug phát hiện | ? |

## AI-first nhưng có review

- Hướng dẫn AI **từng bước** theo kỹ thuật (không prompt chung chung)
- Mọi output AI phải được sinh viên review trước khi nộp
- Ghi gap analysis khi AI thiếu case hoặc sai

## Pool → component mapping

| Pool | Component | URL |
|------|-----------|-----|
| A, B | frontend-web | :5173 |
| C | frontend-admin | :5174 |
| D | frontend-mobile | IP LAN :3000 |
| All | backend | :3000 |

## Khi hoàn thành 1 feature

Nhắc sinh viên: cập nhật test summary, commit log, và chuẩn bị demo video skill.
