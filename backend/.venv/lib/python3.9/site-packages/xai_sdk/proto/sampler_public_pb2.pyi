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
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper

from .google.api import annotations_pb2 as _annotations_pb2

DESCRIPTOR: _descriptor.FileDescriptor

class SampleTokensRequest(_message.Message):
    __slots__ = ["prompt", "settings", "return_attention", "model_name"]
    PROMPT_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    RETURN_ATTENTION_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    prompt: _containers.RepeatedScalarFieldContainer[int]
    settings: SampleSettings
    return_attention: bool
    model_name: str
    def __init__(
        self,
        prompt: _Optional[_Iterable[int]] = ...,
        settings: _Optional[_Union[SampleSettings, _Mapping]] = ...,
        return_attention: bool = ...,
        model_name: _Optional[str] = ...,
    ) -> None: ...

class SampleTokensResponse(_message.Message):
    __slots__ = ["token", "budget"]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    BUDGET_FIELD_NUMBER: _ClassVar[int]
    token: Token
    budget: TokenBudget
    def __init__(
        self,
        token: _Optional[_Union[Token, _Mapping]] = ...,
        budget: _Optional[_Union[TokenBudget, _Mapping]] = ...,
    ) -> None: ...

class SampleSettings(_message.Message):
    __slots__ = [
        "max_len",
        "temperature",
        "nucleus_p",
        "stop_tokens",
        "stop_strings",
        "rng_seed",
        "allowed_tokens",
        "disallowed_tokens",
    ]
    MAX_LEN_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    NUCLEUS_P_FIELD_NUMBER: _ClassVar[int]
    STOP_TOKENS_FIELD_NUMBER: _ClassVar[int]
    STOP_STRINGS_FIELD_NUMBER: _ClassVar[int]
    RNG_SEED_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_TOKENS_FIELD_NUMBER: _ClassVar[int]
    DISALLOWED_TOKENS_FIELD_NUMBER: _ClassVar[int]
    max_len: int
    temperature: float
    nucleus_p: float
    stop_tokens: _containers.RepeatedScalarFieldContainer[str]
    stop_strings: _containers.RepeatedScalarFieldContainer[str]
    rng_seed: int
    allowed_tokens: _containers.RepeatedCompositeFieldContainer[InputToken]
    disallowed_tokens: _containers.RepeatedCompositeFieldContainer[InputToken]
    def __init__(
        self,
        max_len: _Optional[int] = ...,
        temperature: _Optional[float] = ...,
        nucleus_p: _Optional[float] = ...,
        stop_tokens: _Optional[_Iterable[str]] = ...,
        stop_strings: _Optional[_Iterable[str]] = ...,
        rng_seed: _Optional[int] = ...,
        allowed_tokens: _Optional[_Iterable[_Union[InputToken, _Mapping]]] = ...,
        disallowed_tokens: _Optional[_Iterable[_Union[InputToken, _Mapping]]] = ...,
    ) -> None: ...

class InputToken(_message.Message):
    __slots__ = ["string_token", "token_id"]
    STRING_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    string_token: str
    token_id: int
    def __init__(
        self, string_token: _Optional[str] = ..., token_id: _Optional[int] = ...
    ) -> None: ...

class Token(_message.Message):
    __slots__ = ["final_logit", "top_k", "attention", "token_type"]

    class TokenType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        UNKNOWN: _ClassVar[Token.TokenType]
        USER: _ClassVar[Token.TokenType]
        MODEL: _ClassVar[Token.TokenType]
    UNKNOWN: Token.TokenType
    USER: Token.TokenType
    MODEL: Token.TokenType
    FINAL_LOGIT_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    ATTENTION_FIELD_NUMBER: _ClassVar[int]
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    final_logit: Logit
    top_k: _containers.RepeatedCompositeFieldContainer[Logit]
    attention: _containers.RepeatedScalarFieldContainer[float]
    token_type: Token.TokenType
    def __init__(
        self,
        final_logit: _Optional[_Union[Logit, _Mapping]] = ...,
        top_k: _Optional[_Iterable[_Union[Logit, _Mapping]]] = ...,
        attention: _Optional[_Iterable[float]] = ...,
        token_type: _Optional[_Union[Token.TokenType, str]] = ...,
    ) -> None: ...

class Logit(_message.Message):
    __slots__ = ["token_id", "string_token", "prob"]
    TOKEN_ID_FIELD_NUMBER: _ClassVar[int]
    STRING_TOKEN_FIELD_NUMBER: _ClassVar[int]
    PROB_FIELD_NUMBER: _ClassVar[int]
    token_id: int
    string_token: str
    prob: float
    def __init__(
        self,
        token_id: _Optional[int] = ...,
        string_token: _Optional[str] = ...,
        prob: _Optional[float] = ...,
    ) -> None: ...

class TokenizeRequest(_message.Message):
    __slots__ = ["text", "model_name"]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    text: str
    model_name: str
    def __init__(self, text: _Optional[str] = ..., model_name: _Optional[str] = ...) -> None: ...

class TokenizeResponse(_message.Message):
    __slots__ = ["tokens"]
    TOKENS_FIELD_NUMBER: _ClassVar[int]
    tokens: _containers.RepeatedCompositeFieldContainer[Token]
    def __init__(self, tokens: _Optional[_Iterable[_Union[Token, _Mapping]]] = ...) -> None: ...

class ListTransactionsResponse(_message.Message):
    __slots__ = ["transactions"]
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[TokenTransaction]
    def __init__(
        self, transactions: _Optional[_Iterable[_Union[TokenTransaction, _Mapping]]] = ...
    ) -> None: ...

class TokenTransaction(_message.Message):
    __slots__ = ["num_prompt_tokens", "num_generated_tokens", "cost_multiplier", "create_time"]
    NUM_PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    NUM_GENERATED_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COST_MULTIPLIER_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    num_prompt_tokens: int
    num_generated_tokens: int
    cost_multiplier: int
    create_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        num_prompt_tokens: _Optional[int] = ...,
        num_generated_tokens: _Optional[int] = ...,
        cost_multiplier: _Optional[int] = ...,
        create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class TokenBudget(_message.Message):
    __slots__ = ["token_limit", "tokens_spent"]
    TOKEN_LIMIT_FIELD_NUMBER: _ClassVar[int]
    TOKENS_SPENT_FIELD_NUMBER: _ClassVar[int]
    token_limit: int
    tokens_spent: int
    def __init__(
        self, token_limit: _Optional[int] = ..., tokens_spent: _Optional[int] = ...
    ) -> None: ...
