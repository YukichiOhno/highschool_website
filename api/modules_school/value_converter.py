from decimal import Decimal
import datetime

def convert_values(entity):
    # convert decimal fields to float
    for row in entity:
        for key, value in row.items():
            if isinstance(value, Decimal):
                row[key] = float(value)
            elif isinstance(value, datetime.date):
                row[key] = value.strftime('%Y-%m-%d')  # Convert datetime.date to string