import re

def char_type(c):
    """Returns the regex token for the character type"""
    if c.isdigit():
        return r'\d'
    elif c.isalpha():
        if c.islower():
            return r'[a-z]'
        elif c.isupper():
            return r'[A-Z]'
        else:
            return r'[a-zA-Z]'
    elif c.isspace():
        return r'\s'
    else:
        return re.escape(c)

def string_to_regex(s: str) -> str:
    """Convert a single string into a compact regex pattern"""
    if not s:
        return ""

    pattern = []
    prev_type = char_type(s[0])
    count = 1

    for c in s[1:]:
        t = char_type(c)
        if t == prev_type:
            count += 1
        else:
            pattern.append(f"{prev_type}{{{count}}}" if count > 1 else prev_type)
            prev_type, count = t, 1

    pattern.append(f"{prev_type}{{{count}}}" if count > 1 else prev_type)
    return ''.join(pattern)

def sliding_window_regex(strings):
    """Generate regex for each string in list"""
    return [string_to_regex(s) for s in strings]

def merge_regex_patterns(patterns):
    """
    Merge regex patterns into one,
    compressing simple ranges like [a-z]{5}|[a-z]{6}|[a-z]{7} → [a-z]{5,7}.
    """
    # Group patterns by their base token (e.g. [a-z]) and length
    grouped = {}
    leftovers = []

    for p in patterns:
        m = re.fullmatch(r"(\[.*?\]|\\d|\\s|\\.|[A-Za-z])\{(\d+)\}", p)
        if m:
            base, length = m.group(1), int(m.group(2))
            grouped.setdefault(base, []).append(length)
        else:
            leftovers.append(p)

    merged = []
    for base, lengths in grouped.items():
        lengths = sorted(set(lengths))
        if len(lengths) == 1:
            merged.append(f"{base}{{{lengths[0]}}}")
        else:
            merged.append(f"{base}{{{min(lengths)},{max(lengths)}}}")

    merged.extend(leftovers)
    return "^" + "|".join(merged) + "$"

if __name__ == "__main__":
    strings = ['apple', 'apricot', 'banana', 'blueberry', 'cherry', 'X99!!']
    regexes = sliding_window_regex(strings)

    for s, r in zip(strings, regexes):
        print(f"{s:10} -> {r}")

    merged = merge_regex_patterns(regexes)
    print("\nMerged Pattern:\n", merged)
