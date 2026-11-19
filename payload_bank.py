"""
payload_bank.py
Owner: Member 1 (Payload Bank Lead)

Holds the base XSS payloads, organized by injection context.
Right now this only has ONE context + ONE payload, just to prove
the whole pipeline (bank -> cli -> output) actually works end to end.

TODO (Member 1):
- Add more contexts: "attribute", "js_string", "url_param", "css"
- Add multiple base payloads per context (not bypass-encoded yet,
  that's handled later by mutators.py)
- Keep payloads realistic but SAFE examples (no real victim data,
  no payloads that phone out to an external server)
"""

# Each context maps to a list of base (un-mutated) payloads.
PAYLOADS = {
    "html_body": [
        "<script>alert('XSS-test')</script>",
    ],
    # TODO: add "attribute", "js_string", "url_param" contexts here
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
