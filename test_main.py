import pytest
from main import char_type, string_to_regex, list_regex_patterns, merge_regex_patterns

@pytest.mark.parametrize("char,expected", [
    ("a", r"[a-z]"),
    ("Z", r"[A-Z]"),
    ("5", r"\d"),
    (" ", r"\s"),
    ("!", r"!"),
])
def test_char_type(char, expected):
    assert char_type(char) == expected

@pytest.mark.parametrize("string,expected", [
    ("apple", r"[a-z]{5}"),
    ("apricot", r"[a-z]{7}"),
    ("banana", r"[a-z]{6}"),
    ("blueberry", r"[a-z]{9}"),
    ("cherry", r"[a-z]{6}"),
    ("X99!!", r"[A-Z]\d{2}!{2}"),
])
def test_string_to_regex(string, expected):
    assert string_to_regex(string) == expected
    

def test_list_regex_patterns():
    strings = ["apple", "banana"]
    expected = [r"[a-z]{5}", r"[a-z]{6}"]
    assert list_regex_patterns(strings) == expected

def test_merge_regex_patterns_simple_range():
    patterns = [r"[a-z]{5}", r"[a-z]{6}", r"[a-z]{7}"]
    merged = merge_regex_patterns(patterns)
    assert merged == r"^[a-z]{5,7}$"

def test_merge_regex_patterns_mixed():
    patterns = [r"[a-z]{5}", r"[a-z]{9}", r"[A-Z]\d{2}!{2}"]
    merged = merge_regex_patterns(patterns)
    assert merged.startswith("^")
    assert merged.endswith("$")
    assert "[a-z]{5,9}" in merged
    assert "[A-Z]\\d{2}!{2}" in merged
