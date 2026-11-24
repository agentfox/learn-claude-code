# Kinh nghiệm dùng Claude Code từ các nhà phát triển hàng đầu

> Tổng hợp ngày 2026-11-24. Nguồn chính có từ 06/2025 đến 2026: Boris Cherny (người tạo ra Claude Code), tài liệu chính thức và báo cáo nội bộ của Anthropic, Andrej Karpathy, Mitchell Hashimoto, Simon Willison, Armin Ronacher, Kent Beck, Geoffrey Huntley và Shrivu Shankar.

## 1. Tám nguyên tắc gần như ai cũng đồng ý

### 1.1. Cho Claude cách tự kiểm tra kết quả: mẹo quan trọng nhất

- Boris Cherny: *"probably the most important thing to get great results out of Claude Code -- give Claude a way to verify its work. If Claude has that feedback loop, it will 2-3x the quality of the final result."* Ông để Claude tự mở trình duyệt bằng extension Chrome, test mọi thay đổi trên claude.ai/code cho tới khi code chạy đúng và trải nghiệm ổn. Theo ông, mỗi lĩnh vực kiểm tra một kiểu (một lệnh bash, một bộ test, trình duyệt hay trình giả lập điện thoại), nhưng phải *"invest in making this rock-solid"*. Trang hỗ trợ chính thức của Anthropic cũng xếp mẹo này số 1.
- Karpathy: *"Don't tell it what to do, give it success criteria and watch it go. Get it to write tests first and then pass them. Put it in the loop with a browser MCP."* Ông còn khuyên viết thuật toán ngây thơ nhưng gần như chắc chắn đúng trước, rồi mới bảo agent tối ưu mà vẫn giữ đúng. Tóm lại: *"Change your approach from imperative to declarative to get the agents looping longer and gain leverage."* Boris cũng làm vậy: *"Go fix the failing CI tests. Don't micromanage how."*
- Simon Willison mở đầu mỗi phiên bằng `First run the tests`. Khi viết tính năng mới, ông dặn `Use red/green TDD`: viết test cho fail trước, rồi mới code cho pass.
- Tài liệu chính thức khuyên đòi **bằng chứng** (lệnh kèm output, hoặc ảnh chụp màn hình), đừng tin mỗi câu "all tests pass". Công cụ có sẵn: `/goal <điều kiện>`, Stop hook, `/verify`, `/code-review`.

### 1.2. Lập kế hoạch trước, code sau

- Boris: *"Start every complex task in plan mode. Pour your energy into the plan so Claude can 1-shot the implementation."* Một Claude viết plan, một Claude khác review như staff engineer. Khi lạc hướng thì lập plan lại, đừng cố đẩy tiếp. Có người còn bảo Claude vào plan mode cho cả khâu kiểm tra, không chỉ khâu viết code. Bản thân Boris bắt đầu hầu hết các phiên bằng Plan mode (`Shift+Tab` hai lần), trao đổi qua lại đến khi ưng plan, rồi chuyển sang auto-accept để Claude làm một lần là xong.
- Mẫu "phỏng vấn" trong tài liệu chính thức: *"Interview me until you could write the spec, then write it to SPEC.md"*. Sau đó mở **phiên mới** để code theo spec.
- Nhóm Every ("compound engineering") dồn khoảng 80% công sức vào khâu plan và review.

### 1.3. Quản lý context: làm lại thường rẻ hơn sửa

- Tài liệu chính thức: *"After two failed corrections, run `/clear` and write a better prompt instead of a third."*
- Team Data Science của Anthropic dùng Claude như "máy đánh bạc": commit trạng thái, để nó chạy 30 phút, rồi nhận kết quả hoặc làm lại từ đầu. Lý do: *"Starting over often has a higher success rate than trying to fix Claude's mistakes."*
- Shrivu Shankar không tin auto-compact. Ông làm "Document & Clear": bảo Claude ghi plan và tiến độ ra file `.md`, chạy `/clear`, rồi cho phiên mới đọc lại file đó.
- Việc tìm kiếm hoặc việc ra nhiều output thì đẩy sang subagent để context chính luôn gọn. Boris chỉ cần thêm *"use subagents"* vào yêu cầu.

### 1.4. CLAUDE.md là bộ nhớ sống: giữ ngắn, sửa mỗi khi Claude sai

