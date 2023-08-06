from .context.pycwt.helpers import (ar1, ar1_spectrum, boxpdf, fftconv, find,
                                    get_cache_dir, rect, rednoise)


class TestHelpers:
    def test_get_cache_dir(self):
        cache_dir = get_cache_dir()
        assert cache_dir == "/home/sebastian/.cache/pycwt/"
