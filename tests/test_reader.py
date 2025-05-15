import pytest
from contextlib import nullcontext as does_not_raise

headers = ["department", "id", "email", "name", "hours_worked", "rate"]


@pytest.mark.parametrize(
    "file_type, fixture_name, expectation",
    [
        ("payout", "sample_csv", does_not_raise()),
        ("other", "sample_csv", pytest.raises(ValueError)),
        ("payout", "wrong_csv", pytest.raises(ValueError)),
        ("payout", None, pytest.raises(AttributeError)),
    ]
)
def test_read_csv(file_type, fixture_name, expectation, request, reader_factory):
    if fixture_name is not None:
        file_path = request.getfixturevalue(fixture_name)
        paths = [str(file_path)]
    else:
        paths = []

    with expectation:
        reader = reader_factory(paths=paths, file_type=file_type)
        result = reader.read()

        assert isinstance(result, dict)
        assert len(result) > 0


def test_empty_paths(reader_factory):
    reader = reader_factory(paths=[], file_type="payout")
    with pytest.raises(AttributeError, match="Have no files for processing"):
        reader._check_files()


def test_wrong_report_type(reader_factory):
    reader = reader_factory(paths=[], file_type="other")
    with pytest.raises(ValueError, match="Incorrect report type"):
        reader._check_report_type()


def test_correct_data(reader_factory, sample_csv):
    reader = reader_factory(paths=[str(sample_csv)], file_type="payout")
    result = reader.read()
    assert isinstance(result, dict)
    assert isinstance(reader.headers, list)
    assert len(reader.headers) == 6
    assert all(header in reader.headers for header in headers)
