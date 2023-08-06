from datetime import datetime

from sqlalchemy import Column

from ms_utils import TimestampField


class BaseModal:
    created_at = Column(TimestampField, default=datetime.now())
    updated_at = Column(TimestampField, default=datetime.now())
