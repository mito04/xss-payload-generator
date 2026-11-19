# XSS Payload Generator & Bypass Engine

A command-line tool that generates context-aware Cross-Site Scripting (XSS) test payloads and applies encoding/evasion techniques to bypass naive input filters. Built for the **Ethical Hacking Tool Development** assignment (IKB31603, UniKL MIIT) by team **Skibidi Kaboom**.

## Attack Category

**Web Application Attack — Cross-Site Scripting (XSS)**

XSS is a client-side code injection attack where an attacker injects malicious script into content served by a trusted web application. When that content is rendered by a victim's browser without proper sanitization, the injected script executes in the context of the trusted site — allowing session hijacking, credential theft, defacement, and more.

## What This Tool Does

Rather than offering a single generic `<script>alert()</script>` payload, this tool is **context-aware**: it understands that where your injection point lands (HTML body, a tag attribute, a JavaScript string, a URL parameter) changes which payload syntax will actually execute. On top of that, it applies **bypass/evasion techniques** to the base payload, to simulate getting past simple filters or WAF rules that only look for obvious keywords.

## Attack Lifecycle Mapping

This tool maps to the **Reconnaissance → Weaponization** stages of the attack lifecycle (as commonly described in the Cyber Kill Chain):

| Stage | How this tool fits |
|---|---|
| **Reconnaissance** | The tester has already identified an injection point (e.g. a search box, a URL parameter) and determined which context it reflects into (HTML body, attribute, JS string, etc.) — this informs the `--context` choice. |
| **Weaponization** | The tool generates and encodes a payload tailored to that specific context and candidate filter. This is "weaponization" in the ethical sense: building a proof-of-concept payload to demonstrate the vulnerability, not to cause real harm. |
| **Delivery (out of scope)** | Actually delivering the payload to a real target is explicitly restricted by this tool's safe-default guardrails — see Rules of Engagement below. Delivery against a real, unauthorized target is never permitted. |

This tool deliberately stops at Weaponization. It does not perform Delivery, Exploitation, or any post-exploitation action against a real system — it only generates and prints/saves candidate payload strings.

## Installation

Requires Python 3.8+. No external dependencies — only the Python standard library is used (`argparse`, `random`, `os`, `sys`, `datetime`).

```bash
git clone https://github.com/<your-username>/xss-payload-generator.git
cd xss-payload-generator
python cli.py --help
```

## Usage Examples

```bash
# Basic run with defaults (html_body context, no bypass technique)
python cli.py

# Generate payloads for an HTML attribute injection point
python cli.py --context attribute

# Apply the case-randomization bypass technique
python cli.py --context html_body --technique case_random

# Apply HTML entity encoding, targeting a JS string context
python cli.py --context js_string --technique html_entity

# Apply unicode escaping
python cli.py --context url_param --technique unicode_encode

# Apply the filter-bypass tricks (backtick calls + comment whitespace)
python cli.py --context attribute --technique filter_bypass
```

Every run requires you to type `I AGREE` after reading the legal disclaimer, confirming you have explicit authorization for the target you intend to test. Generated payloads are printed to the console **and** saved locally to `./output/` as a timestamped `.txt` file — nothing is ever sent over the network or to an external server.

### Available contexts (`--context`)
- `html_body` — payload reflected directly into HTML page content
- `attribute` — payload reflected inside an HTML tag attribute value
- `js_string` — payload reflected inside a JavaScript string literal
- `url_param` — payload reflected from a URL query parameter

### Available techniques (`--technique`)
- `none` — raw payload, no encoding
- `case_random` — randomizes letter casing to evade case-sensitive filters
- `html_entity` — encodes characters as HTML entities to evade raw-text filters
- `unicode_encode` — encodes characters as JS `\uXXXX` escapes to evade JS-context filters
- `filter_bypass` — removes parentheses (via backtick calls) and spaces (via `/**/`) to evade character-blacklist filters

