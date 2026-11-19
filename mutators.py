"""
mutators.py
Owner: Member 2 (Bypass/Mutator Lead)

This is where the "advanced" part of the assignment lives - the
encoding/evasion transforms that turn a basic payload into something
that can slip past simple filters.

Implemented so far:
1. case_randomize()      - <ScRiPt> instead of <script>  [DONE]
2. html_entity_encode()  - &#x3C;script&#x3E;              [TODO]
3. event_handler_variant() - swap <script> for onerror=/onmouseover= [TODO]
4. unicode_encode()      - UTF-7/UTF-8 trickery             [TODO]
5. filter_bypass_tricks()- missing quotes, alt parens, whitespace/null-byte tricks [TODO]

Reference for technique IDEAS (not for copy-pasting payload strings):
https://swisskyrepo.github.io/PayloadsAllTheThings/XSS%20Injection
"""

import random


def case_randomize(payload: str) -> str:
    """
    Randomly upper/lower-cases each LETTER in the payload, leaving
    symbols like < > ( ) ' " unchanged.

    Why this works as a bypass: some naive filters only check for the
    exact lowercase string "<script>" - they miss "<ScRiPt>" even
    though browsers treat HTML tags as case-insensitive and will
    still execute it.

    Example: "<script>" -> "<ScRiPt>" (random each time you run it)
    """
    result_chars = []  # we build the new string one character at a time

    for c in payload:
        if c.isalpha():
            # It's a letter - randomly pick uppercase or lowercase version
            result_chars.append(random.choice([c.lower(), c.upper()]))
        else:
            # Not a letter (e.g. < > ( ) ' ") - leave it exactly as is
            result_chars.append(c)

    # Join the list of single characters back into one string
    return "".join(result_chars)


def apply_mutation(payload: str, technique: str = "none") -> str:
    """
    Apply a bypass/encoding technique to a base payload.
    """
    if technique == "none":
        return payload

    if technique == "case_random":
        return case_randomize(payload)

    # TODO: implement more techniques here as they're built, e.g.:
    # if technique == "html_entity":
    #     return html_entity_encode(payload)

    raise NotImplementedError(
        f"Mutation technique '{technique}' not implemented yet."
    )
