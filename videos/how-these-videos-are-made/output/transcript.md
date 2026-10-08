# How these explainer videos are made: one human, one AI agent, and a lot of measuring

## 00:00 — Made by something that can't watch it
Here's what a paused frame looked like in an early draft of one of these videos, about tic-tac-toe, for kids around 12. Look at the line on the right: 4 times 3 times 2, and then 12.
Pause for a moment. If you were 12, what would you think went wrong here?
It looks like bad multiplication, but the math was right. The 12 was a running count on its way to 24, sitting on the formula's line. The layout lied. And the reviewer who caught it wasn't a child. It was an AI, pretending to be a 12-year-old.
Now the strange part. Almost everything in these videos was made by AI agents: the script, the animation code, and the checks. And none of them can hear the narration, or press play. So how do they know any of it works?
This video covers the pipeline, who did what, how work gets checked without eyes or ears, the Chinese versions, and what still needs a human.

## 01:02 — What the user asked for
It started with one person, the user: a researcher with more papers to read than time. The look comes from 3Blue1Brown, whose videos are animated in Manim, where every frame is drawn by code. The idea for this project came from a post by Andrej Karpathy, as quoted in the first request.
The user's own words go further: our brain is a neural net, and training it takes hardship. AI is patient, they said, but they were doing a lot of cognitive offloading.
A video should be a mentor, showing how papers connect, because they're never isolated. And video is only a first step: the next is something interactive, where the learner has to make things.
Then came four requests. A privacy paper from a friend, which the user hadn't read, to keep the test fair. A tic-tac-toe video, for a middle-school kid. Chinese versions of both. And this video.

## 01:59 — Who did what
The team: one human, the user. One AI agent: Claude Code. Under it, 183 sub-agents in 46 workflow runs, before this video. A workflow is a script the agent writes to launch sub-agents, each with one job. And tools, like a synthetic voice for each language and a speech recognizer.
The user decided what was worth learning, and for whom. They uploaded 36 PDFs, gave the tic-tac-toe numbers, and supplied the program that video teaches. It already worked. The agent only changed a zero into the letter O, and rewrote the comments.
The agent did the rest. It wrote the toolkit that runs the pipeline, and made all but two of over a hundred commits, the project's saved versions. In under a week, work stopped at least six times on usage limits, and each time picked up where it left off.
From request to final cut, the privacy video took about six hours, and tic-tac-toe just over three. And the cost on screen, at API list prices, is for the whole session: all four requests, not one video.

## 03:07 — A script that is code
The pipeline is a chain of files: a paper, a catalog entry, a digest with page numbers, a script, animation code, and the video. Every step leaves a file behind, so you can stop, review, and resume.
Each file gets checked. Agents cataloging the papers read them, not just their names, and found that 4 of the 36 PDFs were the wrong papers. And the privacy digest even lists the paper's own mistakes.
In the script, each beat pairs a show line, the picture, with a say line: the exact words the voice will speak. The animation code reads those words straight from this file. It's written for the ear: nine factorial is spelled out in words.
So other agents review the script before any animation: a sentence costs seconds to fix, an animation costs a re-render. The agent wrote that rule into its own guide on day one. Minutes later, it started six sub-agents building scenes while the review was still running. Eleven minutes after that, all six were stopped.

## 04:14 — The audio is the clock
Now the animation. In this pipeline, the voice is made first, and the animation waits for words, not seconds. This code says: when the narration reaches "A hundred", show a hundred. When it reaches "A million", show a million.
The voice speaks one sentence at a time, so every sentence start is known exactly. Inside a sentence, the toolkit has to guess. It assumes every character takes the same time to say.
Pause and try it. The number on screen has 7 characters, as many as the word example. Say both out loud. How much longer does the number take?
About three seconds: three hundred sixty-two thousand, eight hundred eighty. Far longer than the word. So the toolkit's guess for the words right after it lands almost two seconds early.
The fix so far is manual: this one scene carries about 20 hand-set shifts, the biggest two point two seconds. Yet the online voice used for Chinese can send a time for every word. The toolkit keeps only the audio.

