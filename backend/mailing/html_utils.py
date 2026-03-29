import re


def extract_substitutions(html: str) -> set:
    return set(re.findall(r'\{(\w+)\}', html))


def extract_cids(html: str) -> set:
    return set(re.findall(r'cid:(\w+)', html))
