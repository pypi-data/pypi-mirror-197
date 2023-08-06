import re
from typing import Optional, Dict

import requests

from ..helper import HTTP_REGEX
from ..visitor import Context, SiteVisitor


class Misskey(SiteVisitor):
    NAME = 'Misskey'
    URL_REGEX: re.Pattern = re.compile(HTTP_REGEX + r'nicovideo.jp/user/(?P<id>\d+)', re.IGNORECASE)
    
    def __init__(self) -> None:
        self._cache: Dict[str, bool] = {}

    def match(self, url, context: Context) -> Optional[re.Match]:
        match = re.search(HTTP_REGEX + r'(?P<host>[\w.]+)', url)
        if match is None:
            return None

        host = match.group('host')
        return


    def normalize(self, url: str) -> str:
        match = self.URL_REGEX.match(url)
        if match is None:
            return url
        return f'https://bit.ly/{match.group("id")}'

    def visit(self, url, context: Context, id: str):
        res = requests.get(f'https://bit.ly/{id}', stream=True)
        context.visit(res.url)
