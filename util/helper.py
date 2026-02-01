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
