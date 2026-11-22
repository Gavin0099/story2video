"""Check the lab's text artifacts; this does not approve story quality."""

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CARDS = {"26M", "41K", "58R", "67C", "73H", "94N"}


def check(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    cards = list((ROOT / "readers").glob("*.md"))
    check({p.stem for p in cards} == CARDS, "Reader card IDs differ")
    for path in cards:
        text = path.read_text(encoding="utf-8")
        check(text.splitlines()[0] == f"# {path.stem}", f"{path.name}: title")
        check(re.findall(r"^## (.+)$", text, re.M) == ["第一段", "第二段"],
              f"{path.name}: expected two ordered parts")
        check(all(part.strip() for part in re.split(r"^## .+$", text, flags=re.M)[1:]),
              f"{path.name}: empty part")

    reveal_ids = re.findall(r"^## (\w+)$", (ROOT / "reveals.md").read_text(encoding="utf-8"), re.M)
    check(Counter(reveal_ids) == Counter(CARDS), "Reveals must match cards once each")

    weights = [20, 25, 20, 15, 10, 10]
    scores = []
    for line in (ROOT / "editorial.md").read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 10 or cells[0] not in CARDS:
            continue
        values = list(map(int, cells[3:9]))
        check(len(values) == 6 and all(1 <= n <= 5 for n in values), f"{cells[0]}: score range")
        check(sum(n * w for n, w in zip(values, weights)) == int(cells[9]) * 5,
              f"{cells[0]}: weighted score mismatch")
        scores.append(cells[0])
    check(Counter(scores) == Counter(CARDS), "Editorial scores differ")

    link_count = 0
    for path in ROOT.rglob("*.md"):
        for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if re.match(r"[a-zA-Z][\w+.-]*:", link):
                continue
            target = link.split("#", 1)[0]
            check(not target or (path.parent / target).exists(), f"{path.name}: missing {link}")
            link_count += 1

    expected_header = None
    total_rows = 0
    counts = Counter()
    gates = Counter()
    for name in ["reader-record.csv", "reader-record-next.csv"]:
        with (ROOT / name).open(encoding="utf-8-sig", newline="") as source:
            rows = list(csv.reader(source))
        check(bool(rows), f"{name}: missing header")
        header, data = rows[0], rows[1:]
        check(len(header) == len(set(header)), f"{name}: duplicate columns")
        if expected_header is None:
            expected_header = header
        check(header == expected_header, f"{name}: header differs")
        for number, values in enumerate(data, 2):
            check(len(values) == len(header), f"{name}:{number}: column count")
            row = dict(zip(header, values))
            check(row["card_id"] in CARDS, f"{name}:{number}: card ID")
            check(row["track"] in {"puzzle", "shorts", "preference"}, f"{name}:{number}: track")
            check(row["leakage_check"] in {"PASS", "FAIL", "UNKNOWN"}, f"{name}:{number}: leakage")
            for field, low, high in [("confidence_pct", 0, 100), ("continue_1to5", 1, 5), ("emotion_1to5", 1, 5)]:
                if row[field]:
                    check(low <= float(row[field]) <= high, f"{name}:{number}: {field}")
            ref = row["transcript_ref"].split("#", 1)[0]
            check(bool(ref) and (ROOT / ref).is_file(), f"{name}:{number}: missing transcript")
            counts[row["reader_type"]] += 1
            for field in ["puzzle_gate", "shorts_gate"]:
                if row[field]:
                    check(row[field] in {"PASS", "FAIL", "PENDING"}, f"{name}:{number}: {field}")
                    gates[row[field]] += 1
        if name == "reader-record-next.csv":
            print(f"Next-round recorded rows: {len(data)}")
        total_rows += len(data)

    print(f"PASS: {len(cards)} cards, {len(reveal_ids)} reveals, {len(scores)} weighted scores, {link_count} local links")
    print(f"CSV: {len(expected_header)} columns; {total_rows} recorded rounds; reader types={dict(counts)}; gates={dict(gates)}")
    print("Structural checks only. Human comprehension, video content and market acceptance remain unverified.")


if __name__ == "__main__":
    main()
