"""
mutators.py
Owner: Member 2 (Bypass/Mutator Lead)

This is where the "advanced" part of the assignment lives - the
encoding/evasion transforms that turn a basic payload into something
that can slip past simple filters.

Implemented so far:
1. case_randomize()      - <ScRiPt> instead of <script>    [DONE]
2. html_entity_encode()  - &#x3C;script&#x3E;               [DONE]
3. event_handler_variant() - swap <script> for onerror=/onmouseover= [TODO]
4. unicode_encode()      - UTF-7/UTF-8 trickery              [TODO]
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


def html_entity_encode(payload: str) -> str:
    """
    Converts every character in the payload into its decimal HTML
    entity form, e.g. '<' becomes '&#60;' and 'a' becomes '&#97;'.

    Why this works as a bypass: many naive filters scan the RAW text
    for literal characters like "<" or keywords like "script". If the
    payload is written out as HTML entities instead, the filter sees
    harmless-looking text like "&#60;&#115;&#99;..." and lets it
    through. The BROWSER, however, decodes HTML entities back into
    real characters when it renders the page in an HTML context - so
    "&#60;" becomes "<" again at render time and the tag still executes.

    Note: this only works when the payload lands somewhere the browser
    HTML-decodes it (e.g. straight into the HTML body). It won't help
    inside a JS string context, since JS doesn't auto-decode HTML
    entities - that's a job for a different technique.

    Example: "<script>" -> "&#60;&#115;&#99;&#114;&#105;&#112;&#116;&#62;"
    """
    result_chars = []

    for c in payload:
        # ord(c) converts the character to its numeric code point,
        # e.g. ord('<') == 60. We wrap that number in the HTML
        # decimal entity format: &#<number>;
        result_chars.append(f"&#{ord(c)};")

    return "".join(result_chars)


def apply_mutation(payload: str, technique: str = "none") -> str:
    """
    Apply a bypass/encoding technique to a base payload.
    """
    if technique == "none":
        return payload

    if technique == "case_random":
        return case_randomize(payload)

    if technique == "html_entity":
        return html_entity_encode(payload)

    # TODO: implement more techniques here as they're built, e.g.:
    # if technique == "event_handler":
    #     return event_handler_variant(payload)

    raise NotImplementedError(
        f"Mutation technique '{technique}' not implemented yet."
    )
