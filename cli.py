# sys lets us control how the program exits (e.g. exit with an error code)
import sys

# os lets us interact with the operating system - here, to create folders
import os

# argparse is Python's built-in tool for building a command-line interface
# (it turns things like "--target 127.0.0.1" typed in the terminal into
# usable Python variables)
import argparse

# datetime lets us grab the current date/time, used to timestamp our output files
from datetime import datetime

# Importing our own functions from the other two files in this project.
# get_payloads() fetches the base payloads for a chosen context.
# list_contexts() returns all the context names we currently support.
from payload_bank import get_payloads, list_contexts

# apply_mutation() applies a bypass/encoding technique to a payload.
from mutators import apply_mutation

# This is the folder name where we will save our generated results.
# Keeping it as a named constant (instead of typing "output" everywhere)
# means if we ever rename the folder, we only change it in ONE place.
OUTPUT_DIR = "output"

# A multi-line string (triple quotes) holding our legal disclaimer text.
# This gets printed to the screen every single time the tool is run,
# before anything else happens - this satisfies the "Legal Disclaimer"
# ethical requirement from the assignment brief.
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

# A tuple (an unchangeable list) of the ONLY targets this tool will allow
# by default. This satisfies the "Safe Defaults" ethical requirement -
# the tool refuses to run against anything outside this safe list.
SAFE_DEFAULT_TARGETS = ("127.0.0.1", "localhost", "example.com")


def confirm_authorization() -> bool:
    """Show the disclaimer and require an explicit typed confirmation."""
    # Print the disclaimer text defined above to the terminal screen.
    print(DISCLAIMER)

    # input() pauses the program and waits for the user to type something
    # and press Enter. Whatever they type gets stored in "answer".
    answer = input("Type 'I AGREE' to confirm you are authorized to proceed: ")

    # .strip() removes any accidental extra spaces at the start/end.
    # .upper() converts it to all-uppercase so "i agree" or "I Agree"
    # still counts as valid - we only care about the words, not the casing.
    # This line returns True if they typed it correctly, False otherwise.
    return answer.strip().upper() == "I AGREE"


