import json
import csv
import re
from pathlib import Path

def categorize_evidence(text):
    """Categorize evidence based on content and certainty."""
    text_lower = text.lower()

    # Canon: Direct descriptions
    canon_indicators = [
        'the castle', 'crydee castle', 'castle crydee',
        'great hall', 'dining hall', 'kitchen', 'stables',
        'barracks', 'armory', 'chapel', 'dungeon',
        'tower', 'wall', 'gate', 'courtyard', 'keep'
    ]

    # Implied: Logical inferences
    implied_indicators = [
        'guards', 'soldiers', 'servants', 'nobles',
        'feasting', 'training', 'defense'
    ]

    # Reconstructed: Reasonable assumptions
    reconstructed_indicators = [
        'typical medieval castle', 'stone walls',
        'wooden doors', 'thatched roofs', 'arrow slits'
    ]

    if any(indicator in text_lower for indicator in canon_indicators):
        return 'canon'
    elif any(indicator in text_lower for indicator in implied_indicators):
        return 'implied'
    elif any(indicator in text_lower for indicator in reconstructed_indicators):
        return 'reconstructed'
    else:
        return 'unknown'

def extract_spatial_info(text):
    """Extract spatial/architectural information."""
    info = {
        'rooms': [],
        'features': [],
        'dimensions': [],
        'locations': []
    }

    # Extract room names
    room_patterns = [
        r'great hall', r'dining hall', r'kitchen', r'stables',
        r'barracks', r'armory', r'chapel', r'dungeon',
        r'tower', r'cellar', r'courtyard'
    ]

    for pattern in room_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        info['rooms'].extend(matches)

    # Extract features
    feature_patterns = [
        r'wall', r'gate', r'door', r'window', r'stair',
        r'fireplace', r'table', r'chair', r'bed'
    ]

    for pattern in feature_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        info['features'].extend(matches)

    return info

def process_evidence(raw_json_path, output_csv_path):
    """Process raw evidence into structured CSV."""
    with open(raw_json_path, 'r', encoding='utf-8') as f:
        sections = json.load(f)

    evidence_rows = []

    for i, section in enumerate(sections):
        text = section['text']
        certainty = categorize_evidence(text)
        spatial_info = extract_spatial_info(text)

        # Clean and truncate text for CSV
        clean_text = text.replace('\n', ' ').strip()
        if len(clean_text) > 500:
            clean_text = clean_text[:497] + '...'

        row = {
            'id': f'crydee_{i+1:03d}',
            'book': 'Magician',
            'page': section['page'],
            'certainty': certainty,
            'category': 'architecture',
            'description': clean_text,
            'rooms': ', '.join(set(spatial_info['rooms'])),
            'features': ', '.join(set(spatial_info['features'])),
            'notes': f'Extracted from page {section["page"]}'
        }

        evidence_rows.append(row)

    # Write to CSV
    fieldnames = ['id', 'book', 'page', 'certainty', 'category', 'description', 'rooms', 'features', 'notes']

    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(evidence_rows)

    print(f"Processed {len(evidence_rows)} evidence entries")
    print(f"Certainty breakdown:")
    certainties = {}
    for row in evidence_rows:
        certainties[row['certainty']] = certainties.get(row['certainty'], 0) + 1
    for cert, count in certainties.items():
        print(f"  {cert}: {count}")

if __name__ == "__main__":
    raw_json = Path(__file__).parent / "crydee_evidence_raw.json"
    output_csv = Path(__file__).parent / "evidence" / "crydee_evidence_ledger.csv"

    process_evidence(raw_json, output_csv)