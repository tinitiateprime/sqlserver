#!/usr/bin/env python3
import re
import sys
from collections import OrderedDict

def extract_questions(text):
    """
    Parse the entire file text, group lines that look like '-- N. text'
    under the last seen '## Section' header.
    """
    sections = OrderedDict()
    current_section = None

    for line in text.splitlines():
        # Section header?
        sec = re.match(r'##\s+(.*)', line)
        if sec:
            current_section = sec.group(1).strip()
            sections[current_section] = []
            continue

        # SQL comment question?
        m = re.match(r'\s*--\s*\d+\.\s*(.*)', line)
        if m and current_section:
            sections[current_section].append(m.group(1).strip())

    return sections

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input.md> [output.md]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) >= 3 else None

    with open(input_path, 'r', encoding='utf-8') as f:
        text = f.read()

    sections = extract_questions(text)

    # Build output
    out_lines = []
    for sec, qs in sections.items():
        if not qs:
            continue
        out_lines.append(f"## {sec}")
        for i, q in enumerate(qs, 1):
            out_lines.append(f"{i}. {q}")
        out_lines.append("")  # blank line

    result = "\n".join(out_lines)

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Wrote extracted questions to {output_path}")
    else:
        print(result)

if __name__ == "__main__":
    main()
