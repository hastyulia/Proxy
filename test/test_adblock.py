import zlib
import unittest
from adblock import AdBlock


class AdBlockTests(unittest.TestCase):
    def test_block_gzip(self) -> None:
        blocker = AdBlock()
        html = (b'<table><tbody><tr><td><div id="yatopbanner"><iframe>'
                b'</iframe><a></a></div></td></tr></tbody></table>')
        gzip_html = zlib.compress(html)
        ad = b'abContent-Encoding: deflate\r\n\r\n' + gzip_html
        response = (b'abContent-Encoding: deflate\r\n\r\n<table><tbody><tr>'
                    b'<td></td></tr></tbody></table>')
        self.assertEqual(blocker.block(ad), response)

    def test_block(self) -> None:
        blocker = AdBlock()
        html = (b'<tbody><tr><td><div id="yatopbanner"><iframe></iframe><a>'
                b'</a></div></td></tr></tbody>')
        ad = b'ab\r\n\r\n' + html
        response = b'ab\r\n\r\n<tbody><tr><td></td></tr></tbody>'
        self.assertEqual(blocker.block(ad), response)
