from sqlalchemy import Column

from .model_utils import TimestampField


class BaseModal:
    created_at = Column(TimestampField)
    updated_at = Column(TimestampField)