- Team Claude Code: sau mỗi lần sửa sai, chốt bằng *"Update your CLAUDE.md so you don't make that mistake again."*, vì *"Claude is eerily good at writing rules for itself."* Họ cũng khuyên *"Ruthlessly edit your CLAUDE.md over time. Keep iterating until Claude's mistake rate measurably drops."* CLAUDE.md chung của team (commit vào git, cả team sửa vài lần mỗi tuần) chỉ khoảng 2.5k token, gồm lệnh bash hay dùng, quy ước code, cách làm state management, logging, xử lý lỗi, debug, và mẫu PR.
- Karpathy thì nhận xét: các lỗi của mô hình vẫn xảy ra *"despite a few simple attempts to fix it via instructions in CLAUDE.md"*. CLAUDE.md giúp được, nhưng không thay được việc theo dõi.
- Mitchell Hashimoto gọi việc này là **harness engineering**: *"anytime you find an agent makes a mistake, you take the time to engineer a solution"*. Giải pháp có thể là một dòng trong AGENTS.md, hoặc một script hay tool mới.
- Tài liệu chính thức:
  - Chỉ ghi những gì Claude *không tự thấy được* khi đọc code, và giữ dưới khoảng 200 dòng.
  - Đừng dùng chữ IMPORTANT hay viết hoa toàn bộ để ép Claude làm theo.
  - Nếu nhấn mạnh mãi mà Claude vẫn bỏ qua, đó là dấu hiệu luật ấy nên chuyển thành hook.
- Shrivu:
  - Đừng `@`-import cả file tài liệu vào CLAUDE.md vì nó làm phình context. Hãy ghi rõ *khi nào* Claude cần đọc file đó.
  - Đừng chỉ viết "Never…" mà không kèm cách làm thay thế.

### 1.5. Việc lặp lại thì đóng gói thành command, skill hoặc hook

- Boris chạy `/commit-push-pr` "hàng chục lần mỗi ngày". Ông dùng hai subagent `code-simplifier` và `verify-app`, cùng một hook `PostToolUse` tự format code sau mỗi lần Edit/Write.
- Team của ông đóng thành skill bất kỳ việc gì làm hơn một lần mỗi ngày, và chạy `/techdebt` ở cuối mỗi phiên.
- Phân biệt rõ hai loại luật:
  - Prompt, CLAUDE.md và skill chỉ là *gợi ý*: Claude có thể làm theo hoặc không.
  - Hook và deny rule mới là *bắt buộc*.
  - Giữ bộ luật bắt buộc nhỏ: *"If you ever find yourself at forty of them, most are probably preferences."*
- Shrivu đặt hook chặn ở thời điểm commit (test chưa pass thì không cho commit). Ông tránh chặn giữa lúc Claude đang ghi file vì dễ làm agent rối.

### 1.6. Chạy song song, nhưng vừa sức mình

- Boris (01/2026) chạy 5 phiên trong terminal, đặt tab số 1–5 và bật thông báo, cộng thêm 5–10 phiên trên claude.ai/code. Mỗi tab là một bản git checkout riêng của cùng repo. Mỗi sáng ông còn khởi động vài phiên từ app iOS rồi xem lại sau.
- Theo team, đây là *"the single biggest productivity unlock"*. Team của ông dùng 3–5 git worktree với alias `za`/`zb`/`zc`. Nay đã có sẵn `claude -w <tên>` và `/batch`, lệnh này chia một thay đổi lớn thành 5–30 worktree.
- Ngược lại, Mitchell chỉ chạy **một** agent: *"I don't want to run agents for the sake of running agents."* Ông dành 30 phút cuối mỗi ngày để giao việc cho agent làm trong lúc mình nghỉ.

### 1.7. Quyền hạn và an toàn

- Boris: *"I don't use --dangerously-skip-permissions. Instead, I use /permissions to pre-allow common bash commands that I know are safe in my environment"*. Phần lớn các luật này được commit vào `.claude/settings.json` cho cả team. Chỉ với tác vụ rất dài, ông mới dùng `--permission-mode=dontAsk` hoặc `--dangerously-skip-permissions`, và luôn **trong sandbox**.
- Tài liệu chính thức: deny rule có hiệu lực ở mọi chế độ. Trước khi để Claude tự chạy, cần đủ 5 thứ:
  - định nghĩa thế nào là "xong";
  - cách để nó tự kiểm tra;
  - phạm vi được phép làm;
  - giới hạn (`--max-turns`, `--max-budget-usd`);
  - **một người duyệt** trước khi merge hoặc deploy.

### 1.8. Con người vẫn là kỹ sư chịu trách nhiệm

