import replyMessage_pb2 as _replyMessage_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Dispenser(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    DISPENSER_NOT_IN_USE: _ClassVar[Dispenser]
    DISPENSER_OPTIMAL: _ClassVar[Dispenser]
    DISPENSER_PARTIAL: _ClassVar[Dispenser]
    DISPENSER_BLOCKAGE: _ClassVar[Dispenser]

class Lightbulb(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    LIGHTBULB_NOT_IN_USE: _ClassVar[Lightbulb]
    LIGHTBULB_GOOD: _ClassVar[Lightbulb]
    LIGHTBULB_BAD: _ClassVar[Lightbulb]

class Sensor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    SENSOR_NOT_IN_USE: _ClassVar[Sensor]
    SENSOR_GOOD: _ClassVar[Sensor]
    SENSOR_BAD: _ClassVar[Sensor]
DISPENSER_NOT_IN_USE: Dispenser
DISPENSER_OPTIMAL: Dispenser
DISPENSER_PARTIAL: Dispenser
DISPENSER_BLOCKAGE: Dispenser
LIGHTBULB_NOT_IN_USE: Lightbulb
LIGHTBULB_GOOD: Lightbulb
LIGHTBULB_BAD: Lightbulb
SENSOR_NOT_IN_USE: Sensor
SENSOR_GOOD: Sensor
SENSOR_BAD: Sensor

class HealthMessage(_message.Message):
    __slots__ = ["seq_no", "ts", "name", "dispenser", "icemaker", "lightbulb", "fridge_temp", "freezer_temp", "sensor_status"]
    SEQ_NO_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DISPENSER_FIELD_NUMBER: _ClassVar[int]
    ICEMAKER_FIELD_NUMBER: _ClassVar[int]
    LIGHTBULB_FIELD_NUMBER: _ClassVar[int]
    FRIDGE_TEMP_FIELD_NUMBER: _ClassVar[int]
    FREEZER_TEMP_FIELD_NUMBER: _ClassVar[int]
    SENSOR_STATUS_FIELD_NUMBER: _ClassVar[int]
    seq_no: int
    ts: float
    name: str
    dispenser: Dispenser
    icemaker: int
    lightbulb: Lightbulb
    fridge_temp: int
    freezer_temp: int
    sensor_status: Sensor
    def __init__(self, seq_no: _Optional[int] = ..., ts: _Optional[float] = ..., name: _Optional[str] = ..., dispenser: _Optional[_Union[Dispenser, str]] = ..., icemaker: _Optional[int] = ..., lightbulb: _Optional[_Union[Lightbulb, str]] = ..., fridge_temp: _Optional[int] = ..., freezer_temp: _Optional[int] = ..., sensor_status: _Optional[_Union[Sensor, str]] = ...) -> None: ...
