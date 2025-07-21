from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MediaKind(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    TEXT: _ClassVar[MediaKind]
    PHOTO: _ClassVar[MediaKind]
    VOICE: _ClassVar[MediaKind]
TEXT: MediaKind
PHOTO: MediaKind
VOICE: MediaKind

class FilePointer(_message.Message):
    __slots__ = ("storage", "bucket", "key", "mime", "size")
    STORAGE_FIELD_NUMBER: _ClassVar[int]
    BUCKET_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    MIME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    storage: str
    bucket: str
    key: str
    mime: str
    size: int
    def __init__(self, storage: _Optional[str] = ..., bucket: _Optional[str] = ..., key: _Optional[str] = ..., mime: _Optional[str] = ..., size: _Optional[int] = ...) -> None: ...

class TelegramMessageV1(_message.Message):
    __slots__ = ("event_id", "ts", "chat_id", "user_id", "kind", "text", "file")
    EVENT_ID_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    event_id: str
    ts: _timestamp_pb2.Timestamp
    chat_id: int
    user_id: int
    kind: MediaKind
    text: str
    file: FilePointer
    def __init__(self, event_id: _Optional[str] = ..., ts: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ..., chat_id: _Optional[int] = ..., user_id: _Optional[int] = ..., kind: _Optional[_Union[MediaKind, str]] = ..., text: _Optional[str] = ..., file: _Optional[_Union[FilePointer, _Mapping]] = ...) -> None: ...
