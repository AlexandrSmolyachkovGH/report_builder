from services.builder.csv_report import PayoutReport
from services.builder.formats.payout_report import PayoutReportFormatter


def test_report_builder(reader_factory, sample_csv):
    reader = reader_factory(paths=[str(sample_csv)], file_type="payout")
    row_data = reader.read()
    assert isinstance(row_data, dict)
    builder = PayoutReport()
    report = builder.build(data=row_data)
    assert isinstance(report, str)
    assert report.endswith('===')


def test_formatter(reader_factory, sample_csv):
    reader = reader_factory(paths=[str(sample_csv)], file_type="payout")
    row_data = reader.read()

    formatter = PayoutReportFormatter()
    result = formatter.format_payout_report(data=row_data)
    assert isinstance(result, str)
    assert len(result) != 0
    assert result.endswith('===')