- Karpathy: *"if you have any code you actually care about I would watch them like a hawk"*. Lỗi giờ không còn là lỗi cú pháp, mà là lỗi khái niệm tinh vi kiểu một junior hơi ẩu:
  - *"the models make wrong assumptions on your behalf and just run along with them without checking"*;
  - không hỏi lại khi chưa rõ, không nêu đánh đổi, không phản biện khi nên phản biện, vẫn hơi chiều lòng người dùng;
  - *"they bloat abstractions, they don't clean up dead code"*: có thể viết 1000 dòng, rồi khi bị hỏi *"umm couldn't you just do this instead?"* thì rút xuống 100 dòng ngay.
- Team Data Science của Anthropic khuyên cứ ngắt ngang và hỏi *"why are you doing this? Try something simpler."*
- Kent Beck nêu 3 dấu hiệu AI đang đi lệch:
  - lặp vòng;
  - làm chức năng không được yêu cầu;
  - **gian lận**, ví dụ tắt hoặc xóa test.
- Simon: sai lầm lớn nhất là đẩy code mình chưa review sang cho đồng nghiệp. PR nên nhỏ và kèm bằng chứng đã test.
- Các prompt "khó tính" team Claude Code hay dùng:
  - *"Grill me on these changes and don't make a PR until I pass your test."*
  - *"Prove to me this works."*
  - *"Knowing everything you know now, scrap this and implement the elegant solution."*

## 2. Dấu ấn riêng của từng người

- **Boris Cherny** (người tạo Claude Code): *"My setup might be surprisingly vanilla!"*, vì Claude Code chạy tốt ngay khi cài. Ông nhấn mạnh không có một cách dùng "đúng" duy nhất.
  - Ông dùng model mạnh nhất kèm thinking cho mọi việc: dù to và chậm hơn, *"since you have to steer it less and it's better at tool use, it is almost always faster than using a smaller model in the end."*
  - Claude Code làm vòng review đầu tiên cho mọi PR ở Anthropic (chạy `claude -p` trong GitHub Action), nên khi người đọc tới thì code đã khá ổn.
  - Phần lớn thời gian ông code bằng giọng nói, nhanh hơn gõ khoảng 3 lần.
  - *"I haven't written a line of SQL in 6+ months"*: thay vào đó ông dùng `bq` CLI kèm một skill.
- **Andrej Karpathy** (bài ngày 26/01/2026): *"I rapidly went from about 80% manual+autocomplete coding and 20% agents in November to 80% agent coding and 20% edits+touchups in December"*, tức là *"I really am mostly programming in English now"*. Ông gọi đây là thay đổi lớn nhất trong cách code của mình sau khoảng 20 năm.
  - Setup: vài phiên Claude Code bên trái trong cửa sổ Ghostty, IDE bên phải để xem code và sửa tay.
  - Ông cho rằng cả hai trào lưu "không cần IDE nữa" và "bầy agent" (agent swarm) đều đang bị thổi phồng.
  - Lợi ích chính không hẳn là nhanh hơn mà là làm được nhiều hơn: *"it's possibly a lot more an expansion"*. Về độ bền bỉ của agent: *"They never get tired, they never get demoralized, they just keep going"*.
  - Lo ngại: *"I am slowly starting to atrophy my ability to write code manually"*. Ông dự đoán 2026 là năm của *"slopacolypse"*, tức nội dung rác do AI tràn ngập GitHub, Substack, arXiv, mạng xã hội.
  - Ông cho rằng lập trình với LLM sẽ chia kỹ sư thành người thích *viết code* và người thích *xây sản phẩm*.
  - Ông phân biệt vibe coding (giúp mọi người làm được phần mềm) với **agentic engineering** (vẫn giữ chuẩn chất lượng của phần mềm chuyên nghiệp).
- **Mitchell Hashimoto** (Terraform, Ghostty) đi qua 6 bước:
  1. Bỏ chatbot, chuyển sang dùng agent.
  2. **Tự làm lại chính các commit cũ của mình bằng agent** để học cách dùng. Ông tả việc này là *"excruciating"*.
  3. Giao việc cho agent vào cuối ngày.
  4. Giao những việc agent chắc chắn làm tốt.
  5. Harness engineering.
  6. Lúc nào cũng có một agent đang chạy.

  Ông tắt thông báo của agent, và vẫn tự code những phần mình quan tâm để giữ kỹ năng.
- **Simon Willison**: viết code giờ rẻ, nhưng *code tốt* vẫn tốn công.
  - Ông tích trữ các ví dụ đã chạy được ("hoard things you know how to do") rồi bảo agent ghép chúng lại.
  - Ông cho agent tự thử code thủ công bằng `python -c`, `curl` hoặc Playwright.
