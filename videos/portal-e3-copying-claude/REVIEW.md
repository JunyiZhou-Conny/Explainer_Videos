# Review record: Copying Claude's chat page (项目周记 E3 · 照着 Claude 抄)

Produced 2026-10-30 by a Claude Code cloud session (issue
[#60](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/60)) on branch
`claude/funny-cannon-6at1kg`, in the 3Blue1Brown style, now the house default (owner, 2026-10-30:
「开始做下一集 E3 吧，以后默认用3blue1brown的style」). Verified facts and unclaimed reviews are kept separate.

## Content gates (AGENTS.md)

1. **Hook.** s01 opens on our empty triage page, redrawn in its own colours, next to the same layout as
   grey outlines (Claude's app, no logo); the puzzle: "Isn't copying exactly what a product should
   avoid? Here it was the plan." ✔
2. **Intuition before formalism; an animated mechanism per core idea.**
   - s02 names each part on a redrawn page, empty and after one turn.
   - s03 shows a collage whose seams clash, against one reference.
   - s04 ticks what was copied on the page, grows the composer, scopes the palette to one tile of the site.
   - s05 crosses out what was not copied, with the reason for each.
   - s06 sets the student's and the parent's strings side by side.
   - s07 shows the night and the day's review bands on time axes, and the stop bug happening on a composer.
   - s08 draws the ideas: a two-reader answer, a card on the parent's phone, a hand-off to booking.
   - s09 sorts every named part on the page by colour.

   No code on screen. ✔
3. **Ponder moments and recap.** Two pause-and-ponder cards with a held pause:
   - s03: "Why would copying one product beat picking the best parts of several?", answered by the seams and Jakob's law.
   - s06: "What does a parent in China need … that the student doesn't?", answered by the 911 and phone-number changes.

   s09 recaps with the sorted page and asks three bilingual test-yourself questions, then holds a pause. Each is answered in the episode (s03, s06, s07). ✔
4. **Written for the ear; anchored cues.**
   - Chinese UI strings are shown, never read.
   - "0006" is spoken "decision six" (it ran together as "zero zero zero six").
   - "1:59" is spoken "one fifty-nine".
   - "Jakob's law" got a lexicon entry, read as "Jacob's law".
   - Every reveal waits on a word anchor. ✔
5. **Simulated-viewer QA over the full draft.** Findings and fixes below. ✔
6. **Measured checks + human review.** Measured values under *Verified*. Human review: **waived** by
   Conny (AGENTS.md, 2026-10-22): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」.
   No human has listened to this cut. ✔ (waiver)

## Research and script review before scenes

- **Research:** two independent agents.
  - PR #41's build path from the portal at `b7ab98e`: commit phases, review rounds, the stop/send bugs, issue #40's ten acceptance criteria, exact UI strings, parent vs student.
  - Chat-UI names, Claude's and ChatGPT's features, WCAG 2.2, and Jakob's law, from primary pages. The OpenAI pages refused automated fetches, so official search snippets were used and marked as such.
- **Accuracy read** (a third independent agent, against the code, issue #40, PR #41 and its handoff): 15 findings, all applied. The ones that changed the story:
  - **Who asked for the copy.** The owner asked for the one-to-one copy in issue #40 (01:45), before the agent wrote decision 0006. The video no longer says "the agent copied it" or "one choice was yours"; two choices were.
  - **Zoom.** At 400 % zoom the page *opens at the top* with the emergency link in view. It is not pinned there.
  - **Stop bug.** It sent whatever was in the box. Only in a demo replay was that the message just stopped.
  - **Review timeline.** The second visual review produced most of the parent wording and accessibility. The times on the axis are when fixes landed.
  - **Open items.** The handoff lists a dozen open items, not two, including 0006's unconfirmed addendum.
  - **On-screen strings.** Several were not verbatim (0006's title, the design doc's heading, the S02 bubble); the parent's +1 number keeps its dial link.

## Whole-video QA (first draft, 7:43)

Simulated target viewer (an independent agent playing Conny from the bilingual subtitles and a frame
every 3 s), plus my own frame-by-frame pass:

- [06:15–06:38][MISSING] His core question, what could we innovate, got about 22 s of text cards. FIX: s08 draws three ideas, each tagged "idea, not built":
  - the answer split into the student's and the parent's version, with demo 01's real folded 「给家长的摘要」 opened;
  - a card arriving on the parent's phone in China;
  - the 「可以这样说：」 block with demo 03's real English line, handing off to booking.
- [06:21][CONFUSING] The parent summary was never shown before. FIX: it is now drawn in s08 with its verbatim text.
- [02:39][WRONG] The three drop-downs sounded copied from Claude. FIX: "where Claude keeps attachments and tools, we put three drop-downs of our own", tagged BLUE.
- [00:27 → 07:00][MISSING] The ten named parts were never sorted. FIX: s09 shows the page again; each part is listed as copied (GREEN), added (BLUE) or not copied (RED), with outlines on the page.
- [02:12 vs 06:40][WRONG] "The rule, now written down" vs "still a proposal". FIX: "the rule the agent proposed", with 提议 flashed and kept on the recap's rule.
- [05:29–05:58][CONFUSING/SLOW] The stop bug was one icon swapping. FIX: a composer with typed text; the cursor clicks stop, the key swaps under it, and the text flies up as a sent bubble (in demo replay, the stopped message). It closes: "Copying how a button looks does not copy how it behaves."
- [06:51][CONFUSING] "A stopped message goes out with your next one" had no alternative. FIX: "is no longer taken back but goes out with your next one".
- [06:42][CONFUSING] "Its addendum" was undefined. FIX: "what the agent added to it that night, unattended: progress-only streaming, the model menu and retry".
- [05:11][CONFUSING] "The streaming you asked for" came right after "not copied: streaming". FIX: "Streaming, which you had asked for, built as progress only".
- [03:11][CONFUSING] The logo-to-dot link was missing. FIX: "where Claude shows its logo while it thinks, ours shows a small dot" (design doc).
- [02:54][SLOW] A blank screen under "two choices were yours". FIX: two option cards (layout only / layout + colours + serif), the second ticked; the quote no longer breaks after 「（」.
- [07:25][SLOW] The questions cut straight to E4. FIX: a 3.5 s hold, and Chinese under each question.
- [06:00][MISSING] The mainstream features were listed, not judged. FIX: one line each, framed as a view. Voice may matter most for a worried parent; history and memory would mean storing health conversations, which needs a privacy decision first.
- [01:06][LAYOUT] The disclaimer callout flashed by. FIX: a 1.8 s hold.
- [00:12, 04:45][LAYOUT] The stamp sat over the page, and the accessibility labels collided. FIX: both moved; this was already caught by my frame pass.
- [captions] 「空白页」 → 「空状态，也就是首屏」; 「在这里，这就是计划」 → 「但这一次，照抄就是计划」; 「把预约接过去」 → 「直接帮你预约」; the help-page line reworded.
- [layout, my frame passes] Fixed in the scenes:
  - the request stamp over the top bar;
  - the S04 quote's line break;
  - the student/parent headers off their columns;
  - the S08 chip grid;
  - the S08 student page's first line touching its frame;
  - the phone card's text spilling out;
  - S09's smaller page hiding the action row.
- [review bots on PR #62] Bugbot raised three findings:
  - **"Fix line appears on wrong cue" (s07):** real. Animating an off-screen mobject added it early. Fixed in 4dda5ac.
  - **"Helper import needs missing script":** true at a WIP checkpoint, before `script.md` existed.
  - **"Chat page sits in caption band":** does not apply to the `video.yaml` route. Its burn mode scales the picture above the subtitle band. Answered on the thread.

## Verified (final render)

To be filled from the final 1080p60 build.

## Not claimed

- **No human listened** to this cut; the listen is waived (above). Prosody, pacing by ear and music balance by ear are unverified.
- **No ASR round trip.** Risky words were checked at the phoneme level instead, and all read as intended: decision six, 768 pixels, one fifty-nine, Bugbot, Jakob's law, terracotta, 400 percent, 24 pixels, end-to-end, 27, Terra, one-to-one.
- The exact disclaimer wording of Claude's app or ChatGPT; who ran PR #41's reviews or whether they compared screenshots side by side; that Claude's app has a thinking on/off switch. None of these is claimed.
- The ideas in s08 and the phone card's text are illustrations, not built features.
- The Chinese captions were checked by the viewer pass for meaning, not by a separate translator.
- The portal PRs (#36, #41) are open; the code may move after `b7ab98e`. Decision 0006 is still "proposed".
