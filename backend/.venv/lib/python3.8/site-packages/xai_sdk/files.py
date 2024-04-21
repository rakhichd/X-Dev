"""SDK for managing files hosted in the PromptIDE.

Users can host up to 50 MiB of files in the IDE with each file having a maximum size of 5 MiB. This
is useful for experimenting with small to medium-sized CSV files.
"""

from google.protobuf import empty_pb2

from .proto import files_pb2, files_pb2_grpc


class AsyncFiles:
    """Contains API for interacting with files."""

    def __init__(self, stub: files_pb2_grpc.FileStub) -> None:
        """Initializes a new instance of the `AsyncFiles` class.

        Args:
            stub: Stub used to communicate with the gRPC API.
        """
        self._stub = stub

    async def download(self, file_name: str) -> bytes:
        """Reads a file store in the IDE.

        Args:
            file_name: Name of the file. This is case-sensitive.

        Returns:
            The file contents in bytes.
        """
        response: files_pb2.FileObject = await self._stub.DownloadFile(
            files_pb2.DownloadFileRequest(file_name=file_name)
        )
        return response.content

    async def upload_file(self, local_file_name: str, remote_file_name: str) -> None:
        """Uploads a locally stored file to the IDE's storage.

        Args:
            local_file_name: Local filename.
            remote_file_name: Name of the file in the IDE.
        """
        # Read the file content.
        with open(local_file_name, "rb") as f:
            await self.upload(remote_file_name, f.read())

    async def upload(
        self, file_name: str, content: bytes, mime_type: str = "", overwrite: bool = True
    ) -> None:
        """Creates a new file in the IDE.

        Args:
            file_name: Name of the file in the IDE.
            content: File contents.
            mime_type: Mime type of the file.
            overwrite: True if the file shall be overwritten when it's re-uploaded.
        """
        await self._stub.UploadFile(
            files_pb2.UploadFileRequest(
                file_name=file_name, content=content, mime_type=mime_type, overwrite=overwrite
            )
        )

    async def list(self) -> list[files_pb2.FileMetadata]:
        """Returns the metadata of all files stored in the IDE.

        Returns:
            Metadata of all uploaded files.
        """
        response: files_pb2.ListFilesResponse = await self._stub.ListFiles(empty_pb2.Empty())
        return list(response.files)

    async def delete(self, file_name: str) -> None:
        """Deletes a file.

        Args:
            file_name: Name of the file to delete.
        """
        await self._stub.DeleteFile(files_pb2.DeleteFileRequest(file_name=file_name))
