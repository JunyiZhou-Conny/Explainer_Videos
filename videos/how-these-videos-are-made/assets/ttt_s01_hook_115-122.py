        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(left, game_a, win_a, neq, turned, turned_nums, turned_caption)),
                      run_time=0.7)
            vo.wait_until("A hundred")
            self.play(FadeIn(guesses[0], scale=0.8), run_time=0.5)
            vo.wait_until("A million")
            self.play(FadeIn(guesses[1], scale=0.8), run_time=0.5)
            vo.wait_until("Pause the video")
