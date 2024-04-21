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

DESCRIPTOR: _descriptor.FileDescriptor

class UploadFileRequest(_message.Message):
    __slots__ = ["file_name", "content", "mime_type", "overwrite"]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    content: bytes
    mime_type: str
    overwrite: bool
    def __init__(
        self,
        file_name: _Optional[str] = ...,
        content: _Optional[bytes] = ...,
        mime_type: _Optional[str] = ...,
        overwrite: bool = ...,
    ) -> None: ...

class FileMetadata(_message.Message):
    __slots__ = ["file_name", "size_bytes", "mime_type", "create_time"]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    MIME_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    size_bytes: int
    mime_type: str
    create_time: _timestamp_pb2.Timestamp
    def __init__(
        self,
        file_name: _Optional[str] = ...,
        size_bytes: _Optional[int] = ...,
        mime_type: _Optional[str] = ...,
        create_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...,
    ) -> None: ...

class RenameFileRequest(_message.Message):
    __slots__ = ["file_name", "new_file_name"]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    NEW_FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    new_file_name: str
    def __init__(
        self, file_name: _Optional[str] = ..., new_file_name: _Optional[str] = ...
    ) -> None: ...

class DownloadFileRequest(_message.Message):
    __slots__ = ["file_name"]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    def __init__(self, file_name: _Optional[str] = ...) -> None: ...

class FileObject(_message.Message):
    __slots__ = ["metadata", "content"]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    metadata: FileMetadata
    content: bytes
    def __init__(
        self,
        metadata: _Optional[_Union[FileMetadata, _Mapping]] = ...,
        content: _Optional[bytes] = ...,
    ) -> None: ...

class ListFilesResponse(_message.Message):
    __slots__ = ["storage_used", "storage_available_total", "files"]
    STORAGE_USED_FIELD_NUMBER: _ClassVar[int]
    STORAGE_AVAILABLE_TOTAL_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    storage_used: int
    storage_available_total: int
    files: _containers.RepeatedCompositeFieldContainer[FileMetadata]
    def __init__(
        self,
        storage_used: _Optional[int] = ...,
        storage_available_total: _Optional[int] = ...,
        files: _Optional[_Iterable[_Union[FileMetadata, _Mapping]]] = ...,
    ) -> None: ...

class DeleteFileRequest(_message.Message):
    __slots__ = ["file_name"]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    def __init__(self, file_name: _Optional[str] = ...) -> None: ...
