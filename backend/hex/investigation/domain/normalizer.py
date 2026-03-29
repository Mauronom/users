import re

_STRIP_PREFIXES = {"sala", "festival", "teatre", "espai", "club", "associació", "associacio", "ateneu", "cicle"}


def normalize_name(name: str) -> str:
    s = re.sub(r"\s+", " ", name.strip()).lower()
    first_word = s.split(" ")[0] if s else ""
    if first_word in _STRIP_PREFIXES:
        s = s[len(first_word):].strip()
    return s
