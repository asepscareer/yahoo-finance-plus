import re
from datetime import date
import ssl
from dateutil import parser

if hasattr(ssl, "_create_unverified_context"):
    ssl._create_default_https_context = ssl._create_unverified_context

def get_paginated_list(results, url, page=1, limit=10):
    page = int(page)
    limit = int(limit)
    count = len(results)
    if page < 1 or limit <= 0:
        raise ValueError('Invalid pagination parameters')

    start = (page - 1) * limit
    end = start + limit
    if start >= count:
        return None

    response = {
        'page': page,
        'limit': limit,
        'count': count,
        'previous': f"{url}?page={page-1}&limit={limit}" if page > 1 else '',
        'next': f"{url}?page={page+1}&limit={limit}" if end < count else '',
        'results': results[start:end]
    }
    return response

def default_converter(o):
    if isinstance(o, date):
        return o.isoformat()

def to_timestamp(date_str):
    obj_datetime = parser.parse(date_str)
    timestamp = int(obj_datetime.timestamp())
    return timestamp

def to_epoch(date_str):
    date_obj = parser.parse(date_str, dayfirst=False)
    formatted_date = date_obj.strftime("%Y-%m-%d")
    epoch_time = int(parser.parse(formatted_date).timestamp() * 1000)
    return epoch_time

def _to_camel_case(snake_str):
    # Remove special characters and handle various delimiters
    snake_str = re.sub(r'[^a-zA-Z0-9]+', ' ', snake_str)
    # Split and filter out empty strings
    components = [c for c in snake_str.split(' ') if c]

    if not components:
        return ""

    # If there's only one component, it has no delimiters.
    # It could be camelCase, PascalCase, lowercase, or UPPERCASE.
    if len(components) == 1:
        s = components[0]
        # If it's not all uppercase, it might be camelCase or PascalCase.
        if not s.isupper():
            # If it starts with an uppercase letter (PascalCase), convert the first letter to lower.
            # Otherwise (camelCase or lowercase), return as is.
            return s[0].lower() + s[1:] if s[0].isupper() else s
    
    # For multiple components (from snake_case, etc.) or all-caps single words,
    # apply the conversion logic.
    return ''.join(x.lower() if i == 0 else x.capitalize() for i, x in enumerate(components))

def convert_keys_to_camel_case(data):
    if isinstance(data, dict):
        return {
            _to_camel_case(key): convert_keys_to_camel_case(value)
            for key, value in data.items()
        }
    if isinstance(data, list):
        return [convert_keys_to_camel_case(item) for item in data]
    return data