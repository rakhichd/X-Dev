"""This module exposes a simple chat API.

The API in this module differs from the one in the `grok` module in that it's stateless.
Conversations cannot be accessed from the grok.x.ai UI and every backend request contains the entire
conversation history.
"""

import asyncio
import uuid
from typing import AsyncGenerator, Sequence

from .proto import stateless_chat_pb2, stateless_chat_pb2_grpc


class AsyncChat:
    """Provides a simple chat API that can be used for products."""

    def __init__(self, stub: stateless_chat_pb2_grpc.StatelessChatStub) -> None:
        """Initializes a new instance of the `AsyncChat` class.

        Args:
            stub: Stub used to communicate with the gRPC API.
        """
        self._stub = stub

    def create_conversation(self, fun_mode: bool = False) -> "Conversation":
        """Creates a new empty conversation.

        Args:
            fun_mode: Whether fun mode shall be enabled for this conversation.

        Returns:
            Newly created conversation.
        """
        return Conversation(self._stub, fun_mode)


class Conversation:
    """A conversation held via the stateless Chat API."""

    def __init__(self, stub: stateless_chat_pb2_grpc.StatelessChatStub, fun_mode: bool):
        """Initializes a new instance of the `Conversation` class.

        Args:
            stub: Stub used to communicate with the gRPC API.
        """
        self._stub = stub
        self._conversation_id = uuid.uuid4().hex

        self._conversation = stateless_chat_pb2.StatelessConversation(
            stateless_conversation_id=self._conversation_id,
            responses=[],
            system_prompt_name="fun" if fun_mode else "",
        )

    @property
    def history(self) -> Sequence[stateless_chat_pb2.StatelessResponse]:
        """Returns the linear conversation history."""
        return self._conversation.responses

    @property
    def fun_mode(self) -> bool:
        """Returns true if the conversation happens in fun mode."""
        return self._conversation.system_prompt_name == "fun"

    async def add_response_no_stream(
        self, user_message: str
    ) -> stateless_chat_pb2.StatelessResponse:
        """Same as `add_response` but doesn't return a token stream.

        Use this function if you are only interested in the complete response and don't need to
        stream the individual tokens.

        Args:
            user_message: Message the user has entered.

        Returns:
            The newly generated response.
        """
        stream, response = self.add_response(user_message)

        # We have to iterate over the stream to generate the final response.
        async for _ in stream:
            pass

        response = await response
        return response

    def add_response(
        self, user_message: str
    ) -> tuple[AsyncGenerator[str, None], asyncio.Future[stateless_chat_pb2.StatelessResponse]]:
        """Adds a new user response to the conversation and samples a model response in return.

        Args:
            user_message: Message the user has entered.

        Returns:
            A tuple of the form `token_stream, response` where `token_stream` is an async iterable
                that emits the individual string tokens of the newly sampled response and `response`
                is a future that resolves to the Response object created.
        """
        self._conversation.responses.append(
            stateless_chat_pb2.StatelessResponse(
                sender=stateless_chat_pb2.StatelessResponse.Sender.HUMAN,
                message=user_message,
            )
        )

        response_future: asyncio.Future[stateless_chat_pb2.StatelessResponse] = asyncio.Future()

        async def _unroll_tokens():
            """Unrolls the token stream."""
            try:
                response = stateless_chat_pb2.StatelessResponse(
                    sender=stateless_chat_pb2.StatelessResponse.Sender.ASSISTANT,
                    message="",
                    query="",
                )

                async for update in self._stub.AddResponse(self._conversation):
                    if update.message:
                        response.message += update.message
                        yield update.message

                    if update.query:
                        response.query += update.query

                self._conversation.responses.append(response)
                response_future.set_result(response)
            except Exception as e:
                response_future.set_exception(e)

        return _unroll_tokens(), response_future
