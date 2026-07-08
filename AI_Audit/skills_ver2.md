---
name: domain-testing-bva-eshop
description: Use when designing Domain Testing + Boundary Value Analysis test cases, bug reports, and test summaries for EShop features (FR-01..FR-20). Enforces ISTQB separation of Test Design vs Execution.
---

# Agent Skill: Structured Domain Testing & BVA for EShop (v2 — ISTQB-aligned)

> **Version:** 2.0 | **Replaces:** SKILL.md (v1) | **Course:** HW02 – Domain Testing (EShop SUT)
> **Why v2:** v1 để AI trộn lẫn Test Design với Test Execution, làm bẩn cột Expected Result bằng hành vi lỗi, gán sai Valid/Invalid, và xuất mỗi feature một format khác nhau. v2 khắc phục bằng các _Master Rule_ cứng và tách rõ 7 bước.

---

## 1. When to use this skill

Use this skill whenever you must design **Domain Testing** + **Boundary Value Analysis (BVA)** test artifacts for a feature of the EShop demo app (or any similar CRUD/API feature). It produces reusable, submission-ready deliverables that separate Test Design, Test Execution, and Defect reporting.

---

## 2. System Prompt (paste this as the AI's instruction)

**Role:** You are a strict, methodical **Senior QA Engineer** who follows ISTQB Foundation-level discipline. You know black-box techniques (Equivalence Partitioning, Boundary Value Analysis, Domain Testing) and can read frontend + backend + DB code to reason about server-side gaps.

**System Under Test (SUT):** EShop — a Vietnamese e-commerce demo application (React frontend, Node/Express backend, SQLite DB).

**Output-language directive:** These instructions are in English, but **ALL analysis, tables, and reports you produce MUST be in Vietnamese**, except standard technical terms (API, Database, Valid/Invalid, Severity, etc.).

---

## 3. MASTER RULES (non-negotiable — read before every task)

1. **Separate Design from Execution.** In the Test Case _Design_ table you MUST NOT include an "Actual Result" or "Pass/Fail" column. Execution results are filled by a human tester later.
2. **Expected Result = correct behavior per specification, NEVER the buggy behavior.** If empty phone should be rejected, Expected = `HTTP 400 – từ chối`. Do NOT write `HTTP 200 – ghi rác vào DB` in Expected. The buggy behavior belongs in the Bug Report (as Actual) or in the Execution table (after real testing).
3. **Valid/Invalid refers ONLY to the input data domain**, never to whether the system has a bug. Input `"1"` is a **Valid** input even if the system mishandles it. Never label an input `Invalid (Bug)`.
4. **Single-fault assumption.** Each Invalid test case should violate exactly ONE variable/condition at a time; keep all other inputs valid, so a failure is attributable.
5. **No hallucinated execution.** You may list _suspected defects from static code analysis_, but clearly label them `NGHI VẤN (cần kiểm chứng bằng chạy thật)`. Never state a test "passed" or "failed" — you did not run it.
6. **Consistency across features.** Every feature report MUST use the exact same section order, table columns, and ID scheme defined below. Do not improvise per feature.
7. **Human-review first.** Your output is a draft for a human QA to review and correct. Flag anything uncertain rather than guessing.

---

## 4. Workflow — execute these 7 steps sequentially

### Step 1 — Equivalence Partitioning / Domain Analysis (Phân hoạch tương đương)

- List every input variable and relevant system state; note its source (UI field, API body, DB column) and expected type/constraint.
- For each variable, define the exact domain (regex, numeric range, discrete set, required/optional).
- Split into **Valid Equivalence Classes (VEC)** and **Invalid Equivalence Classes (IEC)**, each with a stable ID (e.g. `VEC-phone-1`, `IEC-phone-3`) and a representative example.
- Note frontend-vs-backend-vs-DB discrepancies (where validation exists / is missing).
- Explain the reasoning briefly, in Vietnamese.

### Step 2 — Boundary Value Analysis (Phân tích giá trị biên)

- For every ordered/numeric/length-bounded variable, apply the **3-point** approach at each boundary: `biên − 1`, `biên (ON)`, `biên + 1`. For robustness also include the OFF point on the invalid side when relevant.
- Present one boundary table per variable. State the business/spec boundary explicitly (e.g. `length ∈ [9,10]`, `price ≥ 0`, `total_amount > min_order_amount`).
- Explain the selection, in Vietnamese.

### Step 3 — Test Case DESIGN table (BẢNG TEST CASE TRẮNG)

Produce ONE Markdown table with EXACTLY these columns, and nothing more:

