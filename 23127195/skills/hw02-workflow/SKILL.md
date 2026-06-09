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
- [ ] B2: Domain Testing (@hw02-domain-testing) → lưu report
- [ ] B3: Boundary Value Analysis (@hw02-boundary-value-analysis) → lưu report
- [ ] B4: Human review — sửa/bổ sung test case AI bỏ sót
- [ ] B5: Thực thi test trên SUT, ghi kết quả Pass/Fail/Not run
- [ ] B6: Bug found → @hw02-bug-report + GitHub Issue + screenshot
- [ ] B7: AI gap analysis — case/bug AI miss + lý do
- [ ] B8: Git commit cho từng bước (domain design, BVA, execute, bug fix doc...)
- [ ] B9: Ghi AI Audit log (@hw02-ai-audit-report)
```

## Output files (lưu vào `23127195/reports/`)

```
23127195/reports/
  FR-XX_domain-testing.md
  FR-XX_bva.md
  FR-XX_test-execution.md
  FR-XX_ai-gap-analysis.md
  FR-XX_bugs/
    BUG-001_screenshot.png
```

## Commit message convention

```
test(FR-XX): [step] — mô tả ngắn

Ví dụ:
test(FR-02): design domain test cases for login
test(FR-02): execute BVA TC-07 account lockout boundary
test(FR-02): report bug — lockout counter increments twice
```

## Test summary (cho README nộp bài)

Sau khi xong 4 feature, tổng hợp:

| Metric | Giá trị |
|--------|---------|
| Số feature | 4 |
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

Nhắc sinh viên: cập nhật test summary, commit log, và chuẩn bị demo video skill (nếu nộp phần Agent Skill).
