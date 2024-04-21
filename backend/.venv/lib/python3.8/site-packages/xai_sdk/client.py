"""Wrappers around the bare gRPC bindings."""

import os
from typing import Optional

import grpc

from . import chat, files, grok, sampler
from .proto import chat_pb2_grpc, files_pb2_grpc, sampler_public_pb2_grpc, stateless_chat_pb2_grpc


class Client:
    """Client for connecting to the xAI API.

    The client uses an API key, which is either read from the environment variable `XAI_API_KEY` or
    provided by the `api_key` constructor argument. API keys can be created and managed in our IDE,
    which is available under ide.x.ai (click on your username in the top right hand corner).

    The API is hosted on api.x.ai, and we connect via port 443.
    """

    chat: chat.AsyncChat
    files: files.AsyncFiles
    grok: grok.AsyncGrok
    sampler: sampler.AsyncSampler

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        initial_rng_seed: Optional[int] = None,
        api_host: str = "api.x.ai",
    ) -> None:
        """Initializes a new instance of the `Client` class.

        Args:
            api_key: API key to use. If unspecified, the API key is read from the `XAI_API_KEY`
                environment variable.
            initial_rng_seed: Used to make calls to the API deterministic given the initial seed and
                the order of API calls. If unspecified, a random seed will be sampled for every new
                instance of the `Client` class.
            api_host: Hostname of the API server.

        Raises:
            ValueError: If the `XAI_API_KEY` environment variable is not set.
            ValueError: If the API key is empty.
        """
        if api_key is None:
            api_key = _get_api_from_env()

        if not api_key:
            raise ValueError("Empty xAI API key provided.")

        # Create a channel to connect to the API host. Use the API key for authentication.
        call_credentials = grpc.metadata_call_credentials(_APIAuthPlugin(api_key))
        channel_credentials = grpc.ssl_channel_credentials()
        credentials = grpc.composite_channel_credentials(channel_credentials, call_credentials)
        async_channel = grpc.aio.secure_channel(api_host, credentials)

        # Create the stubs used by the SDK. Note that they don't create any connections until being
        # used.
        self.sampler = sampler.AsyncSampler(
            sampler_public_pb2_grpc.SamplerStub(channel=async_channel), initial_rng_seed
        )
        self.chat = chat.AsyncChat(stateless_chat_pb2_grpc.StatelessChatStub(channel=async_channel))
        self.grok = grok.AsyncGrok(chat_pb2_grpc.ChatStub(channel=async_channel))
        self.files = files.AsyncFiles(files_pb2_grpc.FileStub(channel=async_channel))


def _get_api_from_env() -> str:
    """Reads the API key from the `XAI_API_KEY` environment variable.

    Returns:
        The API key.

    Raises:
        ValueError: If the `XAI_API_KEY` environment variable is not set.
    """
    api_key = os.environ.get("XAI_API_KEY")
    if api_key is None:
        raise ValueError(
            "Trying to read the xAI API key from the XAI_API_KEY environment variable "
            "but it doesn't exist."
        )
    else:
        return api_key


class _APIAuthPlugin(grpc.AuthMetadataPlugin):
    """A specification for API-key based authentication."""

    def __init__(self, api_key: str) -> None:
        """Initializes a new instance of the `_APIAuthPlugin` class.

        Args:
            api_key: A valid xAI API key.
        """
        self._api_key = api_key

    def __call__(
        self, context: grpc.AuthMetadataPluginCallback, callback: grpc.AuthMetadataPluginCallback
    ):
        """See `grpc.AuthMetadataPlugin.__call__`."""
        del context  # Unused.
        callback((("apikey", self._api_key),), None)
