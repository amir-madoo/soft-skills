import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "curriculum.json").read_text(encoding="utf-8"))
source_path = ROOT / data.get("sourceFile", "content/curriculum.md")
source = source_path.read_text(encoding="utf-8") if source_path.is_file() else ""
units = data.get("units", [])
caps = data.get("capstones", [])
unit_ids = [x.get("id") for x in units]
cap_ids = [x.get("id") for x in caps]
errors = []
if len(units) != 15:
    errors.append(f"Expected 15 units; found {len(units)}")
if len(caps) != 5:
    errors.append(f"Expected 5 capstones; found {len(caps)}")
if data.get("moduleCount") != 0 or data.get("lessonCount") != 0:
    errors.append("Module/lesson counts must reflect that the supplied source defines neither separately")
for label, ids in (("unit", unit_ids), ("capstone", cap_ids)):
    if any(not x for x in ids):
        errors.append(f"At least one {label} has a missing ID")
    if len(set(ids)) != len(ids):
        errors.append(f"Duplicate {label} IDs detected")
if [x.get("code") for x in units] != [f"U{i}" for i in range(1, 16)]:
    errors.append("Unit sequence is missing, out of order, or has a duplicate unit code")
if any(not x.get("title") or not isinstance(x.get("content"), str) or not x["content"].strip() for x in units + caps):
    errors.append("At least one curriculum item has missing title or source content")
if not (ROOT / data.get("sourceFile", "")).is_file():
    errors.append("Bundled source curriculum file is missing")
source_lines = source.splitlines()
source_units = []
source_caps = []
for i, line in enumerate(source_lines):
    match = re.match(r"^### (U\d+)\. (.+)$", line)
    if match:
        j = i + 1
        while j < len(source_lines) and not re.match(r"^### U\d+\.", source_lines[j]) and not source_lines[j].startswith("## "):
            j += 1
        source_units.append((match.group(1), match.group(2), "\n".join(source_lines[i + 1:j]).strip()))
    cap = re.match(r"^\*\*Capstone (\d+) . (.+?) \((\d+h)\):\*\* (.*)$", line)
    if cap:
        source_caps.append((f"capstone-{cap.group(1)}", cap.group(2), cap.group(3), cap.group(4)))
bundle_units = [(x.get("code"), x.get("title"), x.get("content", "")) for x in units]
bundle_caps = [(x.get("id"), x.get("title"), x.get("hours"), x.get("content", "")) for x in caps]
if source_units != bundle_units:
    errors.append("Unit bundle does not exactly match the source headings/content")
if source_caps != bundle_caps:
    errors.append("Capstone bundle does not exactly match the source briefs")
known_units = {x.get("code") for x in units}
corpus = json.dumps(data, ensure_ascii=False)
references = {f"U{n}" for n in re.findall(r"\bU(\d{1,2})\b", corpus)}
for ref in sorted(references - known_units):
    errors.append(f"Broken internal unit reference: {ref}")
urls = re.findall(r"https?://[^\s\]\)]+", corpus)
if any(not url.startswith("https://") for url in urls):
    errors.append("A curriculum resource URL is not HTTPS")
print(f"Separately named modules loaded: {data.get('moduleCount', 0)}")
print(f"Units loaded: {len(units)}")
print(f"Separate lessons loaded: {data.get('lessonCount', 0)}")
print(f"Capstones loaded: {len(caps)}")
print(f"Unique unit IDs: {len(set(unit_ids))} / {len(unit_ids)}")
print(f"Unique capstone IDs: {len(set(cap_ids))} / {len(cap_ids)}")
print(f"Internal unit references checked: {len(references)}")
print(f"Resource URL syntax checked: {len(urls)}")
print(f"Source-to-bundle unit/brief text matches: {len(source_units)} / {len(source_caps)}")
if errors:
    print("VALIDATION FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)
print("VALIDATION PASSED")
