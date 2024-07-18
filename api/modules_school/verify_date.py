import re

# Define the regular expression pattern for yyyy-mm-dd
date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

# Function to test if a string matches the date pattern
def is_valid_date(date_string):
    return bool(date_pattern.match(date_string))

if __name__ == "__main__":
    # Test cases
    test_dates = [
        "2024-06-11",
        "1999-12-31",
        "2020-02-30",  # Invalid date but matches format
        "2024-6-11",
        "24-06-11",
        "2024/06/11",
        "11-06-2024"
    ]

    for date in test_dates:
        print(f"{date}: {is_valid_date(date)}")