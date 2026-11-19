"""
mutators.py
Owner: Member 2 (Bypass/Mutator Lead)

This is where the "advanced" part of the assignment lives - the
encoding/evasion transforms that turn a basic payload into something
that can slip past simple filters.

Right now this is just a STUB (does nothing / passes payload through
unchanged) so the rest of the pipeline runs without crashing.

TODO (Member 2), roughly in order of difficulty:
1. case_randomize()      - <ScRiPt> instead of <script>
2. html_entity_encode()  - &#x3C;script&#x3E;
3. event_handler_variant() - swap <script> for onerror=/onmouseover=
4. unicode_encode()      - UTF-7/UTF-8 trickery
5. filter_bypass_tricks()- missing quotes, alt parens, whitespace/null-byte tricks

Reference for technique IDEAS (not for copy-pasting payload strings):
https://swisskyrepo.github.io/PayloadsAllTheThings/XSS%20Injection
"""


def apply_mutation(payload: str, technique: str = "none") -> str:
    """
    Apply a bypass/encoding technique to a base payload.
    Currently only "none" is implemented (passthrough) - this proves
    the function signature/plumbing works before real logic is added.
    """
    if technique == "none":
        return payload

    # TODO: implement real techniques here, e.g.:
    # if technique == "case_random":
    #     return case_randomize(payload)

    raise NotImplementedError(
        f"Mutation technique '{technique}' not implemented yet."
    )
