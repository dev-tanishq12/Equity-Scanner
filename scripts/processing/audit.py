import csv

from scripts.config import RAW_DIR
from scripts.processing.schema import EXPECTED_COLUMNS


class DataAuditor:

    def __init__(self):
        self.raw_dir = RAW_DIR

    def audit(self):

        csv_files = sorted(self.raw_dir.glob("*.csv"))

        print("=" * 60)
        print("DATA AUDIT REPORT")
        print("=" * 60)

        print(f"CSV Files Found : {len(csv_files)}")
        print()

        readable = 0
        empty = 0
        schema_errors = 0
        corrupted = 0

        for file in csv_files:

            print(f"Checking: {file.name}")

            # Empty file check
            if file.stat().st_size == 0:
                empty += 1
                print("  -> Empty file")
                continue

            try:

                with open(file, "r", encoding="utf-8-sig") as f:

                    reader = csv.reader(f)
                    header = [col.strip() for col in next(reader)]

                expected = set(EXPECTED_COLUMNS)
                actual = set(header)

                missing = expected - actual
                extra = actual - expected

                if len(missing) == 0:

                    readable += 1

                else:

                    schema_errors += 1

                    print("  -> Schema Mismatch")

                    if missing:
                        print(f"     Missing Columns : {sorted(missing)}")

                    if extra:
                        print(f"     Extra Columns   : {sorted(extra)}")

            except Exception as e:

                corrupted += 1

                print("  -> Cannot Read File")

                print(f"     Error : {e}")

        print()
        print("=" * 60)
        print("AUDIT SUMMARY")
        print("=" * 60)

        print(f"Total CSV Files : {len(csv_files)}")
        print(f"Readable Files  : {readable}")
        print(f"Empty Files     : {empty}")
        print(f"Schema Errors   : {schema_errors}")
        print(f"Corrupted Files : {corrupted}")

        print("=" * 60)