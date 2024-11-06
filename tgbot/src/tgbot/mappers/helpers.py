from datetime import datetime
from typing import Any

from serpyco_rs import CustomType


class _DateTimeType(CustomType[datetime, datetime]):
    def serialize(self, value: datetime) -> datetime:
        return value

    def deserialize(self, value: datetime) -> datetime:
        return value

    def get_json_schema(self) -> dict[str, Any]:
        return {}


_datetime_mapper= _DateTimeType()


def datetime_resolver(t: type) -> CustomType | None:
    if t is datetime:
        return _datetime_mapper
    return None
