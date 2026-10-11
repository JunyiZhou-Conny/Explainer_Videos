import numpy as np

from explainer import music


def test_bed_is_deterministic_quiet_and_the_right_length():
    a = music.generate(12, seed=1)
    b = music.generate(12, seed=1)
    assert a.shape == (12 * music.SR, 2) and a.dtype == np.float32
    assert np.array_equal(a, b)                                   # same seed, same track
    rms_db = 20 * np.log10(np.sqrt(np.mean(a.astype(np.float64) ** 2)))
    assert -30 < rms_db < -20                                     # a bed, not a song
    assert np.abs(a).max() < 0.5                                  # far from clipping
    assert abs(a[0]).max() < 1e-3 and abs(a[-1]).max() < 1e-3     # fades in and out


def test_seeds_differ():
    assert not np.allclose(music.generate(6, seed=0), music.generate(6, seed=1))
