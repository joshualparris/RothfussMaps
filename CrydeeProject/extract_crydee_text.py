import pdfplumber
import re
import json
from pathlib import Path

def extract_castle_crydee_text(pdf_path):
    """Extract text related to Castle Crydee from the Magician PDF."""
    castle_keywords = [
        'castle', 'crydee', 'keep', 'tower', 'wall', 'gate', 'courtyard',
        'great hall', 'dining hall', 'kitchen', 'stables', 'barracks',
        'armory', 'chapel', 'dungeon', 'cellar', 'roof', 'battlements',
        'moat', 'drawbridge', 'portcullis', 'guard', 'soldier'
    ]

    extracted_sections = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            text = page.extract_text()
            if text:
                # Look for sections containing castle-related keywords
                lines = text.split('\n')
                current_section = []
                in_castle_section = False

                for line in lines:
                    line_lower = line.lower()
                    if any(keyword in line_lower for keyword in castle_keywords):
                        if not in_castle_section:
                            in_castle_section = True
                            current_section = []
                        current_section.append(line)
                    elif in_castle_section and line.strip():
                        # Continue collecting until we hit a blank line or new paragraph
                        current_section.append(line)
                    elif in_castle_section and not line.strip():
                        # End of section
                        if current_section:
                            extracted_sections.append({
                                'page': page_num + 1,
                                'text': '\n'.join(current_section)
                            })
                        in_castle_section = False
                        current_section = []

                # Don't forget the last section
                if current_section:
                    extracted_sections.append({
                        'page': page_num + 1,
                        'text': '\n'.join(current_section)
                    })

    return extracted_sections

if __name__ == "__main__":
    pdf_path = r"c:\Users\joshua.parris\OneDrive - Dubbo Christian School\Documents\03_Projects\RothfussGame\CrydeeProject\magician_file.pdf"
    sections = extract_castle_crydee_text(pdf_path)

    output_path = Path(__file__).parent / "crydee_evidence_raw.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)

    print(f"Extracted {len(sections)} sections related to Castle Crydee")
    print(f"Saved to: {output_path}")