"""Build nirf.json mapping JoSAA institute names → NIRF 2025 Engineering rank/score.

Reads the NIRF CSV (top 100) and matches against institutes appearing in data.json.
Emits nirf.json: { "IIT Madras": {"rank": 1, "score": 88.72}, ... }

Re-run after updating either source.
"""
import csv, json, re, sys

NIRF_CSV = "NIRF College Rankings 2025  - Sheet1.csv"
DATA_JSON = "data.json"
OUT = "nirf.json"

def clean_nirf_name(s: str) -> str:
    return re.sub(r"\s*More Details\s*\|\s*\|.*$", "", s).strip()

# Manual aliases: JoSAA institute name (as in data.json `i` field) → exact NIRF cleaned name.
# Only institutes that appear in JoSAA AND NIRF top 100 are listed.
ALIASES = {
    # IITs
    "IIT Madras": "Indian Institute of Technology Madras",
    "IIT Delhi": "Indian Institute of Technology Delhi",
    "IIT Bombay": "Indian Institute of Technology Bombay",
    "IIT Kanpur": "Indian Institute of Technology Kanpur",
    "IIT Kharagpur": "Indian Institute of Technology Kharagpur",
    "IIT Roorkee": "Indian Institute of Technology Roorkee",
    "IIT Hyderabad": "Indian Institute of Technology Hyderabad",
    "IIT Guwahati": "Indian Institute of Technology Guwahati",
    "IIT Varanasi": "Indian Institute of Technology (Banaras Hindu University) Varanasi",
    "IIT Indore": "Indian Institute of Technology Indore",
    "IIT Dhanbad": "Indian Institute of Technology (Indian School of Mines)",
    "IIT Patna": "Indian Institute of Technology Patna",
    "IIT Gandhinagar": "Indian Institute of Technology Gandhinagar",
    "IIT Mandi": "Indian Institute of Technology Mandi",
    "IIT Jodhpur": "Indian Institute of Technology Jodhpur",
    "IIT Ropar": "Indian Institute of Technology Ropar",
    "IIT Bhubaneswar": "Indian Institute of Technology Bhubaneswar",
    "IIT Jammu": "Indian Institute of Technology Jammu",
    "IIT Tirupati": "Indian Institute of Technology, Tirupati",
    "IIT Palakkad": "Indian Institute of Technology Palakkad",
    "IIT Bhilai": "Indian Institute of Technology Bhilai",
    "IIT Dharwad": "Indian Institute of Technology Dharwad",
    # IIT Goa — not in NIRF top 100

    # NITs
    "NIT, Tiruchirappalli": "National Institute of Technology Tiruchirappalli",
    "NIT, Rourkela": "National Institute of Technology Rourkela",
    "NIT Karnataka, Surathkal": "National Institute of Technology Karnataka, Surathkal",
    "NIT Calicut": "National Institute of Technology Calicut",
    "NIT, Warangal": "National Institute of Technology Warangal",
    "NIT Durgapur": "National Institute of Technology Durgapur",
    "NIT, Silchar": "National Institute of Technology Silchar",
    "NIT Patna": "National Institute of Technology Patna",
    "Dr. B R Ambedkar NIT, Jalandhar": "Dr. B R Ambedkar National Institute of Technology, Jalandhar",
    "Malaviya NIT Jaipur": "Malaviya National Institute of Technology",
    "Visvesvaraya NIT, Nagpur": "Visvesvaraya National Institute of Technology, Nagpur",
    "Motilal Nehru NIT Allahabad": "Motilal Nehru National Institute of Technology",
    "NIT Delhi": "National Institute of Technology Delhi",
    "Sardar Vallabhbhai NIT, Surat": "Sardar Vallabhbhai National Institute of Technology",
    "NIT, Srinagar": "National Institute of Technology Srinagar",
    "Maulana Azad NIT Bhopal": "Maulana Azad National Institute of Technology",
    "NIT, Jamshedpur": "National Institute of Technology, Jamshedpur",
    "NIT Meghalaya": "National Institute of Technology Meghalaya",
    "NIT, Kurukshetra": "National Institute of Technology Kurukshetra",
    "NIT Raipur": "National Institute of Technology, Raipur",
    "NIT Hamirpur": "National Institute of Technology Hamirpur",
    "NIT Puducherry": "National Institute of Technology Puducherry",

    # IIITs
    "Atal Bihari Vajpayee IIIT & Management Gwalior":
        "Atal Bihari Vajpayee Indian Institute of Information Technology and Management",

    # GFTIs / others in JoSAA
    "Indian Institute of Engineering Science and Technology, Shibpur":
        "Indian Institute of Engineering Science and Technology, Shibpur",
    "Sant Longowal Institute of Engineering and Technology":
        "Sant Longowal Institute of Engineering & Technology",
}


def main():
    # Load NIRF
    nirf_by_clean = {}
    with open(NIRF_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = clean_nirf_name(row["Name"])
            nirf_by_clean[name] = {
                "rank": int(row["Rank"]),
                "score": float(row["Score"]),
            }

    # Load JoSAA institutes
    with open(DATA_JSON, encoding="utf-8") as f:
        data = json.load(f)
    josaa_insts = sorted({r["i"] for r in data["rows"]})

    # Build mapping
    out = {}
    matched = 0
    unmatched_in_aliases = []
    for josaa_name, nirf_name in ALIASES.items():
        if josaa_name not in josaa_insts:
            print(f"WARN: alias key not in JoSAA data: {josaa_name!r}", file=sys.stderr)
        if nirf_name not in nirf_by_clean:
            unmatched_in_aliases.append((josaa_name, nirf_name))
            continue
        out[josaa_name] = nirf_by_clean[nirf_name]
        matched += 1

    if unmatched_in_aliases:
        print("Aliases pointing to NIRF names not found:", file=sys.stderr)
        for j, n in unmatched_in_aliases:
            print(f"  {j!r} -> {n!r}", file=sys.stderr)

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    print(f"Wrote {OUT}: {matched} JoSAA institutes matched to NIRF top 100")
    print(f"JoSAA institutes total: {len(josaa_insts)}")
    print(f"NIRF top 100 entries:   {len(nirf_by_clean)}")


if __name__ == "__main__":
    main()
