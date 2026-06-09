---
name: hw02-ai-audit-report
description: >-
  Logs AI tool interactions for HW02 mandatory AI Audit Report appendix. Use when
  the user finishes an AI session, needs audit trail, or asks to document prompts
  and AI outputs for domain testing homework.
---

# AI Audit Report — HW02

## Mục đích

Bài HW02 **bắt buộc** đính kèm AI Audit Report. Mỗi lần dùng AI phải ghi log.

## File output

Append vào: `23127195/reports/AI_Audit_Report.md`

Nếu chưa có, tạo với header:

```markdown
# AI Audit Report — MSSV 23127195 — HW02

**Khai báo:** Tôi sử dụng AI tools cho các tác vụ sau trong bài HW02 Domain Testing.

**Công cụ sử dụng:** Cursor (Claude), [bổ sung nếu có ChatGPT/Gemini...]

---
```

## Mỗi interaction ghi

```markdown
## Interaction NNN

| Field | Nội dung |
|-------|----------|
| Tool | Cursor / ChatGPT / ... |
| Date & Time | 2026-06-08 14:30 |
| Feature | FR-02 Login |
| Task | Domain Testing — xác định equivalence partitions |

### Prompt (nguyên văn)

\`\`\`
[paste prompt đầy đủ]
\`\`\`

### AI Output (tóm tắt hoặc nguyên văn)

\`\`\`
[output]
\`\`\`

### Human Review
- Đã sửa: [mô tả chỉnh sửa sinh viên thực hiện]
- Đánh giá: Đúng / Sai / Thiếu — [giải thích ngắn]

---
```

## Auto-log sau mỗi session AI

Khi skill này được gọi cuối phiên làm việc, agent phải:

1. Đánh số interaction tiếp theo (NNN+1)
2. Ghi tool name = Cursor
3. Ghi datetime hiện tại
4. Trích prompt chính của user trong session
5. Tóm tắt output agent đã tạo
6. Ghi mục Human Review (để sinh viên điền hoặc agent đề xuất)

## AI Critique (200–300 từ, bắt buộc)

Lưu riêng: `23127195/reports/AI_Critique.md`

Trả lời:
- AI sai/thiếu/thiên lệch ở đâu?
- Vì sao AI miss (prompt, giới hạn tool, độ phức tạp feature)?
- Bài học khi collaborate với AI?

```markdown
# AI Critique — HW02

[200–300 từ, tiếng Việt hoặc Anh theo yêu cầu lớp]
```

## AI Gap Analysis (theo từng feature)

Ghi nhận AI Gap Analysis vào file báo cáo chính: **`23127195/reports/Main_Testing_Report.md`** tại mục:
`# FEATURE: FR-XX — [Tên]` -> `## 4. AI Gap Analysis — FR-XX`

### Cấu trúc Markdown ghi nhận:

```markdown
## 4. AI Gap Analysis — FR-XX: [Tên feature]

### 1. Những lỗi và kịch bản kiểm thử AI thông thường bỏ sót (AI Gaps)
| Kịch bản kiểm thử / Lỗi bị bỏ sót | Lý do AI bỏ sót (Root cause of AI gap) | Bài học rút ra & Giải pháp khắc phục |
|-----|-----|-----|
| ... | | |

### 2. Cách cải tiến prompt để tối ưu hóa AI
1. ...
```
