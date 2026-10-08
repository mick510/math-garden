import re
from pathlib import Path

INPUT = Path("commands.tex")
OUTPUT = Path("macros.html")


def convert_macros(tex):
    macros = {}

    # Match:
    # \newcommand{\R}{\mathbb{R}}
    # \newcommand{\abs}[1]{\left|#1\right|}
    pattern = re.compile(
        r"\\newcommand\{\\(\w+)\}(?:\[(\d+)\])?\{((?:[^{}]|\{[^{}]*\})*)\}"
    )

    for match in pattern.finditer(tex):
        name = match.group(1)
        num_args = int(match.group(2) or 0)
        definition = match.group(3)

        # Convert LaTeX backslashes to JavaScript strings
        definition = definition.replace("\\", "\\\\")

        if num_args:
            macros[name] = [definition, num_args]
        else:
            macros[name] = definition

    return macros


def generate_html(macros):
    lines = [
        "<script>",
        "MathJax = {",
        "  tex: {",
        "    macros: {",
    ]

    items = []

    for name, value in macros.items():
        if isinstance(value, list):
            definition, num_args = value
            items.append(
                f'      "{name}": ["{definition}", {num_args}]'
            )
        else:
            items.append(
                f'      "{name}": "{value}"'
            )

    lines.append(",\n".join(items))

    lines.extend([
        "    }",
        "  }",
        "};",
        "</script>",
        ""
    ])

    return "\n".join(lines)


tex = INPUT.read_text()
macros = convert_macros(tex)
html = generate_html(macros)
OUTPUT.write_text(html)

print(f"Converted {len(macros)} macros from {INPUT} → {OUTPUT}")
