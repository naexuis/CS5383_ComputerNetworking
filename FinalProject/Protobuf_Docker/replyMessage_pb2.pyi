from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReplyRequest(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    REPLY_REQUEST_NOT_SET: _ClassVar[ReplyRequest]
    GOOD: _ClassVar[ReplyRequest]
    BAD: _ClassVar[ReplyRequest]

class ReplyStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    REPLY_STATUS_NOT_SET: _ClassVar[ReplyStatus]
    SUCCESSFUL: _ClassVar[ReplyStatus]
    UNSUCCESSFUL: _ClassVar[ReplyStatus]
REPLY_REQUEST_NOT_SET: ReplyRequest
GOOD: ReplyRequest
BAD: ReplyRequest
REPLY_STATUS_NOT_SET: ReplyStatus
SUCCESSFUL: ReplyStatus
UNSUCCESSFUL: ReplyStatus

class ReplyMessage(_message.Message):
    __slots__ = ["seq_no", "ts", "reply_request", "reply_status"]
    SEQ_NO_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    REPLY_REQUEST_FIELD_NUMBER: _ClassVar[int]
    REPLY_STATUS_FIELD_NUMBER: _ClassVar[int]
    seq_no: int
    ts: float
    reply_request: ReplyRequest
    reply_status: ReplyStatus
    def __init__(self, seq_no: _Optional[int] = ..., ts: _Optional[float] = ..., reply_request: _Optional[_Union[ReplyRequest, str]] = ..., reply_status: _Optional[_Union[ReplyStatus, str]] = ...) -> None: ...
