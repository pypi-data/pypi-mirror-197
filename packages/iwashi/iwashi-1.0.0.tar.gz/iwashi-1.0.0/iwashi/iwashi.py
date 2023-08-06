from typing import List, MutableSet, Optional
from .visitor import Visitor, SiteVisitor, Context, Result
from .helper import parse_host

class Iwashi(Visitor):
    def __init__(self) -> None:
        self.visitors: List[SiteVisitor] = []
        self.visited: MutableSet[str] = set()

    def add_visitor(self, visitor: SiteVisitor) -> None:
        self.visitors.append(visitor)

    def is_visited(self, url: str) -> bool:
        return url in self.visited

    def mark_visited(self, url: str) -> bool:
        url = url.lower()
        if self.is_visited(url):
            return False
        self.visited.add(url)
        return True

    def visit(self, url: str, context: Optional[Context] = None) -> Optional[Result]:
        context = context or Context(url=url, visitor=self)
        for visitor in self.visitors:
            match = visitor.match(url, context)
            if match is None:
                continue

            normalized = visitor.normalize(url)
            if self.mark_visited(normalized):
                match = visitor.match(normalized, context)
                if match is not None:
                    visitor.visit(normalized, context, **match.groupdict())
            elif context.parent is not None:
                context.parent.link(normalized)
            break
        else:
            context.create_result(site_name=parse_host(url), url=url, score=1.0)
            self.mark_visited(url)
            print('[Iwashi]', '[No Visitor Found]', url)

        return context.result

def visit(url: str, iwashi: Optional[Iwashi] = None) -> Optional[Result]:
    if iwashi is None:
        iwashi = Iwashi()
        from . import visitors
        for attr in dir(visitors):
            value = getattr(visitors, attr)
            if attr.startswith('_'):
                continue
            if isinstance(value, type) and issubclass(value, SiteVisitor):
                iwashi.add_visitor(value())

    return iwashi.visit(url)