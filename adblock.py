import re
import zlib


ADS_PATTERN = re.compile('<div .*?((class=)|(id=))((.*?ad.*?)|(.*?banner.*?)|'
                         '(.*?offer.*?)).*?>.*?</div>')


class AdBlock:
    def block(self, response):
        response_split = response.split(b'\r\n\r\n', maxsplit=1)
        gzip_f = response_split[0].find(b'Content-Encoding: deflate')
        if gzip_f != -1:
            html = zlib.decompress(response_split[1])
        else:
            html = response_split[1]
            rn = html.find(b'\r\n')
            if rn != -1:
                html = html.split(b'\r\n', maxsplit=1)[1]

        html = html.decode()
        html = re.sub(ADS_PATTERN, '', html)
        html = html.encode()
        reduplicate_response = response_split[0] + b'\r\n\r\n'
        reduplicate_response += html
        return reduplicate_response
