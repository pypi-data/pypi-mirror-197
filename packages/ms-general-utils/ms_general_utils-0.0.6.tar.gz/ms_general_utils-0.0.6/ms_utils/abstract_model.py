from sqlalchemy import Column, Integer

from .func_date import get_timestamp_now, convert_timestamp_to_date
from .model_utils import TimestampField


class BaseModal:
    created_at = Column(TimestampField, server_default=str(get_timestamp_now()))
    updated_at = Column(TimestampField, server_default=str(get_timestamp_now()))

    def __repr__(self):
        self.created_at = convert_timestamp_to_date(self.created_at)
        self.updated_at = convert_timestamp_to_date(self.updated_at)
        return self
