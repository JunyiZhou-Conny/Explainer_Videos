"""S11 · The long last line: uv run.

1. The line, split into its parts.
2. uv · --python 3.12 (pyproject requires-python >=3.12) · --directory services/voice.
3. --extra mic (pyproject optional "mic" = pyaudio); a container with a crossed-out microphone.
4. python -c "…" → start the voice session; the README's `uv run careonex-voice` → main() checks for
   keys in env vars or ~/.aws/credentials and stops; INFERRED: calling run() skips that check.
"""

from manim import *

from explainer import style as S
from explainer.scene import VoiceScene

from common import (BAD_C, CODE_C, NARRATION, OK_C, QUERY_C, code_panel, container, mark_bad, mono, sans, serif,
                    source_tag, text_panel)

SAY = NARRATION["S11"]
PARTS = ["uv run", "--python 3.12", "--extra mic", "--directory services/voice",
         'python -c "import asyncio; from nova_sonic.__main__ import run; asyncio.run(run())"']


class UvRun(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the parts
        with self.voiceover(SAY[0]) as vo:
            row1 = VGroup(*[mono(p, 26) for p in PARTS[:4]]).arrange(RIGHT, buff=0.35)
            row2 = mono(PARTS[4], 22)
            line = VGroup(row1, row2).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            if line.width > 12.6:
                line.scale_to_fit_width(12.6)
            line.to_edge(UP, buff=0.55)
            boxes = VGroup(*[SurroundingRectangle(p, buff=0.08, corner_radius=0.06, color=QUERY_C, stroke_width=2)
                             for p in [*row1, row2]])
            self.play(FadeIn(line), run_time=0.8)
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.25), run_time=1.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- uv, python, directory
        with self.voiceover(SAY[1]) as vo:
            items = VGroup(
                VGroup(mono("uv run", 30, QUERY_C), serif("set up the right Python and libraries, then run a command in them", 26)),
                VGroup(mono("--python 3.12", 30, QUERY_C), serif("the oldest version Amazon's streaming library accepts", 26)),
                VGroup(mono("--directory services/voice", 30, QUERY_C), serif("use the voice project's settings", 26)))
            for it in items:
                it.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
            items.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.6).to_edge(LEFT, buff=0.8)
            self.play(Indicate(row1[0], color=QUERY_C), FadeIn(items[0], shift=RIGHT * 0.15), run_time=0.9)
            vo.wait_until("Python 3.12")
            pv = VGroup(mono('requires-python = ">=3.12"', 22, S.GREY), source_tag("code", "voice/pyproject.toml")
                        ).arrange(RIGHT, buff=0.3).next_to(items[1], RIGHT, buff=0.5)
            if pv.get_right()[0] > 6.5:
                pv.next_to(items[1][1], DOWN, buff=0.1).align_to(items[1], LEFT)
            self.play(Indicate(row1[1], color=QUERY_C), FadeIn(items[1], shift=RIGHT * 0.15), run_time=0.9)
            self.play(FadeIn(pv), run_time=0.5)
            vo.wait_until("And the directory")
            self.play(Indicate(row1[3], color=QUERY_C), FadeIn(items[2], shift=RIGHT * 0.15), run_time=0.9)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- --extra mic
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(items, pv)), run_time=0.5)
            ex = VGroup(mono("--extra mic", 30, QUERY_C), serif("also install PyAudio, the microphone library", 26)
                        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT).to_edge(LEFT, buff=0.8).shift(DOWN * 0.2)
            toml = text_panel(["[project.optional-dependencies]", 'mic = ["pyaudio>=0.2.13"]'], size=22)
            toml.next_to(ex, DOWN, buff=0.35).align_to(ex, LEFT)
            tag = source_tag("code", "voice/pyproject.toml").next_to(toml, DOWN, buff=0.15).align_to(toml, LEFT)
            self.play(Indicate(row1[2], color=QUERY_C), FadeIn(ex), run_time=0.9)
            self.play(FadeIn(toml), FadeIn(tag), run_time=0.7)
            vo.wait_until("a container has no microphone")
            box = container("voice", "inside a container?", width=3.4, name_size=28, sub_size=22).move_to(RIGHT * 3.6 + DOWN * 0.6)
            micx = VGroup(serif("no microphone,", 24, BAD_C), serif("no speakers", 24, BAD_C)).arrange(DOWN, buff=0.05)
            micx.next_to(box, DOWN, buff=0.25)
            x = mark_bad(0.5).move_to(box.frame.get_corner(UR))
            self.play(FadeIn(box), run_time=0.6)
            self.play(Create(x), FadeIn(micx), run_time=0.7)
            vo.wait_until("so the voice program")
            lap = serif("→ runs directly on the laptop", 26, OK_C).next_to(micx, DOWN, buff=0.25)
            self.play(FadeIn(lap), run_time=0.6)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- python -c, and why not the short command
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not line and m is not boxes], run_time=0.5)
            self.play(Indicate(row2, color=QUERY_C), run_time=0.8)
            tiny = serif("a tiny Python program: start the voice session  run()", 26).move_to(UP * 1.1)
            self.play(FadeIn(tiny), run_time=0.6)
            vo.wait_until("The team's instructions")
            short = VGroup(sans("THE README'S WAY", 20, S.GREY), mono("uv run careonex-voice", 26),
                           mono("→ main()", 24, S.GREY)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).to_edge(LEFT, buff=0.7).shift(DOWN * 0.6)
            code = code_panel('def main():\n'
                              '    has_env = os.environ.get("AWS_ACCESS_KEY_ID") and ...\n'
                              '    has_file = os.path.exists("~/.aws/credentials")\n'
                              '    if not has_env and not has_file:\n'
                              '        raise SystemExit(1)\n'
                              '    asyncio.run(run())', size=20, width=7.4)
            code.next_to(short, RIGHT, buff=0.5).align_to(short, UP)
            src = VGroup(mono("voice/nova_sonic/__main__.py (shortened)", 20, S.GREY), source_tag("code")
                         ).arrange(RIGHT, buff=0.25).next_to(code, DOWN, buff=0.12).align_to(code, RIGHT)
            self.play(FadeIn(short), FadeIn(code), FadeIn(src), run_time=1.0)
            vo.wait_until("that an SSO login")
            self.play(Circumscribe(VGroup(*code.code_lines[2:5]) if hasattr(code, "code_lines") else code, color=BAD_C), run_time=1.2)
            vo.wait_until("Calling the session directly")
            why = VGroup(source_tag("inferred"),
                         serif("calling run() directly skips a check that expects saved long-lived keys;", 24, S.PURPLE),
                         serif("an SSO login keeps its keys elsewhere (~/.aws/sso/cache)", 24, S.PURPLE)
                         ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).to_edge(DOWN, buff=0.35).to_edge(LEFT, buff=0.7)
            self.play(FadeIn(why), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