## 05:26 — Checking without eyes or ears
Pause and think. Suppose you can't hear, and you can't press play. How would you check a video?
The agent's answer: turn time into pictures, and sound into text. The toolkit renders a quick draft, and tiles a still from every two seconds into one grid. An agent can look at an image, so this is how it watches.
Between stills, things can go wrong, so to check motion, it grabs frames a fifth of a second apart. If they're all the same, nothing moved.
Then it measures everything it can. A checker called a lint runs each scene without drawing a frame, and flags anything off screen, text that's too small, or objects left behind. And the tic-tac-toe scenes check themselves, with 82 checks, most of them on the numbers shown.

## 06:21 — Reviewers who pretend
Next come the reviewers, fresh agents that didn't build the video. They get the stills, the subtitles as a stand-in for sound, and a role: a director, or a simulated 12-year-old, sharp but ordinary. That simulated kid found real problems, like move labels it couldn't decode.
Round one found 30 issues, including that 12 on the formula line. In round two, a fresh director re-checked each one: 25 were fixed, and 5 only partly.
The director caught a subtler bug. The scene should shuffle 4 marks through all 24 orders, but the board froze while the counter ticked on. The cause is a Manim pitfall: every move was prepared before any played, so each overwrote the last. Now each move is prepared as it plays.
Some problems only show across scenes. In the privacy video, agents building different scenes named the same person Dan in one part and Dev in another. Only a reviewer looking across scenes could catch that.

## 07:31 — Same video, second language
On to Chinese. The user asked to keep English terms that would sound weird translated, with subtitles in both languages. The key rule: one Chinese sentence for each English sentence, so every animation cue still has a sentence to wait for.
Both languages share the same scene code, so the agent checks that the English video didn't change. It compares a fingerprint of every frame, before and after. A few scenes don't render exactly the same every time, but most match.
Then, which voice? The agent can't listen, so it asked a speech recognizer. With the first Mandarin voice, the recognizer heard "Nice" where the script said noise, and "Excellent" where it said epsilon. Another voice passed all 17 test terms, and was chosen. There's no record yet of anyone checking it by ear.
And one subtitle flipped a meaning. The English narration answers with a short no, then says a computer can do more than count. The Chinese subtitle said the opposite: that this is not something a computer can do. Both AI reviewers of the Chinese version caught it.
Pause on this one. The English line is right, and the Chinese says the opposite. Was this a bad translation?

## 08:55 — Bugs in the machinery
It wasn't. The translation had a full stop after that no, but the subtitle tool dropped it when it merged that short subtitle into the next. Tool bugs often look like content bugs.
Another tool bug: a plain build used to reuse old scene movies, so edited scenes were quietly stitched from out-of-date footage. The file dates gave it away: the movies were older than the code. Now a scene is rendered again whenever it's older than its sources, or its voice has changed.
Fixes need checking too. For the Chinese privacy video, reviewers raised 103 points, most of them polish, and fixers made 75 changes. Then skeptical verifiers checked the fixers' work, and made 12 more corrections. One fixer said a passage now fit its time limit. It didn't.

## 09:49 — What to improve next
So what's next? The biggest gaps sit exactly where measuring runs out. First, what only people can do. There's no recorded human review of any narration yet. Every test viewer on record was simulated, and there's no measure yet of what anyone learned.
People should also revisit the agent's own calls, like the length of the privacy video and the choice of Chinese voice.
Second, engineering: a licensed Chinese voice, since the free service isn't licensed for published videos. Timing should follow words, not characters, so the hand-set shifts can go. And shared parts would shrink the scene code.
Third, subtitles. Hand-written rules decide where to cut each sentence into subtitle lines. In its first review round, the newest version fixed most of its targets, but made 11 other subtitles worse. A sentence parser could propose the cuts, and the rules could check them.
Last, and closest to the user's vision: interactivity. The first two videos each come with a playground, a small web page to try the idea yourself, but it sits apart from the video. Next, pausing the video should open it right there, in the same state, and keep your answer.

## 11:08 — A recipe, and a request
Want to try this yourself? A human picks the learner and the question. Write the script first, as code. Let the audio be the clock. Use independent reviewers, including a simulated viewer. Measure what you can't perceive, and check the fixes too. And keep every step in a file.
Above all, remember the goal. As the user put it, AI should not just be cognitive offloading. It should make knowledge easier to reach, and still let you learn just as deeply.
One last thing. This video was made the same way, so it has the same blind spot: the agent that made it can't listen to it. You can. If anything sounded wrong, or lost you, say so, with the time. That's exactly the feedback this pipeline is missing.
