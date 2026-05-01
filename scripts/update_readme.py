#!/usr/bin/env python3
"""
Scans the reported/ and patches/ directories for CVE markdown files,
extracts CVE ID, description, and severity, then rewrites the
Reported and Patched tables in README.md automatically.
"""

import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
README_PATH = os.path.join(REPO_ROOT, "README.md")
REPORTED_DIR = os.path.join(REPO_ROOT, "reported")
PATCHES_DIR = os.path.join(REPO_ROOT, "patches")


def extract_info(filepath: str) -> dict:
    """Return {cve_id, description, severity} parsed from a CVE markdown file."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    # CVE ID from filename (most reliable source)
    filename = os.path.basename(filepath)
    cve_id = re.sub(r"\.md$", "", filename, flags=re.IGNORECASE)

    # Description: grab from the first level-1 heading, strip the CVE prefix
    description = ""
    heading_match = re.search(r"^#\s+(?:CVE-[\d-]+\s*[—–-]+\s*)?(.*)", content, re.MULTILINE)
    if heading_match:
        description = heading_match.group(1).strip()

    # Severity: look for bold label **Severity:** value (same line or next word)
    severity = "N/A"
    sev_match = re.search(
        r"\*\*Severity:\*\*\s*([^\n|]+)", content, re.IGNORECASE
    )
    if sev_match:
        severity = sev_match.group(1).strip().rstrip("\\").strip()

    return {"cve_id": cve_id, "description": description, "severity": severity}


def build_table(entries: list, folder: str) -> str:
    """Build a markdown table string from a list of entry dicts."""
    lines = [
        "| CVE | Description | Severity |",
        "|-----|-------------|----------|",
    ]
    for e in entries:
        cve_link = f"[{e['cve_id']}]({folder}/{e['cve_id']}.md)"
        lines.append(f"| {cve_link} | {e['description']} | {e['severity']} |")
    # trailing newline preserves the blank line before the next `---` separator
    return "\n".join(lines) + "\n"


def collect_entries(directory: str) -> list:
    """Return sorted list of entry dicts for all CVE .md files in a directory."""
    entries = []
    if not os.path.isdir(directory):
        return entries
    for fname in sorted(os.listdir(directory)):
        if re.match(r"CVE-\d+-\d+\.md$", fname, re.IGNORECASE):
            fpath = os.path.join(directory, fname)
            entries.append(extract_info(fpath))
    return entries


def update_readme(reported_entries: list, patched_entries: list) -> None:
    """Replace the Reported and Patched tables in README.md."""
    with open(README_PATH, encoding="utf-8") as f:
        readme = f.read()

    reported_table = build_table(reported_entries, "reported")
    patched_table = build_table(patched_entries, "patches")

    # Pattern: from the table header row up to (but not including) the next heading or end
    table_pattern = r"(\| CVE \| Description \| Severity \|.*?)(?=\n---|\n##|\Z)"

    tables_found = re.findall(table_pattern, readme, flags=re.DOTALL)
    if len(tables_found) < 2:
        print("ERROR: Could not locate both tables in README.md", file=sys.stderr)
        sys.exit(1)

    # Replace first table occurrence (Reported), then second (Patched)
    new_readme = readme
    # Use a counter-based replacement to replace occurrences independently
    count = [0]

    def replacer(m):
        count[0] += 1
        if count[0] == 1:
            return reported_table
        return patched_table

    new_readme = re.sub(table_pattern, replacer, readme, flags=re.DOTALL)

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme)

    print(f"README.md updated: {len(reported_entries)} reported, {len(patched_entries)} patched.")


def main():
    reported = collect_entries(REPORTED_DIR)
    patched = collect_entries(PATCHES_DIR)
    update_readme(reported, patched)


if __name__ == "__main__":
    main()
