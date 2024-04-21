from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from .google.api import annotations_pb2 as _annotations_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class StatelessConversation(_message.Message):
    __slots__ = [
        "stateless_conversation_id",
        "responses",
        "system_prompt_name",
        "name",
        "username",
        "expose_username_to_grok",
    ]
    STATELESS_CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_PROMPT_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    EXPOSE_USERNAME_TO_GROK_FIELD_NUMBER: _ClassVar[int]
    stateless_conversation_id: str
    responses: _containers.RepeatedCompositeFieldContainer[StatelessResponse]
    system_prompt_name: str
    name: str
    username: str
    expose_username_to_grok: bool
    def __init__(
        self,
        stateless_conversation_id: _Optional[str] = ...,
        responses: _Optional[_Iterable[_Union[StatelessResponse, _Mapping]]] = ...,
        system_prompt_name: _Optional[str] = ...,
        name: _Optional[str] = ...,
        username: _Optional[str] = ...,
        expose_username_to_grok: bool = ...,
    ) -> None: ...

class StatelessResponse(_message.Message):
    __slots__ = ["sender", "message", "query"]

    class Sender(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        UNKNOWN: _ClassVar[StatelessResponse.Sender]
        HUMAN: _ClassVar[StatelessResponse.Sender]
        ASSISTANT: _ClassVar[StatelessResponse.Sender]
    UNKNOWN: StatelessResponse.Sender
    HUMAN: StatelessResponse.Sender
    ASSISTANT: StatelessResponse.Sender
    SENDER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    sender: StatelessResponse.Sender
    message: str
    query: str
    def __init__(
        self,
        sender: _Optional[_Union[StatelessResponse.Sender, str]] = ...,
        message: _Optional[str] = ...,
        query: _Optional[str] = ...,
    ) -> None: ...

class DeleteLoggedConversationsRequest(_message.Message):
    __slots__ = ["accounting_key"]
    ACCOUNTING_KEY_FIELD_NUMBER: _ClassVar[int]
    accounting_key: str
    def __init__(self, accounting_key: _Optional[str] = ...) -> None: ...
