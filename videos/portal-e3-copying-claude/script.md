# 项目周记 E3 · Copying Claude's chat page — script & visual plan

Series: *项目周记* (`docs/PORTAL_SERIES.md`). Watch after E2. Brief: `BRIEF.md`; every claim's source:
`SOURCES.md`.

Audience: Conny, after E1–E2. Goal: he can name the parts of a chat page, say what decision 0006
decided and why, sort the page into copied / not copied / added, retell how PR #41 built it, and
name what mainstream apps have that we don't and what only this product could do.

**Narrated.** SAY lines are spoken (Kokoro `af_heart`, 0.95×, over a quiet music bed) and shown as
subtitles (Chinese above, English below). Chinese UI strings are shown, never read.

Colours: the page itself in its own light palette (cream `#FAF9F5`, white input, beige bubble
`#F0EEE6`, ink `#141413`, terracotta `#C96442`) on the dark canvas · names and callouts YELLOW ·
our code BLUE · copied GREEN tick · not copied RED cross · added for safety RED outline · Claude's app
a GREY outline only (no logo, no name styling).

---

## S01 · Copied, on purpose — `s01_hook.py` · `Hook`

SHOW: The empty triage page redrawn in cream: serif 「哪里不舒服？」, the composer in the middle with its placeholder 「说说哪里不舒服，比如：喉咙很痛，发烧两天了」, the demo chips under it, the fine print. Beside it, a GREY outline of the same layout labelled "Claude's app (outline)"; matching lines connect greeting to greeting, box to box.
SAY: Before you type, our triage page shows a serif greeting asking where it hurts, an input box in the middle of the screen, and a row of suggestions under it. If that reminds you of Claude's app, it should. You asked for a one-to-one copy, and the agent built it.

SHOW: The word "copy" in YELLOW with a question mark; four chips appear: copied · not copied · added · not built yet.
SAY: Isn't copying exactly what a product should avoid? Here it was the plan. What was copied, what was refused, what we added, and what nobody has built yet: that is this episode.

---

## S02 · The parts of a chat page — `s02_anatomy.py` · `Anatomy`

SHOW: The empty page again, larger. YELLOW callouts name each part as it is said: empty state · suggestion chips · composer · model menu · send key (it morphs into the stop key). A small source tag per name (NN/g, Material, chat-UI kits; SOURCES.md).
SAY: First, the parts. Almost every chat app has the same ones, and designers have names for them. The empty state is the page before the first message. Suggestion chips are ready-made questions; ours start demo replays. The composer is the input box. Inside it sit a model menu and the send key, which turns into a stop key while you wait.

SHOW: The page fills with one turn: a live turn: a beige bubble on the right with demo 01's first message 「喉咙痛两天了，吞东西的时候特别疼，今天量了体温38.5度」, the thinking row, an answer in serif without a frame, the action row 「复制 · 复制给家长 · 重新回答」, the round scroll-to-bottom button (its tooltip: 「回到最新」), the fine print 「AI 生成，不是诊断 · 只用虚构情况，别输入真实病情 · 危及生命直接打 911」. Callouts: user bubble · answer column · action row · scroll-to-bottom · disclaimer line.
SAY: Once you send, your words sit in a bubble on the right, and the answer runs full width without a box. Under each answer is an action row: copy, and under the latest one, retry. Scroll up, and a round button appears to take you back to the bottom. And under the input, one line of fine print: the disclaimer.

---

## S03 · Why copy? — `s03_decision.py` · `Decision`

SHOW: Decision 0006's title 「0006：界面先朴素，每个界面只照抄一个参考；分诊聊天页照 Claude App 做」, owner Junyi, status 提议; issue #40 (01:45, before 0006): 「照着一个固定的参考（Claude App 的聊天界面）一比一地做，不混搭别的风格」. Three option cards: 1 our own style · 2 the best parts of several · 3 one mature reference, copied exactly.
SAY: The team has no designer. You asked for the page to follow Claude's chat, one to one, and that night the agent wrote the reasons down as decision six, against two other options. Invent our own style: without references, probably ordinary, and likely to be redone. Take the best parts of several apps. Or copy one mature app exactly, with no mixing.

SHOW: Pause-and-ponder card.
SAY: Before the answer: why would copying one product beat picking the best parts of several?

