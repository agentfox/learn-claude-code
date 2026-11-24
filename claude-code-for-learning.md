# Dùng Claude Code để học và hiểu các khái niệm phức tạp

Tổng hợp từ nghiên cứu của Anthropic, tài liệu chính thức của Claude Code và kinh nghiệm của Andrej Karpathy, Addy Osmani, Simon Willison, Rob Conery cùng một số kỹ sư khác. Cập nhật 24/11/2026.

## 1. Kết luận quan trọng nhất: cách hỏi quyết định bạn có học được hay không

Tháng 1/2026, Anthropic công bố một thí nghiệm có đối chứng ngẫu nhiên với 52 kỹ sư, phần lớn là junior. Ai cũng dùng Python ít nhất hằng tuần trong hơn một năm nhưng chưa dùng thư viện Trio (lập trình bất đồng bộ) bao giờ. Mỗi người làm hai tính năng bằng Trio trong 35 phút, sau đó làm bài kiểm tra 25 phút gồm debug, đọc code, viết code và câu hỏi khái niệm. Nhóm AI có trợ lý AI ở thanh bên; trợ lý này nhìn thấy code và lúc nào cũng viết được đáp án đúng nếu được hỏi.

Kết quả:
- Nhóm dùng AI đạt trung bình **50%** ở bài kiểm tra, nhóm tự code đạt **67%** (Cohen's d = 0,738, p = 0,01). Chênh lệch lớn nhất nằm ở câu hỏi **debug**.
- Nhóm dùng AI chỉ nhanh hơn khoảng 2 phút, và mức chênh này **không có ý nghĩa thống kê** (p = 0,391).

Điểm số khác nhau nhiều theo cách dùng AI:

| Cách dùng | Số người | Thời gian | Điểm quiz |
|---|---|---|---|
| Giao hết việc viết code cho AI | 4 | 19,5 phút | 39% |
| Ban đầu tự làm, sau dần giao hết cho AI | 4 | 22 phút | 35% |
| Nhờ AI debug thay mình | 4 | 31 phút | 24% |
| **Chỉ hỏi khái niệm, rồi tự viết code** | 7 | 22 phút | 65% |
| Xin code kèm giải thích | 3 | 24 phút | 68% |
| **Sinh code xong hỏi lại cho đến khi hiểu** | 2 | 24 phút | 86% |

Hai điểm đáng chú ý:
- Nhóm "sinh code xong hỏi lại" thao tác gần giống nhóm "giao hết cho AI". Khác biệt duy nhất là họ dùng AI để **kiểm tra mình đã hiểu chưa**.
- Nhóm "chỉ hỏi khái niệm" gặp nhiều lỗi nhưng tự sửa được, và là nhóm nhanh thứ hai.

Bài viết có câu: *"Cognitive effort—and even getting painfully stuck—is likely important for fostering mastery."* Nói cách khác, phải tự nỗ lực, kể cả bị bí, thì mới thành thạo được.

**Giới hạn của nghiên cứu:**
- Các tác giả nói nghiên cứu không chứng minh quan hệ nhân quả giữa cách dùng và kết quả học.
- Mẫu nhỏ, và bài kiểm tra làm ngay sau khi code.
- Thí nghiệm không dùng Claude Code. Các tác giả dự đoán với công cụ agentic như Claude Code, tác động lên việc học còn mạnh hơn.
- Bài viết có nhắc đến chế độ Learning và Explanatory của Claude Code là công cụ "designed to foster understanding", nhưng nghiên cứu không đánh giá hai chế độ này.

## 2. Bật đúng chế độ: output style Explanatory và Learning

Claude Code có sẵn hai output style dành cho việc học:

- **Explanatory:** sau mỗi lần làm, Claude thêm khối `★ Insight` gồm 2–3 ý, giải thích vì sao chọn cách đó.
- **Learning:** cũng có Insight. Ngoài ra Claude tự làm phần việc lặp lại, còn ở chỗ có quyết định thiết kế thật thì chèn `TODO(human)` vào code, ghi Context, Your Task và Guidance, rồi **dừng lại chờ bạn tự viết**. Bạn viết xong thì Claude nhận xét bằng một Insight rồi làm tiếp.

**Cách bật:**
- `/config` → **Output style**.
- `/output-style learning`. Lệnh này cần bản v2.1.269 trở lên; một số bài viết cũ có nhắc đến nó, nhưng ở các bản giữa thì lệnh đã bị bỏ.
- Bật mặc định cho mọi dự án: đặt `"outputStyle": "Learning"` trong `~/.claude/settings.json`. Giá trị này **phân biệt hoa thường**: viết `learning` sẽ quay về Default. Lệnh `/output-style` thì không phân biệt hoa thường.
- Style mới có hiệu lực từ tin nhắn tiếp theo.

John (johnoct.com) gợi ý dùng Learning khi học framework mới, gặp quyết định kiến trúc khó, vào codebase lạ hoặc làm pair programming. Việc lặp lại mà bạn đã hiểu rõ thì dùng chế độ thường. Anh viết: *"This 'friction' is the feature, not a bug"*, nghĩa là sự chậm lại đó chính là mục đích.

**Tự tạo style riêng:**
- Đặt file `.md` trong `~/.claude/output-styles/` (dùng cho mọi dự án) hoặc `.claude/output-styles/` (một dự án).
- Frontmatter: `name`, `description`, `keep-coding-instructions`. Đặt `keep-coding-instructions: true` để giữ hướng dẫn kỹ thuật phần mềm mặc định của Claude Code.
- Phải khởi động lại Claude Code sau khi tạo hoặc sửa style.
- Ví dụ: máy này đã có style **Gia sư** ở `~/.claude/output-styles/gia-su.md`. Style này giải thích theo lớp kèm ví dụ chạy được, gợi ý dần thay vì đưa ngay đáp án bài tập, và kết thúc bằng một câu hỏi kiểm tra.
- Output style chỉ là chỉ dẫn, không bảo đảm Claude luôn làm đúng. Đặt kiến thức dự án trong CLAUDE.md, giọng điệu trong output style, còn việc bắt buộc thì dùng hook.

## 3. Quy trình học một khái niệm hoặc tài liệu khó

### Karpathy: đọc theo 3 lượt

Từ [bài trên X ngày 18/11/2025](https://x.com/karpathy/status/1990577951671509438):

> "I'm starting to get into a habit of reading everything (blogs, articles, book chapters,…) with LLMs. Usually pass 1 is manual, then pass 2 "explain/summarize", pass 3 Q&A. I usually end up with a better/deeper understanding than if I moved on."

Áp dụng với Claude Code:
1. **Tự đọc trước.** Không cho Claude giải thích ngay.
2. **Nhờ giải thích và tóm tắt.** Có thể yêu cầu nhiều cách: bằng phép so sánh, bằng ví dụ cụ thể, bằng sơ đồ Mermaid.
3. **Hỏi đáp.** Bạn hỏi chỗ chưa hiểu, rồi đảo vai để Claude hỏi lại bạn.

### Addy Osmani: chống thui chột kỹ năng

Từ bài "Avoiding Skill Atrophy in the Age of AI" (25/04/2025):
- Tự thử 15–30 phút trước khi hỏi AI, ví dụ bằng cách in log hoặc tự lần theo code. Coi AI *"as a backstop, not the first stop"*, tức là chỗ dựa cuối cùng chứ không phải nơi hỏi đầu tiên.
- Đừng tin code chỉ vì trông có vẻ đúng. Hỏi "vì sao cách này chạy được, nó có giới hạn gì?".
- Nhờ giải thích từng dòng hoặc đưa ra cách khác, để câu trả lời thụ động thành *"an active lesson"* (một bài học chủ động).
- Khi code chạy rồi, tự giải thích lại bằng lời của mình, hoặc hỏi "tại sao không làm cách khác?".
- Ghi nhật ký những lần phải nhờ AI, rồi biến chúng thành flashcard hoặc bài tập.
- Thỉnh thoảng dành một ngày không dùng AI: tự viết code từ đầu và tự đọc tài liệu.

### Simon Willison

Theo ông, chưa bao giờ học lập trình dễ như bây giờ, nhưng phải *"disciplined enough to make sure you're not outsourcing the bits you need to learn to the machines"*, tức là đủ kỷ luật để không giao cho máy những phần chính mình cần học. (Câu này lấy từ kết quả tìm kiếm về một bài nói năm 2024, chưa đối chiếu với bản gốc.)

### Rob Conery: bắt trích nguồn

- Đưa Claude URL tài liệu chính thức rồi nhờ giải thích phần mình còn thiếu.
- Bắt Claude **trích nguồn** để tự kiểm chứng, vì LLM có thể bịa: *"this one is hugely important, cite its sources"*.
- Sau đó đem điều vừa học đi trao đổi hoặc review với người thật.

## 4. Học một codebase lạ

Kinh nghiệm thực tế ở Anthropic (tài liệu "How Anthropic teams use Claude Code"):
- **Data Infrastructure:** nhân viên data science mới được hướng dẫn dùng Claude Code để tìm hiểu codebase lớn. Claude đọc CLAUDE.md, tìm file liên quan, giải thích quan hệ phụ thuộc giữa các pipeline dữ liệu và nguồn dữ liệu nào cấp cho dashboard nào.
- **Inference:** thành viên chưa có nền tảng ML nhờ Claude giải thích các hàm và tham số của model. Việc trước đây mất 1 giờ tra Google giờ còn 10–20 phút, tức giảm khoảng 80% thời gian tra cứu.

Brendan MacLean (blog Claude, 28/04/2026, 17 năm phát triển một dự án lớn):
- Mở rộng phạm vi dần dần, như khi kèm người mới: *"You wouldn't hand a new hire a 700,000-line codebase and expect results on day one."*
- *"The to-do lists and plans Claude generates don't persist across sessions. Context is what persists."* Kiến thức tích lũy nên ghi vào CLAUDE.md và quản lý như mọi file khác của dự án.

Những câu hỏi nên dùng (bật plan mode bằng Shift+Tab hai lần để Claude chỉ đọc, không sửa file):
```
Giải thích kiến trúc tổng thể của repo này, đừng sửa gì.
Request đi từ đâu đến đâu khi người dùng đăng nhập? Chỉ ra file và dòng cụ thể.
Nếu đổi chữ ký hàm X thì những gì sẽ hỏng?
Endpoint nào có sẵn nên dùng làm mẫu khi tôi viết endpoint mới?
```

## 5. Prompt mẫu để học khái niệm

```
Giải thích <khái niệm> cho người đã biết <thứ bạn biết>. Dùng một phép so sánh,
một ví dụ code nhỏ chạy được, và chỉ ra hiểu lầm phổ biến nhất.
```
```
Đừng cho đáp án. Hỏi tôi từng câu một để tôi tự suy ra.
```
```
Tôi hiểu <khái niệm> như sau: ... Chỉ ra chỗ tôi hiểu sai.
```
```
Viết một script nhỏ chứng minh <khái niệm> rồi chạy cho tôi xem kết quả.
```
```
Giải thích lại đoạn code bạn vừa viết từng dòng một, rồi hỏi tôi 3 câu để kiểm tra tôi đã hiểu chưa.
```

Prompt thứ tư tận dụng thế mạnh riêng của Claude Code là **chạy được code**. Nhờ vậy lời giải thích được kiểm chứng bằng kết quả chạy thật, không chỉ là lời nói.

## 6. Tóm tắt thành nguyên tắc

1. Dùng AI để **hiểu**, không chỉ để **ra kết quả**. Sinh code xong thì hỏi cho đến khi hiểu.
2. Tự làm hoặc tự đọc trước, hỏi sau. Bị bí một lúc là một phần của việc học.
3. Khi đang học thì bật output style Learning, hoặc style gia sư tự tạo.
4. Đòi ví dụ chạy được và nguồn để kiểm chứng.
5. Tự giải thích lại hoặc để Claude kiểm tra bạn. Nếu chưa tự giải thích được thì chưa hiểu.
6. Ghi lại điều đã học, vào CLAUDE.md hoặc sổ tay riêng.

## 7. Ghi chú về độ tin cậy

- Câu của Karpathy, nghiên cứu của Anthropic, tài liệu output styles, bài của Addy Osmani, John, Brendan MacLean và tài liệu PDF của Anthropic: đã đọc bản gốc.
- Bài của Rob Conery: chỉ đọc được phần miễn phí, phần còn lại cần trả phí.
- Câu trích của Simon Willison: lấy qua kết quả tìm kiếm, chưa đọc bài gốc.
- Bài "Three techniques to understand your codebase when coding agents write the code" trên Towards Data Science chặn truy cập tự động (HTTP 403), nên không được dùng trong bản tổng hợp này.

## 8. Nguồn

- Anthropic, [How AI assistance impacts the formation of coding skills](https://www.anthropic.com/research/AI-assistance-coding-skills) (29/01/2026) · [paper trên arXiv](https://www.arxiv.org/pdf/2601.20245)
- [Claude Code docs: Output styles](https://code.claude.com/docs/en/output-styles)
- Andrej Karpathy, [bài trên X](https://x.com/karpathy/status/1990577951671509438) (18/11/2025)
- Addy Osmani, [Avoiding Skill Atrophy in the Age of AI](https://addyo.substack.com/p/avoiding-skill-atrophy-in-the-age) (25/04/2025)
- John, [Claude Code's Output Styles: Breaking Free from AI Dependency with Learning Mode](https://johnoct.github.io/blog/2025/08/22/claude-code-output-styles-learning-mode-insights) (22/08/2025)
- Rob Conery, [Using Claude Code to Learn Something New](https://bigmachine.io/articles/ai/how-to-use-claude-code-to-learn-something-new) (21/06/2025)
- Brendan MacLean, [Onboarding Claude Code like a new developer: Lessons from 17 years of development](https://claude.com/blog/onboarding-claude-code-like-a-new-developer-lessons-from-17-years-of-development) (28/04/2026)
- Simon Willison, [loạt bài Using LLMs](https://feeds.simonwillison.net/series/using-llms/)
- Anthropic, How Anthropic teams use Claude Code (PDF)
