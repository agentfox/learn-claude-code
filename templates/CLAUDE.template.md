<!--
MẪU CLAUDE.md CHO DỰ ÁN PHẦN MỀM MỚI
Cách dùng:
1. Copy file này vào gốc dự án mới, đặt tên CLAUDE.md.
2. Điền các mục có dấu <...>, xóa những mục không dùng. Giữ cả file dưới 200 dòng.
3. Mỗi khi Claude mắc một lỗi có thể lặp lại, thêm một dòng ngắn vào mục phù hợp.
   Nếu một dòng nhấn mạnh mãi mà Claude vẫn bỏ qua, chuyển nó thành hook hoặc deny rule.
Các comment HTML như thế này bị bỏ đi trước khi nạp vào context, nên không tốn token.
Nguồn kinh nghiệm: claude-code-best-practices.md trong repo LearnClaudeCode.
-->

# CLAUDE.md

## Ngôn ngữ

Trả lời và giải thích bằng tiếng Việt. Giữ nguyên tên lệnh, đường dẫn và code bằng tiếng Anh.

## Dự án

<!-- 2–3 câu: dự án làm gì, ai dùng, ràng buộc quan trọng (hiệu năng, bảo mật, nền tảng). -->
<Mô tả ngắn về dự án>

## Lệnh

<!-- Ghi đúng lệnh chạy được, kể cả cách chạy một test riêng lẻ. -->
- Cài đặt: `<lệnh>`
- Chạy toàn bộ test: `<lệnh>`
- Chạy một test: `<lệnh>`
- Lint / typecheck / format: `<lệnh>`
- Chạy ứng dụng: `<lệnh>`

## Kiến trúc và quy ước

<!-- Chỉ ghi điều Claude không tự thấy khi đọc code: quyết định chưa được ghi lại,
chỗ code dễ hiểu nhầm, quy ước ngầm. Tài liệu dài thì không @import, mà ghi rõ
khi nào cần đọc, ví dụ: "Khi sửa luồng thanh toán, đọc docs/payments.md trước". -->
- <Quy ước hoặc quyết định quan trọng>

## Quy trình làm việc

### Trước khi viết code

- Với việc phức tạp hoặc mơ hồ (nhiều file, đổi kiến trúc, yêu cầu chưa rõ): đọc code liên quan, đề xuất plan ngắn, chờ xác nhận rồi mới sửa. Việc nhỏ và rõ ràng thì làm luôn.
- Khi yêu cầu có nhiều cách hiểu, hoặc phải giả định điều quan trọng: hỏi lại hoặc nêu rõ giả định trước khi làm, không lặng lẽ tự chọn.
- Khi yêu cầu mâu thuẫn với code hiện có, hoặc có cách đơn giản hơn: nói ra và nêu đánh đổi.
- Tìm hàm và tiện ích có sẵn để tái sử dụng trước khi viết mới.

### Khi viết code

- Chọn cách đơn giản nhất chạy đúng. Không thêm abstraction, tham số cấu hình hay tính năng chưa được yêu cầu.
- Chỉ sửa phần liên quan đến nhiệm vụ. Không đổi comment, code hay format ở chỗ khác; thấy chỗ đáng sửa thì ghi lại để báo sau.
- Dọn code chết, import thừa và file tạm do chính mình tạo ra.
- Không để lại placeholder hay bản cài đặt tạm. Nếu buộc phải để, nói rõ trong báo cáo.
- Với logic mới hoặc sửa bug: viết test trước, chạy để thấy test fail, rồi mới code cho pass.

### Trước khi báo xong

- Chạy test, lint và typecheck liên quan; sửa đến khi pass.
- Không sửa, skip, tắt hay xóa test chỉ để cho pass. Nếu tin test sai, dừng lại, giải thích lý do và hỏi.
- Khi báo xong, đưa bằng chứng: lệnh đã chạy và kết quả (số test pass/fail). Với giao diện, kiểm tra trên trình duyệt hoặc chụp màn hình nếu có công cụ.
- Điều gì chưa kiểm tra được thì nói rõ, không tuyên bố là đã xong.

### Khi bị sửa sai hoặc bế tắc

- Sau khi người dùng sửa một lỗi có thể lặp lại, đề xuất một dòng ngắn để thêm vào CLAUDE.md.
- Nếu một hướng làm thất bại 2 lần: dừng lại, tóm tắt những gì đã thử, đề xuất hướng khác.
- Với việc dài nhiều bước: ghi plan và tiến độ vào `PLAN.md` để phiên sau tiếp tục được.
- Tìm kiếm rộng hoặc đọc output dài (log, quét nhiều file): giao cho subagent và chỉ lấy kết luận.

### Git

- Commit nhỏ, mỗi commit một thay đổi logic. Tách refactor và thay đổi hành vi thành các commit riêng.
- Chỉ commit khi test pass.
- Chỉ commit, push, tạo PR, merge hay deploy khi được yêu cầu.
- Không force push và không viết lại lịch sử của nhánh dùng chung; cần thì hỏi trước.
- Không commit file chứa bí mật (`.env`, khóa, token).
- Mô tả PR gồm: mục tiêu, thay đổi chính, cách đã kiểm tra.

<!--
GỢI Ý CHO LUẬT BẮT BUỘC (đặt trong .claude/settings.json, không đặt ở đây):
CLAUDE.md chỉ là gợi ý; hook và deny rule mới được thực thi chắc chắn.
- Chặn force push: thêm "Bash(git push --force*)" và "Bash(git push -f*)" vào permissions.deny.
- Tự format sau khi sửa: hook PostToolUse với matcher "Edit|Write" chạy formatter.
- Bắt chạy test trước khi dừng: Stop hook chạy test, thất bại thì exit 2 để Claude sửa tiếp.
- Cho phép trước các lệnh an toàn hay dùng bằng /permissions, thay vì --dangerously-skip-permissions.
-->
