from sqlalchemy import Column, Integer

from .func_date import get_timestamp_now, convert_timestamp_to_date
from .model_utils import TimestampField


class BaseModal:
    created_at = Column(TimestampField, default=str(get_timestamp_now()))
    updated_at = Column(TimestampField, default=str(get_timestamp_now()))
