"""S05 · Who are you? AWS profile and SSO login.

1. The team's AWS account: a fenced area with Bedrock models, S3 buckets, the Knowledge Base; a
   budget meter "$30 / month on Bedrock" (TEAM NOTES: TEAM_SETUP.md).
2. Five people → a sign-in portal (SSO, e-mail + second factor) → the AC215 permission card
   (what it allows, and ✗ careonex-*). TEAM NOTES.
3. The two lines; the one-time `aws configure sso` (session careonex, role AC215, profile
   careonex-team) → ~/.aws/config; `aws sso login` → browser approve → 8-hour key in ~/.aws/sso/cache.
4. session.py: _load_sso_credentials (botocore, profile) and the "log in again" message. READ IN CODE.
"""

from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.scene import VoiceScene

from common import (AWS_C, BAD_C, DATA_C, NARRATION, OK_C, PEOPLE, PERSON_C, QUERY_C, aws, big_line,
                    code_panel, mark_bad, mark_ok, mono, sans, serif, source_tag, store, text_panel)

SAY = NARRATION["S05"]


class Login(VoiceScene):
    def construct(self):
        # 1 ---------------------------------------------------------------- the account
        with self.voiceover(SAY[0]) as vo:
            fence = RoundedRectangle(width=8.6, height=4.6, corner_radius=0.3, stroke_color=AWS_C, stroke_width=3)
            fence = DashedVMobject(fence, num_dashes=80).move_to(LEFT * 1.6 + DOWN * 0.1)
            ftitle = sans("THE TEAM'S AWS ACCOUNT", 24, AWS_C).next_to(fence, UP, buff=0.15).align_to(fence, LEFT)
            aws_word = serif("AWS = Amazon Web Services: computers and services you rent", 24, S.GREY).to_edge(UP, buff=0.35)
            items = VGroup(aws("bedrock model", "Nova 2 Sonic", "hears and speaks", width=3.6, name_size=24, sub_size=20),
                           aws("bedrock model", "Titan Embeddings", "text → numbers", width=3.6, name_size=24, sub_size=20),
                           store("ac215-program-kb-…", "documents", tag="S3 bucket", width=3.6, name_size=22, sub_size=20),
                           aws("bedrock", "Knowledge Base", "searchable passages", width=3.6, name_size=24, sub_size=20))
            items.arrange_in_grid(rows=2, buff=(0.4, 0.35)).move_to(fence)
            self.play(FadeIn(aws_word), run_time=0.6)
            self.play(Create(fence), FadeIn(ftitle), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(i, scale=0.95) for i in items], lag_ratio=0.2), run_time=1.4)
            vo.wait_until("The team's notes show")
            meter = VGroup(sans("BEDROCK BUDGET", 20, S.GREY),
                           mono("$30 / month", 30, QUERY_C),
                           serif("alerts at 50 %, 80 %, 100 %", 22, S.GREY),
                           source_tag("notes")).arrange(DOWN, buff=0.15)
            meter.next_to(fence, RIGHT, buff=0.5)
            self.play(FadeIn(meter, shift=LEFT * 0.2), run_time=0.8)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 2 ---------------------------------------------------------------- people, portal, permissions
        with self.voiceover(SAY[1]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            names = ["Nadir", "Caroline", "Helen", "Junyi", "Marco"]
            people = VGroup(*[VGroup(person_icon(PERSON_C, 0.55), serif(n, 22)).arrange(DOWN, buff=0.08) for n in names])
            people.arrange(DOWN, buff=0.18).to_edge(LEFT, buff=0.6)
            portal = VGroup(RoundedRectangle(width=3.3, height=2.0, corner_radius=0.15, stroke_color=PERSON_C),
                            VGroup(sans("SIGN-IN PORTAL", 20, S.GREY), serif("SSO", 40),
                                   serif("e-mail + second factor", 20, S.GREY)).arrange(DOWN, buff=0.1))
            portal[1].move_to(portal[0])
            portal.move_to(LEFT * 1.6)
            self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.1) for p in people], lag_ratio=0.15), run_time=1.0)
            arrows = VGroup(*[Arrow(p.get_right(), portal.get_left(), buff=0.1, stroke_width=2, color=S.GREY,
                                    max_tip_length_to_length_ratio=0.08) for p in people])
            self.play(FadeIn(portal), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), run_time=1.2)
            vo.wait_until("After signing in")
            allow = [("talk to Nova 2 Sonic and Titan", True), ("read and write ac215-* buckets", True),
                     ("ac215-* vector buckets", True), ("create and search knowledge bases", True),
                     ("anything named careonex-*", False)]
            rows = VGroup()
            for t, ok in allow:
                m = mark_ok(0.26) if ok else mark_bad(0.22)
                rows.add(VGroup(m, serif(t, 24, S.WHITE if ok else BAD_C)).arrange(RIGHT, buff=0.2))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
            card = VGroup(VGroup(sans("PERMISSION SET", 20, S.GREY), mono("AC215", 34, QUERY_C)).arrange(DOWN, buff=0.08),
                          rows).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
            frame = SurroundingRectangle(card, buff=0.3, corner_radius=0.15, color=QUERY_C)
            card = VGroup(frame, card).move_to(RIGHT * 3.6)
            a2 = Arrow(portal.get_right(), frame.get_left(), buff=0.1, color=QUERY_C, stroke_width=3)
            self.play(GrowArrow(a2), FadeIn(card), run_time=1.0)
            tag = source_tag("notes", "TEAM_SETUP.md").next_to(frame, DOWN, buff=0.2).align_to(frame, LEFT)
            self.play(FadeIn(tag), run_time=0.4)
            vo.wait_until("and nothing in the company's")
            self.play(Indicate(rows[-1], color=BAD_C), run_time=1.0)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 3 ---------------------------------------------------------------- the profile and the login
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
            l1 = big_line('$env:AWS_PROFILE = "careonex-team"', 26)
            l2 = big_line('aws sso login --profile careonex-team', 26)
            VGroup(l1, l2).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(UP, buff=0.45)
            self.play(FadeIn(l1), FadeIn(l2), run_time=0.8)
            once = text_panel(["aws configure sso      (once)",
                               "  SSO session name: careonex",
                               "  SSO start URL:    <portal>",
                               "  account:          <team account>",
                               "  role:             AC215",
                               "  default region:   us-east-1",
                               "  profile name:     careonex-team"], size=20, colors={0: S.GREY, 6: QUERY_C})
            once.to_edge(LEFT, buff=0.6).shift(DOWN * 1.0)
            dest = VGroup(mono("~/.aws/config", 22, DATA_C), source_tag("notes")).arrange(RIGHT, buff=0.25)
            dest.next_to(once, DOWN, buff=0.2).align_to(once, LEFT)
            self.play(FadeIn(once, shift=UP * 0.15), FadeIn(dest), run_time=1.0)
            vo.wait_until("The command aws sso login")
            browser = VGroup(RoundedRectangle(width=3.2, height=1.6, corner_radius=0.1, stroke_color=PERSON_C),
                             VGroup(sans("BROWSER", 18, S.GREY), serif("Allow access?", 26),
                                    VGroup(RoundedRectangle(width=1.2, height=0.4, corner_radius=0.08).set_fill(OK_C, 0.6).set_stroke(width=0),
                                           ).add(serif("Approve", 20).move_to(ORIGIN))).arrange(DOWN, buff=0.12))
            browser[1].move_to(browser[0])
            browser[1][2][1].move_to(browser[1][2][0])
            browser.move_to(RIGHT * 3.6 + UP * 0.1)
            self.play(FadeIn(browser, shift=DOWN * 0.2), run_time=0.7)
            key = VGroup(Circle(radius=0.18, color=QUERY_C, stroke_width=4), Line(RIGHT * 0.18, RIGHT * 0.75, color=QUERY_C, stroke_width=4),
                         Line(RIGHT * 0.55, RIGHT * 0.55 + DOWN * 0.18, color=QUERY_C, stroke_width=4))
            key.next_to(browser, DOWN, buff=0.4)
            hrs = mono("valid 8 hours", 24, QUERY_C).next_to(key, RIGHT, buff=0.25)
            cache = mono("→ ~/.aws/sso/cache", 22, DATA_C).next_to(VGroup(key, hrs), DOWN, buff=0.2)
            self.play(FadeIn(key, shift=DOWN * 0.2), FadeIn(hrs), run_time=0.8)
            self.play(FadeIn(cache), run_time=0.5)
            self.wait(max(0.1, vo.remaining() - 0.2))

        # 4 ---------------------------------------------------------------- how the code uses it
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(once, dest, browser, key, hrs, cache)), run_time=0.6)
            code = code_panel('def _load_sso_credentials():\n'
                              '    profile = os.environ.get("AWS_PROFILE")\n'
                              '    frozen = Session(profile=profile).get_credentials()\n'
                              '    ...\n'
                              '    raise SystemExit(\n'
                              '        f"Run:  aws sso login --profile {profile}   and start again.")',
                              size=22, width=11.0)
            code.move_to(DOWN * 0.5)
            src = VGroup(mono("services/voice/nova_sonic/session.py (shortened)", 20, S.GREY), source_tag("code")
                         ).arrange(RIGHT, buff=0.3).next_to(code, DOWN, buff=0.2).align_to(code, LEFT)
            self.play(FadeIn(code, shift=UP * 0.2), FadeIn(src), run_time=1.0)
            vo.wait_until("When they expire")
            self.play(Circumscribe(code.code_lines[4:6] if hasattr(code, "code_lines") else code, color=QUERY_C), run_time=1.4)
            self.wait(max(0.1, vo.remaining() - 0.2))
        self.play(FadeOut(*self.mobjects), run_time=0.8)
