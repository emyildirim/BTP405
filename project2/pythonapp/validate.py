# This file contains the form validation functions
import re
from datetime import datetime, date, timedelta

def validate_date(date_text, date_format='%Y-%m-%d'):
    """
    Validates if the input date_text follows the specified date_format and
    checks if the date is today or in the future. Default format is YYYY-MM-DD.
    """
    try:
        input_date = datetime.strptime(date_text, date_format)
        current_date = datetime.now()
        
        # Compare the input date to the current date, ignoring the time component
        if input_date.date() >= current_date.date():
            return True
        else:
            return False
    except ValueError:
        return False

def validate_phone(phone):
    """
    Validates if the input phone number contains exactly 10 digits.
    The phone number can include optional country code prefix.
    """
    # This pattern matches an optional '+' followed by 10 digits
    pattern = re.compile(r"^\+?\d{10}$")
    return bool(pattern.match(phone))

def validate_email(email):
    """
    Validates if the input email is of a valid format.
    """
    pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    return bool(pattern.match(email))

def validate_time(time_text, time_format='%H:%M'):
    """
    Validates if the input time_text follows the specified time_format.
    Default format is HH:MM.
    """
    try:
        datetime.strptime(time_text, time_format)
        return True
    except ValueError:
        return False

def validate_number_of_guests(number):
    """
    Validates if the number of guests is within a reasonable range.
    """
    return 1 <= number <= 8

def format_timedelta_to_ampm(td):
    # Convert total seconds to hours, minutes, and seconds
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format into AM/PM
    period = 'AM'
    if hours >= 12:
        period = 'PM'
    if hours > 12:
        hours -= 12
    elif hours == 0:
        hours = 12

    # Return the formatted time string
    return f"{hours:02d}:{minutes:02d} {period}"

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, date):
        return obj.isoformat()
    elif isinstance(obj, timedelta):
        return str(format_timedelta_to_ampm(obj))
    raise TypeError("Type %s not serializable" % type(obj).__name__)

# if __name__ == "__main__":
#     print(validate_date("2023-01-01"))  # True
#     print(validate_phone("+1234567890"))  # True
#     print(validate_email("example@example.com"))  # True
#     print(validate_time("14:00:00"))  # True
#     print(validate_number_of_guests(5))  # True