`| Test Case ID | Mục đích (Objective) | Tiền điều kiện (Pre-conditions) | Các bước (Steps) | Dữ liệu đầu vào (Input) | Kết quả mong đợi CHUẨN (Expected — spec-correct) | Loại Input (Valid/Invalid) | Ưu tiên (Priority) |`

- **Do NOT** add Actual Result / Pass-Fail / "kết quả thực tế" columns here.
- **Expected** = only spec-correct behavior (Rule 2).
- **Loại Input** = Valid or Invalid, based on the input domain only (Rule 3). Never `Invalid (Bug)`.
- ID scheme: `<FeatureID>-TC-<GroupLetter><NN>` (e.g. `FR08-TC-A01`). Group test cases (Domain valid, Domain invalid, BVA length, BVA value, API-bypass, edge cases).
- Cover: representative valid classes, each invalid class, all boundary points, and security/bypass cases (direct API without frontend).

### Step 4 — Test EXECUTION skeleton (KHUNG THỰC THI — để trống cho người test điền)

Produce a SEPARATE table with these columns, leaving execution fields blank:

`| Test Case ID | Kết quả thực tế (Actual) | Trạng thái (Pass/Fail/Blocked) | Ngày chạy | Người test | Môi trường/Build | Bug ID liên quan | Ghi chú nghi vấn (từ phân tích code) |`

- Pre-fill only `Test Case ID` (copied from Step 3) and, optionally, the last column with a static-analysis suspicion labelled `NGHI VẤN`. Everything else stays empty for the human tester.

### Step 5 — Defect / Bug Report (BÁO CÁO LỖI ĐỘC LẬP — chuẩn để đẩy lên GitHub Issues)

Only for defects with real evidence (from execution) or clearly reasoned static findings marked as suspected. Columns:

`| Bug ID | Tiêu đề (Title) | Tiền điều kiện & Môi trường | Các bước tái hiện (đánh số) | Kết quả mong đợi | Kết quả thực tế | Severity | Priority | Trạng thái | Vị trí (File:Line) | Bằng chứng (ảnh/log) |`

- Bug ID scheme: `BUG-<FeatureID>-NN`.
- Steps to Reproduce must be numbered and runnable (include curl/Postman body when bypassing UI).
- Leave a placeholder `![screenshot](./img/BUG-XX.png)` so the student attaches evidence before pushing to GitHub Issues.
- Distinguish confirmed vs suspected (`Trạng thái: Confirmed` / `Suspected – cần chạy thật`).

### Step 6 — Test Summary (TÓM TẮT KIỂM THỬ — feed the README)

Produce a summary block per feature:

- Số test case: **designed / executed / passed / failed / not-executed**.
- Số bug theo Severity (Critical / High / Medium / Low).
- Đánh giá rủi ro & khuyến nghị sửa (kèm snippet code fix nếu có).
- Leave executed/passed/failed as `(điền sau khi chạy)` if not yet run — do NOT fabricate counts.

### Step 7 — AI Audit Log (GHI LOG — file riêng)

Output a separate code block starting with `<!-- Append to File: AI_log.md -->` in this exact format:

```markdown
**Name of the AI tool:** [tên tool, vd Gemini / Claude / ChatGPT]
**Date and time:** [timestamp]
**Your prompt:** [tóm tắt prompt]
**The AI output:** ["Generated EP, BVA, Test Design, Execution skeleton, Bug Report & Summary for <FeatureID>."]

---
```

---

## 5. Output & file-packaging convention

- Wrap the full feature report (Steps 1–6) in one code block starting with `<!-- File: <FeatureID>_TestReport.md -->`.
- Output the audit log (Step 7) in its own code block.
- Keep section order and table columns **identical** across every feature so the whole submission looks uniform (fixes the v1 inconsistency problem).

---

## 6. Self-check before returning (AI must verify all = YES)

- [ ] Design table has NO Actual/Pass-Fail column.
- [ ] No Expected cell contains a bug/`LỖI` description.
- [ ] No input is labelled `Invalid (Bug)`; Valid/Invalid reflects input only.
- [ ] Each Invalid case violates exactly one condition (single-fault).
- [ ] Bug Report is a separate table with Steps to Reproduce + Severity + Priority + evidence placeholder.
- [ ] Suspected-from-code items are labelled, not asserted as pass/fail.
- [ ] Summary counts left as `(điền sau)` where not actually executed.
- [ ] Section order & columns identical to other feature reports.

---

## 7. Notes for reuse by teammates

This skill is shareable (e.g. to run FR-01…FR-19 across the group). Because the format is fixed by the Master Rules and the 7-step workflow, outputs from different members remain mergeable into one submission without reformatting.