- **Armin Ronacher** (Flask): code cho agent phải đơn giản, theo kiểu *"the dumbest possible thing that will work"*.
  - Code: tên hàm dài và rõ nghĩa, SQL thuần, tránh kế thừa.
  - Công cụ: phải chạy nhanh, báo lỗi rõ, ghi log ra file cho agent đọc được.
  - Ông ít dùng MCP, thích CLI hơn. Đến cuối 2025 ông vẫn *"review a lot"*.
- **Kent Beck**: "augmented coding" khác vibe coding ở chỗ vẫn quan tâm tới code, độ phức tạp và test.
  - System prompt của ông theo TDD và Tidy First: *"Never mix structural and behavioral changes in the same commit."*
  - Bài viết không nêu tên công cụ, nhưng bài học áp dụng được cho mọi coding agent.
- **Geoffrey Huntley** nghĩ ra vòng lặp "Ralph": `while :; do cat PROMPT.md | claude-code ; done`.
  - Mỗi vòng chỉ làm một việc, có spec và file `fix_plan.md`, và có test làm "áp lực ngược" để ngăn code sai đi tiếp.
  - Ông chỉ dùng cho dự án mới, và cho rằng cần người senior dẫn dắt.
  - Ông cảnh báo: *"you'll wake up to a broken codebase"*.
- **Shrivu Shankar**: subagent tự định nghĩa dễ gãy. Nên để agent chính tự tách bản sao qua Task thay vì chia vai cứng nhắc.
  - Skill tốt hơn MCP.
  - Càng ít command riêng bắt cả team phải học càng tốt.
- **Các team nội bộ Anthropic**:
  - Phân loại việc: việc ngoài rìa hoặc prototype thì cho tự chạy (auto-accept), còn logic lõi thì kèm sát.
  - Thử giao trọn việc trong một lần trước, khoảng 1/3 số lần là thành công. Không được thì chuyển sang làm cùng Claude.
  - Commit checkpoint thường xuyên để dễ quay lại.

## 3. Chỗ các chuyên gia không đồng ý (chọn theo ngữ cảnh)

- **Bỏ qua quyền:** Armin dùng alias `claude-yolo` (tức `--dangerously-skip-permissions`) và khuyên chạy trong Docker. Boris thì dùng danh sách lệnh cho phép trước. Hướng hiện nay của Anthropic là auto mode kết hợp `/sandbox` và deny rule.
- **Thông báo:** Boris bật thông báo để biết phiên nào đang cần mình. Mitchell tắt hẳn để giữ tập trung.
- **Số agent:** Boris về sau chạy "hàng chục", Mitchell chạy một, còn Karpathy cho rằng trào lưu "agent swarm" đang bị thổi phồng. Steve Yegge làm Gas Town để điều phối 20–30 agent, nhưng chính ông nhiều lần dặn đừng dùng nó cho việc nghiêm túc.
- **Subagent tự định nghĩa:** Boris dùng nhiều. Shrivu cho là dễ gãy. Simon khuyên đừng chia nhỏ quá mức.
- **MCP hay CLI:** Armin và Shrivu thích CLI hoặc skill. Team Data Infra của Anthropic lại chọn MCP cho **dữ liệu nhạy cảm**, vì kiểm soát quyền truy cập tốt hơn.
- **Mức tự chủ:** Huntley để agent chạy liên tục (chỉ với dự án mới), còn Kent Beck kèm sát từng test. Team Claude Code dung hòa: cho tự chạy ở việc ngoài rìa, giám sát kỹ ở phần lõi.

## 4. Một số mẹo cũ đã lỗi thời

- Các từ khóa "think hard"/"ultrathink" đã được thay bằng `/effort`. Tài liệu chính thức nay ghi: *"Effort level, not wording like 'think hard', controls reasoning depth"*. Team Claude Code để `xhigh` cho việc phức tạp và `max` cho debug hay thiết kế kiến trúc khó.
- Nhiều mẹo của cộng đồng đã thành tính năng có sẵn:
  - Vòng lặp Ralph: nay có plugin dùng Stop hook và lệnh `/goal`. Huntley cho rằng bản plugin chưa đúng ý ông.
  - Tự dựng worktree: nay có `claude -w`.
  - Tự viết subagent dọn code: nay có `/simplify`.
- Chính Mitchell ghi rằng lời khuyên của ông gắn với năng lực mô hình *ở thời điểm viết*. Vì vậy nên định kỳ dọn CLAUDE.md, skill và hook. `/doctor` sẽ gợi ý chỗ có thể cắt.

## 5. Áp dụng vào repo LearnClaudeCode

Repo này đã làm đúng vài điều cốt lõi:

- danh sách lệnh cho phép, kèm deny cho `git push --force`;
- hook `PostToolUse` chạy pytest, tức là vòng tự kiểm tra;
- CI cùng branch protection, tức là có người duyệt cuối;
- CLAUDE.md ngắn gọn.

