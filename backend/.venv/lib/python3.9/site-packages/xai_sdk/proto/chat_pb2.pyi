from typing import ClassVar as _ClassVar
from typing import Iterable as _Iterable
from typing import Mapping as _Mapping
from typing import Optional as _Optional
from typing import Union as _Union

from google.protobuf import descriptor as _descriptor
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import message as _message
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers

from . import sampler_public_pb2 as _sampler_public_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class RegenerateResponseRequest(_message.Message):
    __slots__ = ["conversation_id", "response_id"]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    response_id: str
    def __init__(
        self, conversation_id: _Optional[str] = ..., response_id: _Optional[str] = ...
    ) -> None: ...

class CreateConversationRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetConversationRequest(_message.Message):
    __slots__ = ["conversation_id"]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    def __init__(self, conversation_id: _Optional[str] = ...) -> None: ...

class DeleteConversationRequest(_message.Message):
    __slots__ = ["conversation_id"]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    def __init__(self, conversation_id: _Optional[str] = ...) -> None: ...

class ListConversationsResponse(_message.Message):
    __slots__ = ["conversations"]
    CONVERSATIONS_FIELD_NUMBER: _ClassVar[int]
    conversations: _containers.RepeatedCompositeFieldContainer[Conversation]
    def __init__(
        self, conversations: _Optional[_Iterable[_Union[Conversation, _Mapping]]] = ...
    ) -> None: ...

class GenerateTitleRequest(_message.Message):
    __slots__ = ["conversation_id", "leaf_response_id"]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    LEAF_RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    leaf_response_id: str
    def __init__(
        self, conversation_id: _Optional[str] = ..., leaf_response_id: _Optional[str] = ...
    ) -> None: ...

class GenerateTitleResponse(_message.Message):
    __slots__ = ["new_title"]
    NEW_TITLE_FIELD_NUMBER: _ClassVar[int]
    new_title: str
    def __init__(self, new_title: _Optional[str] = ...) -> None: ...

class AddModelResponseRequest(_message.Message):
    __slots__ = ["conversation_id", "message", "partial", "parent_response_id"]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_FIELD_NUMBER: _ClassVar[int]
    PARENT_RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    message: str
    partial: bool
    parent_response_id: str
    def __init__(
        self,
        conversation_id: _Optional[str] = ...,
        message: _Optional[str] = ...,
        partial: bool = ...,
        parent_response_id: _Optional[str] = ...,
    ) -> None: ...

class UpdateConversationRequest(_message.Message):
    __slots__ = ["conversation_id", "title", "starred"]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    STARRED_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    title: str
    starred: bool
    def __init__(
        self,
        conversation_id: _Optional[str] = ...,
        title: _Optional[str] = ...,
        starred: bool = ...,
    ) -> None: ...

class AddResponseRequest(_message.Message):
    __slots__ = [
        "conversation_id",
        "message",
        "model_name",
        "parent_response_id",
        "use_grok",
        "system_prompt_name",
    ]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    PARENT_RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    USE_GROK_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_PROMPT_NAME_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    message: str
    model_name: str
    parent_response_id: str
    use_grok: bool
    system_prompt_name: str
    def __init__(
        self,
        conversation_id: _Optional[str] = ...,
        message: _Optional[str] = ...,
        model_name: _Optional[str] = ...,
        parent_response_id: _Optional[str] = ...,
        use_grok: bool = ...,
        system_prompt_name: _Optional[str] = ...,
    ) -> None: ...

class AddResponseResponse(_message.Message):
    __slots__ = ["user_response", "token", "model_response", "query_action"]
    USER_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    MODEL_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    QUERY_ACTION_FIELD_NUMBER: _ClassVar[int]
    user_response: Response
    token: _sampler_public_pb2.SampleTokensResponse
    model_response: Response
    query_action: QueryAction
    def __init__(
        self,
        user_response: _Optional[_Union[Response, _Mapping]] = ...,
        token: _Optional[_Union[_sampler_public_pb2.SampleTokensResponse, _Mapping]] = ...,
        model_response: _Optional[_Union[Response, _Mapping]] = ...,
        query_action: _Optional[_Union[QueryAction, _Mapping]] = ...,
    ) -> None: ...

class QueryAction(_message.Message):
    __slots__ = ["query", "type"]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    query: str
    type: str
    def __init__(self, query: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class Conversation(_message.Message):
    __slots__ = ["conversation_id", "title", "starred", "create_time", "modify_time", "responses"]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    STARRED_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    MODIFY_TIME_FIELD_NUMBER: _ClassVar[int]
    RESPONSES_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    title: str
    starred: bool
    create_time: _timestamp_pb2.Timestamp
    modify_time: _timestamp_pb2.Timestamp
    responses: _containers.RepeatedCompositeFieldContainer[Response]
    def __init__(
        self,
        conversation_id: _Optional[str] = ...,
        title: _Optional[str] = ...,
        starred: bool = ...,
        create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        modify_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        responses: _Optional[_Iterable[_Union[Response, _Mapping]]] = ...,
    ) -> None: ...

class Response(_message.Message):
    __slots__ = [
        "response_id",
        "message",
        "sender",
        "create_time",
        "parent_response_id",
        "manual",
        "partial",
        "shared",
        "query",
        "query_type",
    ]
    RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    PARENT_RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    MANUAL_FIELD_NUMBER: _ClassVar[int]
    PARTIAL_FIELD_NUMBER: _ClassVar[int]
    SHARED_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    QUERY_TYPE_FIELD_NUMBER: _ClassVar[int]
    response_id: str
    message: str
    sender: str
    create_time: _timestamp_pb2.Timestamp
    parent_response_id: str
    manual: bool
    partial: bool
    shared: bool
    query: str
    query_type: str
    def __init__(
        self,
        response_id: _Optional[str] = ...,
        message: _Optional[str] = ...,
        sender: _Optional[str] = ...,
        create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
        parent_response_id: _Optional[str] = ...,
        manual: bool = ...,
        partial: bool = ...,
        shared: bool = ...,
        query: _Optional[str] = ...,
        query_type: _Optional[str] = ...,
    ) -> None: ...

class ShareConversationRequest(_message.Message):
    __slots__ = ["conversation_id", "response_id"]
    CONVERSATION_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    conversation_id: str
    response_id: str
    def __init__(
        self, conversation_id: _Optional[str] = ..., response_id: _Optional[str] = ...
    ) -> None: ...

class ShareConversationResponse(_message.Message):
    __slots__ = ["shared_id"]
    SHARED_ID_FIELD_NUMBER: _ClassVar[int]
    shared_id: str
    def __init__(self, shared_id: _Optional[str] = ...) -> None: ...
