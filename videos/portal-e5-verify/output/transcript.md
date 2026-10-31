# 项目周记 E5 · How an agent proves its change is right: every order, and the real app

## 00:00 — A bug nobody had seen
Here is a bug in our prototype. A student has a referral to an ear, nose and throat specialist, valid until January twenty-second. Their parent opens the booking page, leaves it open past that moment, and presses submit. By the agent's reading of the code, the expired referral is attached anyway, and the tracker shows the specialist as booked, never expired.
All 245 existing tests passed; none of them books after the expiry. The code even carries a comment saying expired referrals are left alone. No person had noticed. On Friday afternoon an agent reported it, after trying every order of a few actions in a small world. This episode is about how an agent can prove a change is right before anyone looks.

## 00:48 — One function, many orders
Every change to the app's data goes through one function, called the reducer. It takes the current state and a single action, such as book, confirm, reschedule, cancel or complete, and returns the next state. The booking page checks the referral when it draws, but the booking reaches the reducer later. So the order of events matters, and time passing is an event too.
A test follows a path someone chose. The bug lives on a path nobody chose: first time passes, then the booking goes through.
A test checks the cases someone thought of. What checks the ones nobody thought of?

## 01:28 — Try every order in a small world
Build a small world instead: two referrals, three specialist slots, and a clock with just two moments, right after the referrals are written and an hour after they expire. From the starting state there are thirteen possible moves. Make each one, then every move from each result, layer by layer, merging any state you've already seen. In this world that is 13,898 states, reached in about a second, and every one of them comes from the real reducer, not a copy.
Four rules are checked at every state and a fifth on every step, all written in plain language, such as one referral backs at most one live appointment, and an expired referral is never newly attached. Because the search goes layer by layer, the first broken rule it meets comes with the shortest story that breaks it. Here, two steps: time passes, then book with that referral.

## 02:22 — Why it slipped through
Why did it slip through? Booking looks only at the referral's stored status. Expired is never stored; it is only worked out for the screen. And the page checks when it draws, not when you submit. The agent did not change the product code. It recorded the bug as a known finding and left the fix to a person: compare the expiry date inside the reducer, or check again on submit.
The rule was not loosened to make the check pass. And the check is built to fail in two ways: if any new rule breaks, and if this known bug ever disappears. That second failure reminds whoever fixes it to delete the note, so the note can never hide the bug if it comes back.

## 03:04 — Breaking it on purpose
Why would an agent break its own code on purpose?
Because a check you have never seen fail proves nothing. Maybe it can't fail at all. So the agent broke the reducer five times on purpose, in five different ways, and ran the check after each. All five were caught, each with a story of two steps or fewer, and each breakage was then undone. It is a hand-made version of what testers call mutation testing; the classic paper on it is from 1978.

## 03:38 — The same idea at Amazon's scale
The idea is old and serious. In 2015 Amazon described checking its designs this way, using TLA+, a language created by Leslie Lamport. In one database service it found a data-loss bug whose shortest story was thirty-five steps long, a bug that had passed design reviews, code reviews and testing. Ours is tiny by comparison, two steps in a one-second check, but it is the same move: let a machine walk every order a person would never try.

## 04:11 — Driving the real app
The second tool drives the app itself, the way a parent would. The agent starts its own copy of the app and its own browser from a saved demo state, then clicks through: open the referral, choose an in-network clinic, pick a time, submit, wait for pending, open the tracker. It finds each control by its role and accessible name, the label a screen reader announces, and waits for the page to settle after each step.
Right means two things at once: the screen says the specialist is booked, and the saved data says the referral now points to that new appointment. Each run is required to keep evidence: screenshots, the saved state, and no browser errors. When a step fails, it says which buttons it could see instead. And when it's done, it shuts down only what it started.

## 05:00 — Where it came from, and what waits
Both tools came from trying two skills in a public plugin called pstack, on Friday afternoon, in two commits twenty-seven minutes apart. Anthropic's own advice for Claude Code says the same thing plainly: give the agent a check to run, or you become the test suite.
What waits for you: choosing the fix for the expired referral, and trying the app-driving tool on your own laptop; so far it has only run in the cloud. And the pull request is still a draft. The last episode asked whether layers can stand in for a human review. Here are two more: a check that tries every order, and an agent that uses the real app.

## 05:40 — Recap
So: one tool walks every order of actions in a small world and hands back the shortest story that breaks a rule. The other uses the real app like a parent and keeps the evidence. The first was checked by breaking it on purpose; the second, by running every flow end to end.
Three questions. What does the exhaustive check try that an ordinary test doesn't? Why break your own code on purpose? And why does the check fail when the bug gets fixed?
Next: before any backend code is written, how do you choose the backend?
