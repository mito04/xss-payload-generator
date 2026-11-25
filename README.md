# XSS Payload Generator & Bypass Engine
  
A command-line tool for generating context-aware Cross-Site Scripting (XSS) test payloads, with a few basic encoding and evasion techniques layered on top so the payloads can get past naive input filters. Built for the Ethical Hacking Tool Development assignment (IKB31603, UniKL MIIT) by team Skibidi Kaboom.

## Attack Category

Web Application Attack — Cross-Site Scripting (XSS)

XSS happens when an attacker manages to inject script into content that a trusted web app later serves back to other users. If that content gets rendered by the browser without proper sanitization, the injected script runs as if it belongs to the trusted site, which opens the door to session hijacking, credential theft, defacement, and so on.

## What This Tool Actually Does

Most beginner XSS demos just throw `<script>alert()</script>` at everything and call it a day. We wanted ours to be a bit smarter than that. The tool is context-aware, meaning it understands that where your injection point lands changes which payload syntax will actually fire. Landing inside an HTML body needs a different approach than landing inside a tag attribute, a JS string, or a URL parameter, so the payload bank is organized around that. On top of the base payload, you can optionally apply an encoding or evasion technique to simulate getting past a simple keyword filter or a basic WAF rule.

## Attack Lifecycle Mapping

We mapped this to the Reconnaissance to Weaponization stages of the Cyber Kill Chain.

| Stage | How this tool fits |
|---|---|
| Reconnaissance | By the time you are using this tool, you have already found an injection point (search box, URL parameter, whatever) and figured out which context it reflects into. That context is what you feed into `--context`. |
| Weaponization | The tool builds and encodes a payload tailored to that context. This is weaponization in the ethical sense, building a proof of concept payload to demonstrate a vulnerability exists, not to cause actual damage. |
| Delivery (out of scope) | Actually sending the payload to a real target is deliberately blocked off by the guardrails below. We are not shipping a tool that can touch a real, unauthorized system. |

We stopped the tool right at Weaponization on purpose. It never performs Delivery, Exploitation, or anything past that against a real system, it only generates and prints or saves candidate payload strings.

## Installation

Needs Python 3.8 or newer. No external dependencies, just the standard library (argparse, random, os, sys, datetime).

```bash
git clone https://github.com/mito04/xss-payload-generator.git
cd xss-payload-generator
python cli.py --help
```

## Usage Examples

```bash
# default run, html_body context, no bypass technique
python cli.py

# target an HTML attribute injection point
python cli.py --context attribute

# apply case randomization
python cli.py --context html_body --technique case_random

# HTML entity encoding, aimed at a JS string context
python cli.py --context js_string --technique html_entity

# unicode escaping
python cli.py --context url_param --technique unicode_encode

# the filter bypass tricks, backtick calls plus comment whitespace
python cli.py --context attribute --technique filter_bypass
```

Every run makes you type `I AGREE` after reading the disclaimer first, confirming you actually have authorization for whatever target you have in mind. Payloads get printed to the console and also saved to `./output/` as a timestamped `.txt` file. Nothing here ever touches the network.

### Contexts (`--context`)
- `html_body` — payload lands straight into the page content
- `attribute` — payload lands inside a tag attribute value
- `js_string` — payload lands inside a JS string literal
- `url_param` — payload comes from a URL query parameter

### Techniques (`--technique`)
- `none` — raw payload, nothing applied
- `case_random` — randomizes letter casing
- `html_entity` — encodes characters as HTML entities
- `unicode_encode` — encodes characters as JS `\uXXXX` escapes
- `filter_bypass` — strips parentheses (via backtick calls) and spaces (via `/**/`)

## Proof of Concept

We tested manually against OWASP Juice Shop, a deliberately vulnerable practice app, running inside an isolated Kali VM, within the scope laid out in the Rules of Engagement below. The tool itself never connects to anything, each generated payload got copied by hand into Juice Shop's search field.

One thing that tripped us up during testing, `<script>` tags inserted through `innerHTML` never execute no matter what, that is just how browsers work, not something a filter is blocking. We also found out the `filter_bypass` technique's space to `/**/` swap can break the surrounding HTML tag structure in some cases rather than actually bypassing anything, which was a useful (if slightly annoying) thing to discover. Both of these are written up properly in the Technical Report.

## Ethical Considerations

We went in with the idea that a security tool is only as responsible as the guardrails built around it, so these are hardcoded rather than left up to whoever is running the tool.

- Explicit authorization confirmation, the tool refuses to run at all unless you read the disclaimer and type `I AGREE`
- Safe default targets only, anything other than `127.0.0.1`, `localhost`, or `example.com` gets rejected outright, there is no support yet for real arbitrary targets
- No network activity, no exfiltration, the tool only ever writes strings to a local file
- Kill switch, Ctrl+C aborts cleanly with no half-written state

## Rules of Engagement (RoE)

This tool is meant strictly for authorized testing and learning purposes.

- Scope — only `127.0.0.1`, `localhost`, and `example.com` are allowed targets in this version, anything else is blocked by the tool itself
- Time windows — since this is a local only tool with no scheduling built in, there is nothing to enforce here in code, but if this ever gets pointed at a real authorized target down the line, that should only happen within whatever window a signed engagement letter specifies
- Permitted techniques — generating and encoding payload strings for display or local storage, that is it
- Prohibited actions — running these payloads against any system without written authorization, or against production or third party systems you do not own
- Emergency stop — Ctrl+C at any point
- Data handling — everything stays local, nothing is ever sent off the machine

## Responsible Disclosure

This is not built to exploit anything live, it generates candidate payloads for a controlled, authorized environment such as a local DVWA or Juice Shop instance. If someone using this tool happens to stumble on a genuine XSS bug in a real third party system

1. Stop testing right away, do not try to push further
2. Report it privately to the system owner or their security team, never publicly, before a fix is out
3. Follow whatever disclosure policy the organization has published, a `security.txt` or bug bounty program if one exists
4. Give them a fair amount of time to fix it before saying anything public

## Legal Disclaimer

This tool generates XSS test payloads for authorized ethical hacking and security testing only. Using it against a system you do not own or do not have written permission to test is a criminal offence under the Computer Crimes Act 1997 (Malaysia), and under equivalent laws elsewhere. By using this tool you are confirming you have authorization for whatever target you intend to use it against. We take no responsibility for misuse.

## Limitations

- No actual "test against a live target" mode yet, it only generates and encodes, it never sends anything and verifies if it fired
- The payload bank and bypass list are not exhaustive, this is a prototype showing the approach, not a production grade scanner
- Techniques are applied one at a time right now, you cannot chain `html_entity` with `case_random` in a single run yet
- No WAF fingerprinting or adaptive technique selection, you pick the technique manually rather than the tool figuring out what would work

## License

MIT License, see [LICENSE](LICENSE)

## Team

Skibidi Kaboom — IKB31603 Ethical Hacking, UniKL MIIT
