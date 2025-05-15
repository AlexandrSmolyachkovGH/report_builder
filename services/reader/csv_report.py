from typing import Dict, List

from services.reader.base import BaseCSVDataReader
from services.reader.types.csv_report_types import csv_report_types


class CSVEmployeeDataReader(BaseCSVDataReader):
    _field_option = 2

    def __init__(self, paths: List[str], file_type: str):
        self.filepath = paths
        self.headers = []
        self.body = {}
        self._allowed_fields = None
        self._file_type = file_type

    def read(self) -> Dict:
        """Extract rows from CSV. Return processed information."""
        self._check_files()

        for file_path in self.filepath:
            with open(file_path, 'r', encoding='utf-8') as f:
                header_line = f.readline()
                if not header_line:
                    raise ValueError("CSV file is empty")

                self.headers = header_line.strip().split(',')
                self._check_report_type()
                self._validate_fields()

                for line in f:
                    line = self._row_parse(line)
                    if not line:
                        break
                    self._parse_body(line)

        return self.body

    def _check_files(self) -> None:
        if len(self.filepath) == 0:
            raise AttributeError(
                "Have no files for processing"
            )

    def _check_report_type(self) -> None:
        if self._file_type != 'payout':
            raise ValueError(
                f"Incorrect report type"
            )

    def _get_allowed_fields(self) -> None:
        """Check and update actual allowed fields for report"""
        self._check_report_type()

        if self._allowed_fields is None or self._allowed_fields != csv_report_types[self._file_type]:
            self._allowed_fields = csv_report_types[self._file_type]

    def _validate_fields(self):
        """Check and update actual allowed fields for report"""
        if self._allowed_fields is None:
            self._get_allowed_fields()

        for header in self.headers:
            if header.lower() not in self._allowed_fields:
                raise ValueError(
                    f"Unexpected header field {header}"
                )

        fields_cnt = len(self._allowed_fields) - self._field_option
        if len(self.headers) != fields_cnt:
            raise ValueError(
                f"Count of received fields = {len(self.headers)}. Required count is {fields_cnt}."
            )

    def _parse_body(self, lst_line: list) -> None:
        """Add the line to the body into relevant department"""

        dct_line = dict(zip(self.headers, lst_line))
        department_type = dct_line.get('department', None)

        if department_type not in self.body:
            self.body[department_type] = [dct_line]
        else:
            self.body[department_type].append(dct_line)

    @staticmethod
    def _row_parse(line: str, delimiter: str = ",") -> List[str]:
        """Return split string in the list"""

        if '"' not in line:
            return line.split(delimiter)

        else:
            result = []
            current = ''
            in_quotes = False
            i = 0

            while i < len(line):
                char = line[i]

                if char == '"':
                    if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                        current += '"'
                        i += 1
                    else:
                        in_quotes = not in_quotes

                elif char == delimiter and not in_quotes:
                    result.append(current)
                    current = ''
                else:
                    current += char

                i += 1

            result.append(current)
            return result
