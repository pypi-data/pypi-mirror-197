import random
import re
import string

from .visitor import Result

HTTP_REGEX = f'(https?://)?(www.)?'


def print_result(result: Result, indent_level=0):
    indent = indent_level * "    "
    print(f'{indent}{result.site_name}')
    print(f'{indent}│url  : {result.url}')
    print(f'{indent}│name : {result.title}')
    print(f'{indent}│score: {result.score}')
    print(f'{indent}│links : {result.links}')
    if result.description:
        print(f'{indent}│description: ' + result.description.replace("\n", "\\n"))
    for child in result.children:
        print_result(child, indent_level + 1)


def parse_host(url: str) -> str:
    match = re.search(r'(https?:\/\/)?(www\.)?(?P<host>[\w.]+)/', url)
    if match is None:
        return url
    return match.group('host')

def random_string(length: int) -> str:
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))