"""
cli.py
Owner: Member 3 (CLI + Ethics Lead)

This is the entry point: run `python cli.py` to use the tool.

Already includes the 3 ethical guardrails required by the brief:
- Legal disclaimer + Computer Crimes Act confirmation
- Safe default target (localhost only, unless explicitly overridden)
- Kill switch (Ctrl+C handled cleanly)

TODO (Member 3):
- Add --context, --technique, --target as real argparse flags
  (right now context is hardcoded to "html_body" to keep this
  version simple and WORKING first)
- Add the "--i-have-authorization" flag + extra confirmation
  for any target that isn't localhost/127.0.0.1/example.com
- Make sure output gets written to ./output/ (per .gitignore),
  never printed-only or sent anywhere else
"""

import sys
import argparse

from payload_bank import get_payloads
from mutators import apply_mutation

DISCLAIMER = """
==================== LEGAL DISCLAIMER ====================
This tool generates Cross-Site Scripting (XSS) test payloads
for AUTHORIZED ethical hacking / security testing ONLY.

Unauthorized use against systems you do not own or do not have
explicit written permission to test is a criminal offence under
the Computer Crimes Act 1997 (Malaysia) and equivalent laws in
other jurisdictions.

By continuing, you confirm that you have explicit authorization
to test the target you intend to use this tool against.
============================================================
"""

SAFE_DEFAULT_TARGETS = ("127.0.0.1", "localhost", "example.com")


def confirm_authorization() -> bool:
    """Show the disclaimer and require an explicit typed confirmation."""
    print(DISCLAIMER)
    answer = input("Type 'I AGREE' to confirm you are authorized to proceed: ")
    return answer.strip().upper() == "I AGREE"


def main():
    parser = argparse.ArgumentParser(
        description="XSS Payload Generator (prototype v0.1 - bare bones)"
    )
    parser.add_argument(
        "--target",
        default="127.0.0.1",
        help="Target host (defaults to a safe local test target).",
    )
    args = parser.parse_args()

    # --- Guardrail 1: legal disclaimer + confirmation ---
    if not confirm_authorization():
        print("[!] Authorization not confirmed. Exiting.")
        sys.exit(1)

    # --- Guardrail 2: safe default target enforcement ---
    if args.target not in SAFE_DEFAULT_TARGETS:
        print(
            f"[!] Target '{args.target}' is not a recognised safe default "
            f"({SAFE_DEFAULT_TARGETS}).\n"
            f"    This prototype does not yet support real targets. Exiting."
        )
        sys.exit(1)

    print(f"[*] Target confirmed as safe: {args.target}")

    # --- Core logic: get a payload, "mutate" it (passthrough for now) ---
    try:
        payloads = get_payloads("html_body")
        for raw_payload in payloads:
            result = apply_mutation(raw_payload, technique="none")
            print(f"[+] Generated payload: {result}")
    except (ValueError, NotImplementedError) as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # --- Guardrail 3: kill switch ---
        print("\n[!] Kill switch triggered (Ctrl+C). Aborting cleanly.")
        sys.exit(0)