def main():
    # Create the command-line argument parser. The "description" and
    # "epilog" text are just what gets shown if someone runs
    # "python cli.py --help" - it's documentation for the user, not logic.
    parser = argparse.ArgumentParser(
        description="XSS Payload Generator (v1.0 - all planned bypass techniques implemented)",
        epilog="""
Examples:
  python cli.py
  python cli.py --context attribute
  python cli.py --context html_body --technique case_random
  python cli.py --context js_string --technique html_entity
  python cli.py --context url_param --technique unicode_encode
  python cli.py --context attribute --technique filter_bypass

Every run requires typing 'I AGREE' to the legal disclaimer before any
payload is generated. Results are printed and saved locally to ./output/.
""",
        # This setting just tells argparse to print the epilog text above
        # exactly as written (with line breaks), instead of reformatting it.
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Defines the "--target" flag. If the user doesn't type --target at
    # all, it automatically becomes "127.0.0.1" (our safe default).
    parser.add_argument(
        "--target",
        default="127.0.0.1",
        help="Target host (defaults to a safe local test target).",
    )

    # Defines the "--technique" flag - which bypass/encoding method to use.
    # "choices" means argparse will AUTOMATICALLY reject any value typed
    # that isn't in this list (e.g. a typo), with a helpful error message.
    parser.add_argument(
        "--technique",
        default="none",
        choices=["none", "case_random", "html_entity", "unicode_encode", "filter_bypass"],
        help="Bypass technique to apply (default: none = plain payload).",
    )

    # Defines the "--context" flag - which injection context to generate
    # payloads for. The allowed choices are pulled dynamically from
    # list_contexts() in payload_bank.py, so if someone adds a new context
    # there later, this flag automatically allows it too - no need to
    # update this file.
    parser.add_argument(
        "--context",
        default="html_body",
        choices=list_contexts(),
        help="Injection context to generate payloads for (default: html_body).",
    )

    # This actually reads whatever the user typed in the terminal and
    # stores it in "args" - e.g. args.target, args.technique, args.context
    args = parser.parse_args()

    # --- Guardrail 1: legal disclaimer + confirmation ---
    # Call the function we wrote above. If it returns False (user didn't
    # type "I AGREE" correctly), print a message and stop the program
    # immediately using sys.exit(1) - the "1" means "exited due to an error".
    if not confirm_authorization():
        print("[!] Authorization not confirmed. Exiting.")
        sys.exit(1)

    # --- Guardrail 2: safe default target enforcement ---
    # Check if whatever target the user typed is NOT in our safe list.
    # If it's not safe, refuse to continue and explain why.
    if args.target not in SAFE_DEFAULT_TARGETS:
        print(
            f"[!] Target '{args.target}' is not a recognised safe default "
            f"({SAFE_DEFAULT_TARGETS}).\n"
            f"    This prototype does not yet support real targets. Exiting."
        )
        sys.exit(1)

    # If we reach this point, the target passed the safety check - let the
    # user know everything is good to proceed.
    print(f"[*] Target confirmed as safe: {args.target}")
    print(f"[*] Using injection context: {args.context}")

    # --- Core logic: get payloads for the chosen context, mutate them ---
    # try/except here means: "attempt this code, but if something goes
    # wrong in a way we expect (ValueError or NotImplementedError),
    # handle it gracefully instead of the whole program crashing."
    try:
        # Ask payload_bank.py for the list of base payloads matching
        # whatever context the user chose (e.g. "html_body", "attribute").
        payloads = get_payloads(args.context)

        # An empty list that we will fill with our final, mutated payloads
        # as we generate them below.
        generated = []

        # Loop through every base payload for this context one at a time.
        for raw_payload in payloads:
            # Apply whatever bypass technique the user chose (or "none"
            # for a plain, unmodified payload) using mutators.py.
            result = apply_mutation(raw_payload, technique=args.technique)

            # Show the generated payload to the user immediately on screen.
            print(f"[+] Generated payload: {result}")

            # Also save it into our "generated" list, so we can write
            # ALL of them to a file afterward.
            generated.append(result)

        # --- Guardrail 4 (Data Handling): write results to a LOCAL
        # output directory only. Nothing here is sent anywhere else -
        # no network calls, no external server, no exfiltration.

        # Create the "output" folder if it doesn't already exist.
        # exist_ok=True means: don't throw an error if the folder is
        # already there from a previous run.
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Build a timestamp string like "20261124_153045" (year, month,
        # day, hour, minute, second) so each run's output file has a
        # unique name and nothing gets accidentally overwritten.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Build the filename combining context + technique + timestamp,
        # e.g. "html_body_case_random_20261124_153045.txt"
        filename = f"{args.context}_{args.technique}_{timestamp}.txt"

        # Combine the folder name and filename into one full file path,
        # e.g. "output/html_body_case_random_20261124_153045.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        # Open that file in write mode ("w") - this creates the file if
        # it doesn't exist yet. "with" automatically closes the file
        # safely once we're done writing, even if something goes wrong.
        with open(filepath, "w", encoding="utf-8") as f:
            # Write a small header of metadata at the top of the file,
            # so anyone opening it later knows exactly what run produced it.
            f.write(f"Target: {args.target}\n")
            f.write(f"Context: {args.context}\n")
            f.write(f"Technique: {args.technique}\n")
            f.write(f"Generated: {timestamp}\n")
            f.write("-" * 40 + "\n")  # just a visual divider line

            # Write every generated payload on its own line.
            for payload in generated:
                f.write(payload + "\n")

        # Tell the user where their results were saved.
        print(f"[*] Results saved locally to: {filepath}")

    # If get_payloads() or apply_mutation() raised an error we expected
    # (e.g. unknown context, or a technique not implemented), catch it
    # here, print a clean message, and exit - instead of showing Python's
    # scary default crash/error screen.
    except (ValueError, NotImplementedError) as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


# This special check means: "only run main() if this file is being
# run directly (python cli.py), not if it's being imported elsewhere."
if __name__ == "__main__":
    try:
        # Actually start the program by calling the function defined above.
        main()
    except KeyboardInterrupt:
        # --- Guardrail 3: kill switch ---
        # KeyboardInterrupt is what Python raises when the user presses
        # Ctrl+C. Instead of letting that crash the program messily, we
        # catch it here and shut down cleanly with a clear message.
        print("\n[!] Kill switch triggered (Ctrl+C). Aborting cleanly.")
        sys.exit(0)  # "0" means "exited normally, no error"
