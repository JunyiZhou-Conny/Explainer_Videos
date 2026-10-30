# 项目周记 E3 · Copying Claude's chat page: what we copied, refused, added, and haven't built

## 00:00 — Copied, on purpose
Before you type, our triage page shows a serif greeting asking where it hurts, an input box in the middle of the screen, and a row of suggestions under it. If that reminds you of Claude's app, it should. You asked for a one-to-one copy, and the agent built it.
Isn't copying exactly what a product should avoid? Here it was the plan. What was copied, what was refused, what we added, and what nobody has built yet: that is this episode.

## 00:27 — The parts of a chat page
First, the parts. Almost every chat app has the same ones, and designers have names for them. The empty state is the page before the first message. Suggestion chips are ready-made questions; ours start demo replays. The composer is the input box. Inside it sit a model menu and the send key, which turns into a stop key while you wait.
Once you send, your words sit in a bubble on the right, and the answer runs full width without a box. Under each answer is an action row: copy, and under the latest one, retry. Scroll up, and a round button appears to take you back to the bottom. And under the input, one line of fine print: the disclaimer.

## 01:11 — Why copy?
The team has no designer. You asked for the page to follow Claude's chat, one to one, and that night the agent wrote the reasons down as decision six, against two other options. Invent our own style: without references, probably ordinary, and likely to be redone. Take the best parts of several apps. Or copy one mature app exactly, with no mixing.
Before the answer: why would copying one product beat picking the best parts of several?
Because parts from different products disagree: spacing, colours, how a button behaves. The seams show, and the decision record names a second cost: you can no longer say where each choice came from. One mature reference answers every small question the same way, so the fewest design calls give a page that is neither ugly nor wrong. It also helps the people using it. Designers call it Jakob's law: users spend most of their time on other sites, so they prefer yours to work the same way. The rule the agent proposed: every screen copies exactly one reference. For the chat page, that is Claude's app, which everyone on the team uses every day.

## 02:25 — What was copied
Here is what was copied. One column, at most 768 pixels wide. Your message in a beige bubble on the right. The answer in serif type, full width, no frame.
The composer: a white rounded box that grows as you type. Along its bottom edge, where Claude keeps attachments and tools, we put three drop-downs of our own: who is asking, insurance, and where you are. On the right, the model menu, Terra at medium effort, next to the terracotta send key, the same spot where Claude's help page puts its own model menu.
Two choices here were yours: copy Claude's chat page at all, and copy its warm colours and serif type too, not only the layout. They stay inside this one page; the rest of the site keeps its neutral theme.

## 03:13 — What was not copied
What was not copied, each for a reason. Claude's logo, name and private fonts: they aren't ours, so where Claude shows its logo while it thinks, ours shows a small dot, and the fonts are open ones. The sidebar, chat history, attachments and tools: we have no accounts and no storage, and the prototype doesn't need them. And the two from episode two: the raw reasoning, and words streaming as they are written. Our answers pass the checker first.

## 03:42 — What we added
Now a harder question. A parent in China opens this page about their child in Boston. What do they need that the student doesn't?
Start with 911. A parent can't dial it from China. So every fixed line on the page changes for parents: instead of call 911, it asks the child or someone nearby to call 911 locally. Phone numbers get a plus one and the words dial from China. Emergency and crisis numbers get no dial link at all, only: ask someone there to call.
Some additions are for everyone. In an emergency, a red do-this-now block comes first, appears at once, and is read aloud by screen readers. An emergency link sits in the top bar at all times. Demos and estimates are labelled simulated, and when a student copies an answer for a parent, the label goes with it: not a diagnosis.
And some are for people who use the page differently: hidden headings a screen reader can jump between, source links at least 24 pixels tall so a finger can hit them, and at 400 percent zoom, a page that opens at the top with the emergency link in view.

## 05:00 — How it was built
How did the agent build it? On Wednesday at one fifty-nine in the morning, Boston time, it wrote the decision down. Seventeen minutes later it committed the rebuilt page: 27 files. Six minutes after that, end-to-end tests.
Then came the reviews. An independent visual review. Streaming, which you had asked for, built as progress only, and a review of it. A second visual review, which brought Claude's phone layout and much of the parent wording and accessibility you just saw. And a final review from five angles: about 30 problems, fixed on parallel branches, then checked once more.
One bug shows why this is hard. Send and stop share one button: while you wait, send turns into stop. Click stop, the wait ends, and in that same click the button turns back into send, so whatever was in the box went out. In a demo replay, that was the very message you had just stopped. The fix was one line. Then Bugbot found the mirror image: double-click send, and the second click lands on stop. Another one-line fix: ignore the second click of a double-click. Copying how a button looks does not copy how it behaves.

## 06:11 — What else
What do the big chat apps have that we don't? Conversation history and projects, file uploads, voice, a side panel for documents and code, and memory across chats. Most of them need accounts and storage, which this prototype doesn't have. Of these, voice may matter most here, for a worried parent who would rather speak than type; history and memory would mean keeping health conversations, which needs a privacy decision first.
And what could only we build? One answer for two readers, the student's and the parent's, side by side; every answer already carries a folded summary for parents, the seed. A summary card the student sends home; copy for parent is already a first step. And a hand-off to booking: the answer already writes the English sentences to say; the page could place the call, or fill in the form.
And what waits for you: a dozen open items. Decision six is still a proposal, and so is what the agent added to it that night, unattended: progress-only streaming, the model menu and retry. Two more choices need your yes: a stopped message is no longer taken back but goes out with your next one, and parents get no dial link for crisis lines.

## 07:27 — Recap
So: one reference per screen, copied exactly, so every small choice has an answer and the page feels familiar. Claude's layout, composer and colours, kept to this page. Not its logo, its history, its raw thoughts or its word-by-word streaming. Plus what only a medical page for two audiences needs: emergency first, wording a parent in China can act on, and labels that travel with copied text.
Three questions. Why copy one product instead of several? Why does the parent's page ask someone else to call 911? And what turned the send key into a bug, twice?
Next time: the two days themselves. What the agents did, hour by hour, and what it cost.
