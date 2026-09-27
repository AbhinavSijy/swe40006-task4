#!/usr/bin/env python3
"""csv-report: summarise the numeric columns of every CSV file in a folder."""

import argparse
import csv
import json
import logging
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("csv-report")


def summarise(path: Path) -> dict:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("file has no header row")
        values = {name: [] for name in reader.fieldnames}
        rows = 0
        for row in reader:
            rows += 1
            for name in values:
                try:
                    values[name].append(float(row[name]))
                except (TypeError, ValueError):
                    pass

    numeric = {
        name: {
            "count": len(nums),
            "min": min(nums),
            "max": max(nums),
            "mean": round(statistics.mean(nums), 2),
            "total": round(sum(nums), 2),
        }
        for name, nums in values.items()
        if nums
    }
    return {"file": path.name, "rows": rows, "numeric_columns": numeric}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="csv-report",
        description="Summarise numeric columns in CSV files and write a JSON report.",
    )
    parser.add_argument("--input", type=Path, default=Path("/data/input"),
                        help="folder containing .csv files")
    parser.add_argument("--output", type=Path, default=Path("/data/output"),
                        help="folder to write reports to")
    parser.add_argument("--log-level", default="INFO",
                        choices=["DEBUG", "INFO", "WARNING", "ERROR"])
    args = parser.parse_args(argv)

    logging.basicConfig(level=args.log_level, stream=sys.stdout,
                        format="%(asctime)s %(levelname)-7s %(message)s")
    log.info("csv-report starting (input=%s, output=%s)", args.input, args.output)

    if not args.input.is_dir():
        log.error("Input folder does not exist: %s", args.input)
        return 2
    files = sorted(args.input.glob("*.csv"))
    if not files:
        log.error("No .csv files found in %s", args.input)
        return 2

    results, skipped = [], []
    for path in files:
        try:
            summary = summarise(path)
        except (ValueError, UnicodeDecodeError, csv.Error) as exc:
            log.warning("Skipped %s: %s", path.name, exc)
            skipped.append(path.name)
            continue
        results.append(summary)
        log.info("Processed %s: %d rows, %d numeric column(s)",
                 path.name, summary["rows"], len(summary["numeric_columns"]))

    args.output.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report_path = args.output / f"report-{stamp}.json"
    report_path.write_text(json.dumps(
        {"generated_utc": stamp, "files": results, "skipped": skipped}, indent=2))
    log.info("Report written to %s", report_path)

    total = len(list(args.output.glob("report-*.json")))
    log.info("Output folder now holds %d report(s)", total)
    log.info("Finished: %d processed, %d skipped", len(results), len(skipped))
    return 1 if skipped else 0


if __name__ == "__main__":
    sys.exit(main())
