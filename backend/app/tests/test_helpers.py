import sys
from pathlib import Path

# Add backend root to sys.path so "app.*" imports work when running as a script
BACKEND_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BACKEND_ROOT))

from app.infra.utils.helpers import clean_text, format_price


def test_clean_text_removes_whitespace_and_newlines():
    raw = "  Hola \n mundo \t "
    result = clean_text(raw)
    assert result == "Hola  mundo"


def test_format_price_with_currency_and_commas():
    assert format_price("$1,200.00") == 1200.0


def test_format_price_with_plain_number():
    assert format_price("99.99") == 99.99


def test_format_price_invalid_value_returns_zero():
    assert format_price("abc") == 0.0


def run_all_tests():
    # Run tests manually
    test_clean_text_removes_whitespace_and_newlines()
    test_format_price_with_currency_and_commas()
    test_format_price_with_plain_number()
    test_format_price_invalid_value_returns_zero()


if __name__ == "__main__":
    run_all_tests()
    print("All tests passed ✅")
