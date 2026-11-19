"""
cli.py
Owner: Member 3 (CLI + Ethics Lead)

This is the entry point: run `python cli.py` to use the tool.

Already includes the 4 ethical guardrails required by the brief:
- Legal disclaimer + Computer Crimes Act confirmation
- Safe default target (localhost only, unless explicitly overridden)
- Kill switch (Ctrl+C handled cleanly)
- Data Handling: results saved locally to ./output/, never sent
  anywhere else - no network calls, no exfiltration

OPTIONAL TODO (Member 3):
- Add the "--i-have-authorization" flag + extra confirmation
  for any target that isn't localhost/127.0.0.1/example.com
"""

import sys
import os
import argparse
from datetime import datetime

from payload_bank import get_payloads, list_contexts
from mutators import apply_mutation

OUTPUT_DIR = "output"

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
        description="XSS Payload Generator (v1.0 - all planned bypass techniques implemented)"
    )
    parser.add_argument(
        "--target",
        default="127.0.0.1",
        help="Target host (defaults to a safe local test target).",
    )
    parser.add_argument(
        "--technique",
        default="none",
        choices=["none", "case_random", "html_entity", "unicode_encode", "filter_bypass"],
        help="Bypass technique to apply (default: none = plain payload).",
    )
    parser.add_argument(
        "--context",
        default="html_body",
        choices=list_contexts(),
        help="Injection context to generate payloads for (default: html_body).",
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
    print(f"[*] Using injection context: {args.context}")

    # --- Core logic: get payloads for the chosen context, mutate them ---
    try:
        payloads = get_payloads(args.context)
        generated = []

        for raw_payload in payloads:
            result = apply_mutation(raw_payload, technique=args.technique)
            print(f"[+] Generated payload: {result}")
            generated.append(result)

        # --- Guardrail 4 (Data Handling): write results to a LOCAL
        # output directory only. Nothing here is sent anywhere else -
        # no network calls, no external server, no exfiltration.
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{args.context}_{args.technique}_{timestamp}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"Target: {args.target}\n")
            f.write(f"Context: {args.context}\n")
            f.write(f"Technique: {args.technique}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write("-" * 40 + "\n")
            for payload in generated:
                f.write(payload + "\n")

        print(f"[*] Results saved locally to: {filepath}")

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