## Ethical Considerations

This tool was built around the principle that **a security tool is only as responsible as its guardrails**. XSS payload generation has obvious dual-use potential, so the following safeguards are built directly into the code rather than left to the user's discretion:

- **Explicit authorization confirmation**: the tool will not run at all unless the user reads a legal disclaimer and types `I AGREE`, confirming they are authorized to test the target.
- **Safe default targets only**: the tool refuses to proceed against any `--target` other than `127.0.0.1`, `localhost`, or `example.com`. It currently does not support testing real, arbitrary targets at all — this is a deliberate limitation, not an oversight (see Limitations below).
- **No network activity, no exfiltration**: the tool never makes an HTTP request or contacts any external server. It only generates strings and writes them to a local file.
- **Kill switch**: pressing Ctrl+C at any point aborts the tool cleanly, with no partial or corrupted state.

These choices reflect a "safe by default, explicit by exception" design: the tool starts in the most restrictive mode possible, and would require deliberate, visible code changes to ever target something other than a local/test environment.

## Rules of Engagement (RoE)

This tool is intended **strictly** for authorized security testing and educational purposes.

- **Scope**: Only localhost (`127.0.0.1`), `localhost`, and `example.com` are permitted targets in this version. Testing against any other system — including real, live websites — is explicitly out of scope and is blocked by the tool itself.
- **Time windows**: As a local-only tool with no scheduling component, there are no time-window restrictions enforced in code; however, any future use against a real authorized target should only occur within the time windows specified in a signed authorization/engagement letter.
- **Permitted techniques**: Generating and encoding XSS payload strings for display/local storage only.
- **Prohibited actions**: Using generated payloads against any system without explicit, written authorization from the system owner. Using this tool to target production systems, third-party services, or any system you do not own or have not been explicitly authorized to test.
- **Emergency stop**: Press `Ctrl+C` at any time to immediately and cleanly abort execution (kill switch).
- **Data handling**: All output stays local. No payload, target information, or result is ever transmitted off the machine running the tool.

## Responsible Disclosure

This tool is not designed to exploit live vulnerabilities — it generates candidate payload strings for use in a controlled, authorized testing environment (e.g. a local DVWA or OWASP Juice Shop instance). If a user of this tool discovers a genuine XSS vulnerability in a real, third-party system while using techniques inspired by this tool, they should:

1. Stop testing immediately and not attempt further exploitation.
2. Report the vulnerability privately to the system owner or their security team, never publicly, until it has been fixed.
3. Follow the target organization's published responsible disclosure policy, if one exists (e.g. via `security.txt` or a bug bounty program).
4. Allow a reasonable remediation period before any public disclosure.

## Legal Disclaimer

This tool generates Cross-Site Scripting (XSS) test payloads for **authorized ethical hacking / security testing only**. Unauthorized use against systems you do not own or do not have explicit written permission to test is a criminal offence under the **Computer Crimes Act 1997 (Malaysia)** and equivalent laws in other jurisdictions. By using this tool, you confirm that you have explicit authorization to test the target you intend to use it against. The developers accept no liability for misuse of this tool.

## Limitations

- Currently only supports generating/encoding payloads — it does not yet send a request to a live target and verify whether the payload actually executed (no real "test against target" feature yet; targets outside the safe-default list are rejected outright).
- The payload bank and bypass techniques, while varied, are not exhaustive — this is a prototype demonstrating the approach, not a production-grade security scanner.
- Encoding techniques are applied independently, not chained together (e.g. you cannot currently combine `html_entity` + `case_random` in a single run).
- No automated WAF-fingerprinting or adaptive bypass selection — the user manually picks a technique rather than the tool detecting what would work against a specific filter.

## License

MIT License — see [LICENSE](LICENSE) for details.

## Team

**Skibidi Kaboom** — IKB31603 Ethical Hacking, UniKL MIIT
