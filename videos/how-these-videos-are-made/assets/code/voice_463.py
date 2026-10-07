                asyncio.run(edge_tts.Communicate(text, self.voice, rate=rate).save(str(out)))
