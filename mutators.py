import random


def case_randomize(payload: str) -> str:
    """Randomize the casing of letters in the payload."""
    result_chars = []

    for c in payload:
        if c.isalpha():
            result_chars.append(random.choice([c.lower(), c.upper()]))
        else:
            result_chars.append(c)

    return "".join(result_chars)


def html_entity_encode(payload: str) -> str:
    """Convert each character into its decimal HTML entity."""
    result_chars = []

    for c in payload:
        result_chars.append(f"&#{ord(c)};")

    return "".join(result_chars)


def unicode_encode(payload: str) -> str:
    """Convert each character into a JavaScript Unicode escape."""
    result_chars = []

    for c in payload:
        result_chars.append(f"\\u{ord(c):04x}")

    return "".join(result_chars)


def filter_bypass_tricks(payload: str) -> str:
    """Apply basic string replacements to the payload."""
    result = payload.replace("('", "`").replace("')", "`")
    result = result.replace(" ", "/**/")

    return result


def apply_mutation(payload: str, technique: str = "none") -> str:
    if technique == "none":
        return payload

    if technique == "case_random":
        return case_randomize(payload)

    if technique == "html_entity":
        return html_entity_encode(payload)

    if technique == "unicode_encode":
        return unicode_encode(payload)

    if technique == "filter_bypass":
        return filter_bypass_tricks(payload)

    raise NotImplementedError(
        f"Mutation technique '{technique}' not implemented yet."
    )
