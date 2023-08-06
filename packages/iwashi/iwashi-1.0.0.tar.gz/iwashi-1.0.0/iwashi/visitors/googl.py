import re

import requests

from ..visitor import Context, SiteVisitor
from ..helper import HTTP_REGEX


class Googl(SiteVisitor):
    NAME = 'Googl'
    URL_REGEX: re.Pattern = re.compile(HTTP_REGEX + r'goo\.gl/(?P<id>\w+)', re.IGNORECASE)

    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://{match.group("id")}'

    def visit(self, url, context: Context, id: str):
        res = requests.get(f'https://goo.gl/{id}')
        context.create_result('Googl', url=url, score=1.0)
        context.visit(res.url)