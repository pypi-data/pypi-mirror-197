import io
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from functools import partial
from typing import Any, AsyncIterator, Callable, Dict, Tuple, TypeVar

from sqlalchemy import ARRAY, JSON, TIMESTAMP, BigInteger, Boolean, Column, Double
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, Integer, SmallInteger, String, Table
from strong_typing.core import JsonType

from ..async_helpers import GzipStreamReader

T = TypeVar("T")

# Simply Dict[str, JsonType] would be enough here, we just want to capture the presence of mandatory
# sub-structures 'key' and 'value'.
JsonRecordType = Dict[str, Dict[str, JsonType]]


class Converter:
    _col_name: str
    _converter: Callable[[JsonRecordType], Any]

    def __init__(self, col_name: str, converter: Callable[[JsonRecordType], Any]):
        self._col_name = col_name
        self._converter = converter

    def __call__(self, record: JsonRecordType) -> Any:
        return self._converter(record)

    @property
    def col_name(self):
        return self._col_name


class ConversionError(Exception):
    def __init_(self, message: str):
        super().__init__(message)


def _identity(obj: T) -> T:
    return obj


def _valid_list(obj: Any) -> list:
    if type(obj) is list:
        return obj
    else:
        raise TypeError(f"object is not a list: {obj}")


def valid_utc_datetime(s: str) -> datetime:
    """Converts a string into a UTC datetime instance."""

    if s.endswith("Z"):
        s = f"{s[:-1]}+00:00"  # Python's isoformat() does not support military time zones like "Zulu" for UTC
    try:
        return datetime.fromisoformat(s).astimezone(timezone.utc)
    except ValueError:
        raise ConversionError(f"not a valid ISO 8601 timestamp: {s}")


def valid_naive_datetime(s: str) -> datetime:
    """Converts a string into a naive datetime instance."""

    if s.endswith("Z"):
        s = f"{s[:-1]}+00:00"  # Python's isoformat() does not support military time zones like "Zulu" for UTC
    try:
        return datetime.fromisoformat(s).replace(tzinfo=None)
    except ValueError:
        raise ConversionError(f"not a valid ISO 8601 timestamp: {s}")


_converters = {
    BigInteger: int,
    Integer: int,
    SmallInteger: int,
    Float: float,
    Double: float,
    SqlEnum: _identity,
    TIMESTAMP: valid_naive_datetime,
    String: str,
    JSON: _identity,
    Boolean: bool,
    ARRAY: _valid_list,
}


def _get_column_value(
    record_json: JsonRecordType,
    col_name: str,
    col_converter: Callable[[JsonType], Any],
) -> Any:
    val = record_json["key"].get(col_name)
    if val is not None:
        return col_converter(val)

    record_values = record_json.get("value")
    if record_values is not None:
        val = record_values.get(col_name)

    return col_converter(val) if val is not None else None


def _create_column_converter(
    col: Column,
) -> Callable[[JsonRecordType], Any]:
    converter: Callable[[JsonType], Any] = _converters.get(type(col.type))  # type: ignore
    if converter is None:
        raise TypeError(f"cannot convert to {type(col.type)}")
    return partial(_get_column_value, col_name=col.name, col_converter=converter)


class Operation(Enum):
    Upsert = 0
    Delete = 1


@dataclass
class Record:
    operation: Operation
    content: Dict[str, Any]


async def process_resource_for_copy(
    stream: io.BufferedIOBase, table_def: Table
) -> AsyncIterator[Tuple]:
    # Create a tuple of converter objects for each column
    converters: Tuple = tuple(
        [
            Converter(col_name=col.name, converter=_create_column_converter(col))
            for col in table_def.columns
        ]
    )

    with GzipStreamReader(stream) as gzip_reader:
        async for line in gzip_reader:
            record_json: JsonRecordType = json.loads(line)
            yield tuple([converter(record_json) for converter in converters])


async def process_resource(
    stream: io.BufferedIOBase, table_def: Table
) -> AsyncIterator[Record]:
    # Create a tuple of converter objects for each column for UPSERT records
    upsert_converters: Tuple = tuple(
        [
            Converter(col_name=col.name, converter=_create_column_converter(col))
            for col in table_def.columns
        ]
    )

    # Create a tuple of converter objects for each column for DELETE records
    delete_converters: Tuple = tuple(
        [
            Converter(col_name=col.name, converter=_create_column_converter(col))
            for col in table_def.primary_key
        ]
    )

    with GzipStreamReader(stream) as gzip_reader:
        async for line in gzip_reader:
            record_json: JsonRecordType = json.loads(line)
            operation = _operation(record_json)
            converters = (
                upsert_converters
                if operation == Operation.Upsert
                else delete_converters
            )
            yield Record(
                operation=operation,
                content={
                    converter.col_name: converter(record_json)
                    for converter in converters
                },
            )


def _operation(record_json: JsonType) -> Operation:
    if "value" not in record_json:
        return Operation.Delete
    else:
        return Operation.Upsert