SHOW: Option 2 as a collage: three page fragments with different spacing, corner radii and button colours; the seams flash RED. 0006's line: 「风格容易打架，也说不清每个决定从哪来」. Then option 3: one reference, every small question answered the same way; 0006's reason: 「能用最少的设计判断得到一个不难看、不出错的结果」. Jakob's law, quoted from NN/g. A GREEN tick on option 3; the rule 「每个界面只照抄一个参考」 and the design doc's heading 「分诊聊天页 ← Claude App」.
SAY: Because parts from different products disagree: spacing, colours, how a button behaves. The seams show, and the decision record names a second cost: you can no longer say where each choice came from. One mature reference answers every small question the same way, so the fewest design calls give a page that is neither ugly nor wrong. It also helps the people using it. Designers call it Jakob's law: users spend most of their time on other sites, so they prefer yours to work the same way. The rule, now written down: every screen copies exactly one reference. For the chat page, that is Claude's app, which everyone on the team uses every day.

---

## S04 · What was copied — `s04_copied.py` · `Copied`

SHOW: One turn on the page, with GREEN ticks: one column at most 768 px; user bubble right, beige, rounded; answer serif, full width, no frame.
SAY: Here is what was copied. One column, at most 768 pixels wide. Your message in a beige bubble on the right. The answer in serif type, full width, no frame.

SHOW: The composer enlarged: it grows with the text; three pills inside 「谁在问」「保险」「在哪里」; 「Terra · 中 ⌄」; the terracotta send key.
SAY: The composer: a white rounded box that grows as you type. Along its bottom edge, three small drop-downs: who is asking, insurance, and where you are. On the right, the model menu, Terra at medium effort, next to the terracotta send key, the same spot where Claude's help page puts its own model menu.

SHOW: The colour table (light / dark) as swatches: 页面底色 #FAF9F5 / #262624 · 输入框 #FFFFFF / #30302E · 用户气泡 #F0EEE6 / #141413 · 正文 #141413 / #FAF9F5 · 主色 #C96442 / #D97757; fonts: 思源宋体 for the greeting and answer, 思源黑体 for the rest. A boundary around the chat page only, labelled `.chat-page`; the rest of the site in the neutral theme. Quote 0006: 「Junyi 选了后者（2026-10-28）」.
SAY: Two choices here were yours: copy Claude's chat page at all, and copy its warm colours and serif type too, not only the layout. They stay inside this one page; the rest of the site keeps its neutral theme.

---

## S05 · What was not copied — `s05_refused.py` · `Refused`

SHOW: Four RED-crossed cards with their reasons: logo, name, private fonts → a small dot, open fonts · sidebar, history, attachments, tools → no accounts, no storage · raw reasoning → E2 · word-by-word streaming → E2.
SAY: What was not copied, each for a reason. Claude's logo, name and private fonts: they aren't ours, so a small dot means thinking and the fonts are open ones. The sidebar, chat history, attachments and tools: we have no accounts and no storage, and the prototype doesn't need them. And the two from episode two: the raw reasoning, and words streaming as they are written. Our answers pass the checker first.

---

## S06 · What we added — `s06_added.py` · `Added`

SHOW: Pause-and-ponder card. A map: the student in Boston, the parent in China.
SAY: Now a harder question. A parent in China opens this page about their child in Boston. What do they need that the student doesn't?

SHOW: The fine print in two versions, student 「危及生命直接打 911」, parent 「危及生命请孩子或身边的人在当地打 911」. A phone number, student 「617-…」 with a dial link; parent 「+1 617-…（从中国拨打）」, still a dial link; 911 for a parent: 「（请孩子或身边的人在当地拨打）」, no link.
SAY: Start with 911. A parent can't dial it from China. So every fixed line on the page changes for parents: instead of call 911, it asks the child or someone nearby to call 911 locally. Phone numbers get a plus one and the words dial from China. Emergency and crisis numbers get no dial link at all, only: ask someone there to call.

SHOW: Added for everyone, each with a RED outline: the red 「现在就做」 block first, at once, role=alert; the top bar's 「紧急情况」; 「模拟」 tags; for students: 「复制给家长」 with the label it appends 「（AI 分诊原型生成，不是诊断；模拟）」.
SAY: Some additions are for everyone. In an emergency, a red do-this-now block comes first, appears at once, and is read aloud by screen readers. An emergency link sits in the top bar at all times. Demos and estimates are labelled simulated, and when a student copies an answer for a parent, the label goes with it: not a diagnosis.

SHOW: Accessibility: hidden headings 「你说」「回答」「回答（紧急）」 a screen reader can jump between; the receipt's source links one per line, each at least 24 px tall; the page zoomed to 400 %: it opens at the top, with 「紧急情况」 in view.
SAY: And some are for people who use the page differently: hidden headings a screen reader can jump between, source links at least 24 pixels tall so a finger can hit them, and at 400 percent zoom, a page that opens at the top with the emergency link in view.

