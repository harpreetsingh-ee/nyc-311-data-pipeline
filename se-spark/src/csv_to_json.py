import csv
import json
import sys
from itertools import islice
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parents[1] / "data"
SOURCE_CSV = DATA_PATH / "311-service-requests-from-2010-to-present.csv"
NUM_ROWS = 1000


def read_rows(csv_path: Path, limit: int) -> list[dict]:
    csv.field_size_limit(sys.maxsize)
    with open(csv_path, newline="", encoding="utf-8") as f:
        return list(islice(csv.DictReader(f), limit))


def write_jsonl(rows: list[dict], path: Path) -> None:
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
    rows = read_rows(SOURCE_CSV, NUM_ROWS)
    out_path = DATA_PATH / f"311-service-requests-sample-{NUM_ROWS}.jsonl"
    write_jsonl(rows, out_path)
    print(f"Wrote {len(rows)} rows to {out_path}")


if __name__ == "__main__":
    main()
