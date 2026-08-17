#!/usr/bin/env python3
"""Post-process pandoc HTML: journal CSS + MathJax CDN."""
import re
import sys
from pathlib import Path

CSS = """
body{font-family:Georgia,"Times New Roman",serif;font-size:11.5pt;line-height:1.45;max-width:42rem;margin:2rem auto;padding:0 1.25rem;color:#111}
h1,h2,h3,h4{font-family:Helvetica,Arial,sans-serif;line-height:1.25}
h1{font-size:1.45rem}
h2{font-size:1.15rem;margin-top:1.6rem}
h3{font-size:1.02rem}
p{margin:0.7em 0}
table{border-collapse:collapse;font-size:0.92em;margin:1em 0;width:100%}
th,td{border:1px solid #ccc;padding:0.35em 0.5em;text-align:left;vertical-align:top}
th{background:#f3f3f3}
caption{caption-side:bottom;font-size:0.9em;color:#333;padding-top:0.4em}
code,pre{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:0.88em}
pre{background:#f6f6f6;padding:0.75em;overflow:auto}
blockquote{border-left:3px solid #444;margin-left:0;padding-left:1em;color:#222}
.abstract{font-size:0.98em}
@media (max-width:640px){body{font-size:11pt}}
"""

def main() -> None:
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    html = src.read_text(encoding="utf-8")
    html = html.replace("https://polyfill.io/v3/polyfill.min.js?features=es6", "")
    if "cdn.jsdelivr.net/npm/mathjax" not in html:
        html = html.replace(
            "</head>",
            '<script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n</head>',
            1,
        )
    if "<style>" not in html:
        html = html.replace("</head>", f"<style>{CSS}</style>\n</head>", 1)
    html = re.sub(r'<embed[^>]+>', '', html)
    dst.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    main()
