"""Small dependency-free PDF renderer for case investigation exports."""

from datetime import date
import re


def _pdf_escape(value: str) -> str:
    value = value.encode("cp1252", errors="replace").decode("cp1252")
    return value.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def _wrap(text: str, width: int = 92):
    clean = re.sub(r"[\\*_`#]", "", text)
    clean = re.sub(r"\s+", " ", clean).strip().encode("cp1252", errors="replace").decode("cp1252")
    return [clean[i:i + width] for i in range(0, len(clean), width)] or [""]


def _section(content: str, heading: str) -> str:
    headings = list(re.finditer(r"(?im)^#{1,3}\s*(.*?)\s*$", content or ""))
    for index, match in enumerate(headings):
        if match.group(1).strip().lower() == heading.lower():
            end = headings[index + 1].start() if index + 1 < len(headings) else len(content)
            return content[match.end():end].strip()
    return ""


def build_report_pdf(report: dict) -> bytes:
    """Build a paginated text-first PDF with only verified case input."""
    lines = [
        "MECHLEDGER  /  MAINTENANCE INVESTIGATION",
        "Industrial Knowledge & Diagnostics",
        "",
        f"Report date: {date.today().isoformat()}",
        f"Case: {report.get('case_title') or 'Untitled investigation'}",
        "",
        "EQUIPMENT DETAILS",
    ]
    equipment = report.get("equipment") or {}
    fields = [("Equipment", "equipment"), ("Manufacturer", "manufacturer"), ("Model", "model"), ("Asset ID", "asset")]
    for label, key in fields:
        lines.append(f"{label}: {equipment.get(key) or 'Not provided'}")
    lines += ["", "REPORTED PROBLEM"]
    lines += _wrap(report.get("problem") or "No problem statement was recorded.")
    messages = report.get("messages") or []
    assistant_notes = [item.get("content", "") for item in messages if item.get("role") == "assistant"]
    lines += ["", "INVESTIGATION SUMMARY"]
    summaries = [_section(note, "Problem summary") for note in assistant_notes]
    summaries = [part for part in summaries if part]
    lines += _wrap("\n".join(summaries) or report.get("problem") or "No investigation summary was recorded.")
    lines += ["", "POSSIBLE CAUSES AND EVIDENCE"]
    causes = [_section(note, "Possible causes") for note in assistant_notes]
    lines += _wrap("\n".join(part for part in causes if part) or "No cause was established in the investigation responses.")
    lines += ["", "DOCUMENTED INSPECTION STEPS"]
    checks = [_section(note, "Documented inspection steps") for note in assistant_notes]
    lines += _wrap("\n".join(part for part in checks if part) or "No documented inspection steps were recorded.")
    lines += ["", "SUPPORTING DOCUMENTATION"]
    docs = report.get("documents") or []
    if docs:
        for name in docs:
            lines.extend(_wrap(name))
    else:
        lines.append("No source documents were indexed for this case.")
    citations = []
    for note in assistant_notes:
        citations.extend(re.findall(r"\[View Source:\s*([^\]]+)\]\((?:<)?([^)>]+)(?:>)?\)", note))
    for citation, link in citations:
        lines += _wrap(f"{citation} — {link}")
    lines += ["", "SAFETY NOTES"]
    safety = [_section(note, "Safety") for note in assistant_notes]
    lines += _wrap("\n".join(part for part in safety if part) or "No document-specific safety notes were recorded.")
    lines += _wrap("Follow current controlled OEM instructions and approved site safety procedures.")
    lines += ["", "CONCLUSION"]
    lines += _wrap("This report records the investigation; no cause is confirmed unless verified against the cited source and field inspection.")
    lines += ["", "INVESTIGATION HISTORY"]
    if not messages:
        lines.append("No investigation responses are available.")
    for item in messages:
        role = "Reported condition" if item.get("role") == "user" else "Investigation response"
        lines.append("")
        lines.append(role.upper())
        lines += _wrap(item.get("content", ""))
    lines += ["", "ENGINEER REMARKS"]
    lines += _wrap(report.get("remarks") or "No engineer remarks provided.")

    pages = [lines[i:i + 48] for i in range(0, len(lines), 48)] or [[]]
    objects = [b""]
    page_ids, content_ids = [], []
    for _ in pages:
        page_ids.append(len(objects)); objects.append(b"")
        content_ids.append(len(objects)); objects.append(b"")
    font_id = len(objects); objects.append(b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    pages_id = len(objects); objects.append(b"")
    for index, page_lines in enumerate(pages):
        commands = ["BT", "/F1 9 Tf", "48 748 Td", "12 TL"]
        for line_index, line in enumerate(page_lines):
            if line_index == 0 and (index > 0 or line.startswith("MECHLEDGER")):
                commands.append("/F1 13 Tf")
                commands.append(f"({_pdf_escape(line)}) Tj")
                commands.append("/F1 9 Tf")
            else:
                commands.append(f"({_pdf_escape(line)}) Tj")
            commands.append("T*")
        commands.append("ET")
        stream = "\n".join(commands).encode("cp1252", errors="replace")
        objects[content_ids[index]] = b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream"
        objects[page_ids[index]] = (
            f"<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 612 792] "
            f"/Resources << /Font << /F1 {font_id} 0 R >> >> /Contents {content_ids[index]} 0 R >>"
        ).encode()
    kids = " ".join(f"{identifier} 0 R" for identifier in page_ids)
    objects[pages_id] = f"<< /Type /Pages /Kids [{kids}] /Count {len(pages)} >>".encode()
    catalog_id = len(objects)
    objects.append(f"<< /Type /Catalog /Pages {pages_id} 0 R >>".encode())

    pdf = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for object_id, body in enumerate(objects[1:], start=1):
        offsets.append(len(pdf))
        pdf.extend(f"{object_id} 0 obj\n".encode()); pdf.extend(body); pdf.extend(b"\nendobj\n")
    xref = len(pdf)
    pdf.extend(f"xref\n0 {len(objects)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        pdf.extend(f"{offset:010d} 00000 n \n".encode())
    pdf.extend(f"trailer\n<< /Size {len(objects)} /Root {catalog_id} 0 R >>\nstartxref\n{xref}\n%%EOF".encode())
    return bytes(pdf)
