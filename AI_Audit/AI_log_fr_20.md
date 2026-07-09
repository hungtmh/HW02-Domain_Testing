<!-- Append to File: AI_log.md -->

**Name of the AI tool:** Antigravity (powered by Claude Sonnet — Thinking Mode)  
**Date and time:** 2026-07-06T23:46:32+07:00  
**Your prompt:** "Analyze the Mobile App Cart & Checkout feature (FR-20). In App.js, the cart allows changing product quantity via a TextInput. The quantity input is parsed using parseInt(text, 10). If it is invalid (NaN) or <= 0, the logic forces it to parsed + 1 or defaults to 1. Apply Domain Testing and BVA focusing on the item quantity input string boundaries (negative numbers, '0', '1', decimals, large numbers, letters/special characters) and how this parsing logic behaves."  
**The AI output:** Generated Domain Testing, BVA analysis, and Test Case table (36 test cases in 7 groups A–G) for FR-20: Mobile App Cart & Checkout. Identified 6 bugs including 2 CRITICAL severity vulnerabilities: (1) off-by-one bug at App.js line 620 where `parsed + 1` is stored instead of `parsed`, causing every valid quantity edit to be inflated by 1 and corrupting cartTotal; (2) cart.slice(0, -1) at line 391 that drops the last cart item during checkout when cart has more than 1 item. Also identified HIGH severity issues: mixed-string inputs ("3abc") accepted by parseInt, decimal truncation adding +1 error, and no maximum quantity cap. Saved to FR-20_TestReport.md

---

**Name of the AI tool:** Antigravity (powered by Gemini 3.5 Flash)  
**Date and time:** 2026-07-08T21:41:00+07:00  
**Your prompt:** "Thực hiện tinh chỉnh theo skill3. Audit log không được xóa cũ, chỉ thêm mới"  
**The AI output:** "Refined EP, BVA, Test Case Design, Execution skeleton, Bug Report & Summary for FR-20 to strictly align with skills_ver3.md (v2). Converted Step 1 & 2 to structured VEC/IEC & 3-point BVA, reformatted Step 3 Test Design to 8-column format (Valid/Invalid type, no actual/severity), reformatted Step 5 Bug Report to 11-column table, added Appendix A for specifications inconsistencies and Appendix B for reserved API testing. Appended audit log to AI_log_fr_20.md."

---

**Name of the AI tool:** Antigravity (powered by Gemini 3.1 Pro)
**Date and time:** 2026-07-09T01:15:00+07:00
**Your prompt:** "Yeu cau tuong tu nhu tren" (Apply the same execution prediction updates to FR-20 based on provided actual results).
**The AI output:** Analyzed frontend-mobile/App.js and backend/server.js to verify the user's predicted actual results for FR-20 (Mobile App Cart & Checkout). Confirmed the logic matches the user's predictions: the off-by-one error (`parsed + 1`) at L620, the slice error (`cart.slice(0, -1)`) at L391, and parsing vulnerabilities with decimals/mixed strings. Inserted the user's test execution data into the Section 4 Skeleton. Tagged all UI-visible failed tests and Bugs (01 to 09) with '<mark>**[CẦN CHỤP ẢNH LỖI]**</mark>' to guide manual evidence capture. Updated test execution metrics in Section 6 (23 Designed, 13 Passed, 10 Failed, 0 Blocked).
