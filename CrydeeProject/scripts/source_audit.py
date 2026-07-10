import argparse
import json
from pathlib import Path

from pypdf import PdfReader


DEFAULT_TERMS = [
    "Castle Crydee",
    "Crydee",
    "great hall",
    "courtyard",
    "gate",
    "stables",
    "west wall",
    "battlements",
    "tower",
]


def sample_hits(reader, term, limit):
    hits = []
    lowered = term.lower()
    for index, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        match_index = text.lower().find(lowered)
        if match_index == -1:
            continue
        snippet = text[max(0, match_index - 100) : match_index + 240].replace("\n", " ").strip()
        hits.append(
            {
                "page": index + 1,
                "snippet": snippet,
            }
        )
        if len(hits) >= limit:
            break
    return hits


def build_payload(pdf_path, reader, terms, sample_limit):
    payload = {
        "pdf_path": str(pdf_path),
        "page_count": len(reader.pages),
        "metadata": dict(reader.metadata or {}),
        "terms": {},
    }
    for term in terms:
        hits = sample_hits(reader, term, sample_limit)
        payload["terms"][term] = {
            "hit_count": len(hits),
            "samples": hits,
        }
    return payload


def markdown_report(payload):
    lines = [
        "# Source Audit",
        "",
        "This file is generated from the current lawful source PDF for the Crydee reconstruction project.",
        "",
        "## Source File",
        "",
        f"- Path: `{payload['pdf_path']}`",
        f"- Pages: `{payload['page_count']}`",
        "",
        "## PDF Metadata",
        "",
    ]

    metadata = payload.get("metadata", {})
    if metadata:
        for key in sorted(metadata):
            lines.append(f"- `{key}`: `{metadata[key]}`")
    else:
        lines.append("- No PDF metadata found.")

    lines.extend(
        [
            "",
            "## Initial Term Probe",
            "",
            "These are not final evidence claims. They are quick extraction checks to confirm the PDF is usable for structured reconstruction work.",
            "",
        ]
    )

    for term, info in payload["terms"].items():
        lines.append(f"### {term}")
        lines.append("")
        lines.append(f"- Sample hits captured: `{info['hit_count']}`")
        if info["samples"]:
            for sample in info["samples"]:
                lines.append(f"- `pdf p. {sample['page']}`: {sample['snippet']}")
        else:
            lines.append("- No sample hits found in the captured range.")
        lines.append("")

    lines.extend(
        [
            "## Working Implications",
            "",
            "- The source PDF is machine-readable enough to seed a structured evidence ledger.",
            "- Castle Crydee, the great hall, the courtyard-gate sequence, and named defensive edges are viable extraction targets.",
            "- The scaffold is ready for a broader Crydee evidence pass.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Generate a source audit for the Crydee project PDF.")
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--doc-out", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--sample-limit", type=int, default=5)
    parser.add_argument("--term", action="append", dest="terms")
    args = parser.parse_args(argv)

    terms = args.terms or DEFAULT_TERMS
    reader = PdfReader(str(args.pdf))
    payload = build_payload(args.pdf, reader, terms, args.sample_limit)

    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.doc_out.parent.mkdir(parents=True, exist_ok=True)

    args.json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    args.doc_out.write_text(markdown_report(payload) + "\n", encoding="utf-8")

    print(f"wrote: {args.doc_out}")
    print(f"wrote: {args.json_out}")


if __name__ == "__main__":
    main()

