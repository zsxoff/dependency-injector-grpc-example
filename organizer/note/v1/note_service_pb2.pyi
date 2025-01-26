from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateNoteRequest(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...

class CreateNoteResponse(_message.Message):
    __slots__ = ("note_id",)
    NOTE_ID_FIELD_NUMBER: _ClassVar[int]
    note_id: str
    def __init__(self, note_id: _Optional[str] = ...) -> None: ...

class GetNoteRequest(_message.Message):
    __slots__ = ("note_id",)
    NOTE_ID_FIELD_NUMBER: _ClassVar[int]
    note_id: str
    def __init__(self, note_id: _Optional[str] = ...) -> None: ...

class GetNoteResponse(_message.Message):
    __slots__ = ("content",)
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...
