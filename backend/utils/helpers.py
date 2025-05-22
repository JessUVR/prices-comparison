import datetime

def clean_text(text: str) -> str:
    """
    Removes unnecessary spaces and characters like line breaks and tabs.
    """
    return text.strip().replace('\n', '').replace('\r', '').replace('\t', '')


def format_price(price_str: str) -> float:
    """
    Converts a price string (e.g., "$1,200.00") to a float.
    Returns 0.0 if the value is invalid.
    """
    try:
        cleaned = price_str.replace('$', '').replace(',', '').strip()
        return float(cleaned)
    except (ValueError, AttributeError):
        return 0.0


def log(msg: str):
    """
    Prints a message with a timestamp.
    Useful for manual process monitoring.
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] {msg}")


def is_valid_field(field: str) -> bool:
    """
    Checks that a string field is not empty or just whitespace.
    """
    return bool(field and field.strip())


def is_valid_date(date_str: str, date_format: str = "%d/%m/%Y") -> bool:
    """
    Checks if a string date matches a given format.
    Example format: "%d/%m/%Y" for "31/12/2025"
    """
    try:
        datetime.datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False