---

## S07 · How it was built — `s07_built.py` · `Built`

SHOW: A time axis, Wednesday 2026-10-28, Boston time: 01:45 issue #40 · 01:59 decision 0006 recorded · 02:16 the rebuilt page committed (27 files) · 02:22 end-to-end tests (41 checks).
SAY: How did the agent build it? On Wednesday at one fifty-nine in the morning, Boston time, it wrote the decision down. Seventeen minutes later it committed the rebuilt page: 27 files. Six minutes after that, end-to-end tests.

SHOW: The day on an axis, as bands of the commits that landed each round's fixes: 10:02–10:14 independent visual review · 10:40–11:04 streaming and the model menu (your request) · 11:35–12:06 the streaming review · 11:23–15:21 the second visual review (phone layout, parent wording, accessibility) · 16:52–19:16 the final review from five angles (安全和状态 · 流式后端 · 排版和无障碍 · 文案和文档 · 测试和检查规则), 36 findings, about 30 unique, fixed on four parallel branches, then a re-review that found 8 more.
SAY: Then came the reviews. An independent visual review. The streaming you had asked for, and a review of it. A second visual review, which brought Claude's phone layout and much of the parent wording and accessibility you just saw. And a final review from five angles, which found about 30 problems, fixed on parallel branches and then checked once more.

SHOW: The send key morphing into the stop key and back. Bug 1: click stop → the wait ends → the same click lands on the send key → whatever is in the box is sent (in a demo replay, the message just stopped). Fix: one line (26b85e0). Bug 2 (Bugbot, Medium): double-click send → the second click lands on stop → 「已停止」. Fix: ignore the second click of a double-click (f95aa77).
SAY: One bug shows why this is hard. Send and stop share one button: while you wait, send turns into stop. Click stop, the wait ends, and in that same click the button turns back into send, so whatever was in the box went out. In a demo replay, that was the very message you had just stopped. The fix was one line. Then Bugbot found the mirror image: double-click send, and the second click lands on stop. Another one-line fix: ignore the second click of a double-click.

---

## S08 · What else — `s08_next.py` · `Next`

SHOW: GREY chips for what mainstream apps have and we don't, each with its source (Claude help centre, OpenAI; as of 2026-10-30): chat history and projects · file uploads · voice · a side panel for documents and code (Artifacts, 2024; canvas, 2024) · memory across chats. Under most of them: "needs accounts and storage".
SAY: What do the big chat apps have that we don't? Conversation history and projects, file uploads, voice, a side panel for documents and code, and memory across chats. Most of them need accounts and storage, which this prototype doesn't have.

SHOW: YELLOW idea cards: one answer for two readers, student and parent side by side (the folded 「给家长的摘要」 is the seed) · a summary card the student sends home (「复制给家长」 is the first step) · a hand-off to booking (the answer already writes the English to say, 「可以这样说」).
SAY: And what could only we build? One answer for two readers, the student's and the parent's, side by side; the folded parent summary is the seed. A summary card the student sends home; copy for parent is already a first step. And a hand-off to booking: the answer already writes the English sentences to say; the page could place the call, or fill in the form.

SHOW: Under 「等你决定」 (12 items in PR #41's handoff): decision 0006 and its addendum 「提议」 (progress-only streaming, the model menu, retry) · a stopped message is sent with your next one · parents get no dial link for crisis lines.
SAY: And what waits for you: a dozen open items. Decision six is still a proposal, and so is its addendum: progress-only streaming, the model menu and retry. Two more choices the agent made unattended need your yes: a stopped message now goes out with your next one, and parents get no dial link for crisis lines.

---

## S09 · Recap — `s09_recap.py` · `Recap`

SHOW: Three columns fill: copied (layout, composer, colours, this page only) · not copied (logo, history, raw thoughts, word-by-word) · added (emergency first, parent wording, labels that travel, accessibility).
SAY: So: one reference per screen, copied exactly, so every small choice has an answer and the page feels familiar. Claude's layout, composer and colours, kept to this page. Not its logo, its history, its raw thoughts or its word-by-word streaming. Plus what only a medical page for two audiences needs: emergency first, wording a parent in China can act on, and labels that travel with copied text.

SHOW: Three test-yourself questions.
SAY: Three questions. Why copy one product instead of several? Why does the parent's page ask someone else to call 911? And what turned the send key into a bug, twice?

SHOW: Next-episode card: 「两天、一百多个提交」.
SAY: Next time: the two days themselves. What the agents did, hour by hour, and what it cost.
