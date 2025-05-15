import argparse
from pathlib import Path

from services.builder.csv_report import PayoutReport
from services.reader.csv_report import CSVEmployeeDataReader

base_dir = Path.cwd()
files_dir = base_dir / "files_for_processing"
print(f"base_dir: {base_dir}")
print(f"files_dir: {files_dir}")


def run_builder():
    parser = argparse.ArgumentParser(
        description='Generate Reports',
    )
    parser.add_argument(
        '-F', '--files',
        nargs='+',
        help='Paths to CSV files',
    )
    parser.add_argument(
        "-R", "--report",
        required=True,
        help='Report type to generate',
        default='payout'
    )

    args = parser.parse_args()
    full_paths = [files_dir / filename for filename in args.files]

    csv_reader = CSVEmployeeDataReader(paths=full_paths, file_type=args.report)
    row_data = csv_reader.read()

    builder = PayoutReport()
    report = builder.build(data=row_data)

    print(report)


if __name__ == '__main__':
    run_builder()
