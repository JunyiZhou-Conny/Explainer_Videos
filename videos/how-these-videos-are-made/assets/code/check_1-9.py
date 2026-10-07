"""Lint a scene without rendering frames: anything off-frame, text under 20 pt, leftovers at the end.

    python -m explainer.check videos/<id>/scenes/s08_payoff.py Payoff [--lang zh] [--tts silent]

Runs the scene as a Manim dry run (narration audio comes from the TTS cache, so timings are
real) and, after every play()/wait(), reports:
  OUT    a visible mobject outside the safe area x in [-6.6, 6.6], y in [-3.6, 3.6]
  SMALL  a Text / MathTex rendered below 20 pt
and at the end lists mobjects still visible (scenes should end on an empty frame).