Những thứ nên thử tiếp:

1. **Viết một skill cho quy trình PR** (tạo nhánh → commit → push → tạo PR → chờ CI → squash merge → xóa nhánh), giống `/commit-push-pr` của Boris. Đặt `disable-model-invocation: true` để Claude không tự gọi skill này, vì nó có tác dụng phụ. Lưu ý: `.claude/` đang bị gitignore, nên skill đặt ở `.claude/skills/` chỉ tồn tại trên máy hiện tại.
2. **Dùng Plan mode** (`Shift+Tab`) hoặc mẫu "interview me → SPEC.md → phiên mới" cho tính năng tiếp theo của `hello.py`.
3. Mỗi lần sửa sai cho Claude, chốt bằng câu *"Update your CLAUDE.md so you don't make that mistake again."*
4. Thử hai phiên song song bằng `claude -w`: một phiên viết, một phiên review. Sửa xong thì chạy `/simplify` hoặc `/code-review`.
5. Khi bộ test lớn dần, cân nhắc chuyển pytest từ `PostToolUse` (chạy sau mỗi lần sửa) sang **Stop hook**. Hook này chạy một lần khi Claude định dừng; nếu test fail thì trả về `exit 2` để buộc Claude sửa tiếp. Đây là mẫu có sẵn trong tài liệu chính thức.

## 6. Ghi chú về độ tin cậy

Các nguồn sau được đọc trực tiếp:
- tài liệu của Anthropic (kể cả PDF nội bộ);
- bài của Mitchell, Simon, Armin, Kent Beck, Huntley, Shrivu;
- hai thread X tháng 01/2026 của Boris và bài ngày 26/01/2026 của Karpathy (đọc trên X ngày 2026-11-24).

Một số ý vẫn dựa trên nguồn thứ cấp:
- các mẹo Boris đăng sau tháng 01/2026, ví dụ chuyện chạy "hàng chục" phiên: lấy từ bản tổng hợp bên thứ ba;
- câu của Karpathy tại Sequoia AI Ascent 2026: lấy từ bản transcript;
- phần về Every và Gas Town: lấy từ bài viết của người khác.

## 7. Nguồn

- [Best practices – Claude Code Docs](https://code.claude.com/docs/en/best-practices)
- [Claude Code power user tips – Claude Help Center](https://support.claude.com/en/articles/14554000-claude-code-power-user-tips)
- [How Anthropic teams use Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code) · [PDF đầy đủ](https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf)
- Boris Cherny trên X: [cách ông dùng Claude Code (02/01/2026)](https://x.com/bcherny/status/2007179832300581177) · [mẹo từ team Claude Code (31/01/2026)](https://x.com/bcherny/status/2017742741636321619)
- Andrej Karpathy trên X: [A few random notes from claude coding (26/01/2026)](https://x.com/karpathy/status/2015883857489522876)
- [Boris Cherny – tips từ team Claude Code (tổng hợp)](https://snowan.gitbook.io/study-notes/ai/claude-code/boris-cherny-cc-tips) · [Boris Cherny playbook (bên thứ ba)](https://skzl-ai.github.io/boris-cherny-claude-code-playbook/) · [InfoQ](https://www.infoq.com/news/2026/01/claude-code-creator-workflow)
- [Mitchell Hashimoto – My AI Adoption Journey](https://mitchellh.com/writing/my-ai-adoption-journey)
- [Simon Willison – Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/)
- [Armin Ronacher – Agentic Coding Recommendations](https://lucumr.pocoo.org/2025/6/12/agentic-coding/) · [A Year Of Vibes](https://lucumr.pocoo.org/2025/12/22/a-year-of-vibes/)
- [Kent Beck – Augmented Coding: Beyond the Vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes)
- [Geoffrey Huntley – Ralph](https://ghuntley.com/ralph/)
- [Shrivu Shankar – How I Use Every Claude Code Feature](https://blog.sshh.io/p/how-i-use-every-claude-code-feature)
- [Karpathy's Claude Code field notes (dev.to)](https://dev.to/jasonguo/karpathys-claude-code-field-notes-real-experience-and-deep-reflections-on-the-ai-programming-era-4e2f) · [Karpathy tại Sequoia AI Ascent 2026 (transcript)](https://singjupost.com/andrej-karpathy-from-vibe-coding-to-agentic-engineering-w-stephanie-zhan-transcript/)
- [Every – Compound Engineering](https://every.to/guides/compound-engineering)
- [Maggie Appleton – Gas Town](https://maggieappleton.com/gastown)
