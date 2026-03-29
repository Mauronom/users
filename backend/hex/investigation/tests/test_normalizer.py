from hex.investigation.domain.normalizer import normalize_name


def test_strips_sala_prefix():
    assert normalize_name("Sala Apolo") == "apolo"


def test_strips_festival_prefix():
    assert normalize_name("Festival Paupaterres") == "paupaterres"


def test_strips_teatre_prefix():
    assert normalize_name("Teatre Municipal de Vic") == "municipal de vic"


def test_strips_espai_prefix():
    assert normalize_name("Espai Jove La Bàscula") == "jove la bàscula"


def test_strips_club_prefix():
    assert normalize_name("Club Cultura") == "cultura"


def test_lowercases():
    assert normalize_name("HELIOGÀBAL") == "heliogàbal"


def test_strips_whitespace():
    assert normalize_name("  Apolo  ") == "apolo"


def test_collapses_inner_whitespace():
    assert normalize_name("La  Mirona") == "la mirona"


def test_no_prefix_unchanged():
    assert normalize_name("Paupaterres") == "paupaterres"


def test_empty_string():
    assert normalize_name("") == ""


def test_multiple_prefix_words_only_first_stripped():
    # "sala de concerts" → strip "sala" → "de concerts"
    assert normalize_name("Sala de Concerts La Nau") == "de concerts la nau"
