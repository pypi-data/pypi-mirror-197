from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetNotificationInfoRequest(_message.Message):
    __slots__ = ["service_token"]
    SERVICE_TOKEN_FIELD_NUMBER: _ClassVar[int]
    service_token: str
    def __init__(self, service_token: _Optional[str] = ...) -> None: ...

class GetNotificationInfoResponse(_message.Message):
    __slots__ = ["email", "id", "is_active", "is_superuser"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    IS_SUPERUSER_FIELD_NUMBER: _ClassVar[int]
    email: str
    id: str
    is_active: bool
    is_superuser: bool
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., is_active: bool = ..., is_superuser: bool = ...) -> None: ...
