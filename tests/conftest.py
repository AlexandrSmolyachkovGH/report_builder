import csv
import pytest
from pathlib import Path

from services.reader.csv_report import CSVEmployeeDataReader

files_dir = Path().cwd().parent / "files_for_processing"


@pytest.fixture(scope="session")
def sample_csv():
    files_dir.mkdir(parents=True, exist_ok=True)
    file_path = files_dir / "test_data.csv"

    with open(file_path, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["department", "id", "email", "name", "hours_worked", "rate"])
        writer.writerow(["HR", 101, "grace@example.com", "Grace Lee", 160, 45])
        writer.writerow(["Marketing", 102, "henry@example.com", "Henry Martin", 150, 35])
        writer.writerow(["HR", 103, "ivy@example.com", "Ivy Clark", 158, 38])

    yield file_path

    if file_path.exists():
        file_path.unlink()


@pytest.fixture(scope="session")
def wrong_csv():
    files_dir.mkdir(parents=True, exist_ok=True)
    file_path = files_dir / "wrong_data.csv"

    with open(file_path, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["brand", "type", "price"])
        writer.writerow(["bmb", "sport", "high"])
        writer.writerow(["lada", "city", "low"])

    yield file_path

    if file_path.exists():
        file_path.unlink()


@pytest.fixture
def reader_factory():
    def _create(paths, file_type):
        return CSVEmployeeDataReader(paths=paths, file_type=file_type)

    return _create
