"""Grok API for conversations."""

import asyncio
import datetime
import logging
from typing import AsyncGenerator, Generator, Optional

from google.protobuf import empty_pb2, timestamp_pb2

from . import sampler
from .proto import chat_pb2, chat_pb2_grpc, sampler_public_pb2


class AsyncGrok:
    """Allows talking to Grok via the API.

    Note that all conversations performed via this API will show up on grok.x.ai too. So, do NOT use
    this API to build new products as it's personalized to your user. Use the `chat` API instead.
    """

    def __init__(self, stub: chat_pb2_grpc.ChatStub):
        """Initializes a new instance of the `AsyncGrok` class.

        Args:
            stub: gRPC Stub used to communicate with the xAI API.
        """
        self._stub = stub

    def create_conversation(self, model_name: str = "", fun_mode: bool = False) -> "Conversation":
        """Creates a new empty conversation.

        Args:
            model_name: Name of the model to use for this conversation. Leave empty to use the
                default model.
            fun_mode: Whether fun mode shall be enabled for this conversation.

        Returns:
            Newly created conversation.
        """
        return Conversation(self._stub, model_name, fun_mode, None)

    async def get_conversation(
        self, conversation_id: str, model_name: str = "", fun_mode: bool = False
    ) -> "Conversation":
        """Loads an existing conversation based on its ID.

        Args:
            conversation_id: ID of the conversation to load.
            model_name: Name of the model to use for this conversation. Leave empty to use the
                default model.
            fun_mode: Whether fun mode shall be enabled for this conversation.

        Returns:
            Loaded conversation.
        """
        c = Conversation(self._stub, model_name, fun_mode, conversation_id)
        await c.load()
        return c

    async def list_conversations(self) -> list[chat_pb2.Conversation]:
        """Returns a list of all conversations."""
        response: chat_pb2.ListConversationsResponse = await self._stub.ListConversations(
            empty_pb2.Empty()
        )
        return list(response.conversations)


class Conversation:
    """SDK for interacting with a Grok conversation.

    A Grok conversation is composed of a forest of responses. It's not a tree because there can be
    multiple root nodes. Each connected component in the response graph is, however, a tree.
    Responses can be created by a human user or sampled from Grok. Users can also store responses
    with Grok indicated as the sender, which is useful for debugging and research purposes.

    Note that the properties of the conversation are cached client-side.

    Important: A single conversation is not thread-safe. Only a single response must be sampled at
    any point in time.
    """

    def __init__(
        self,
        stub: chat_pb2_grpc.ChatStub,
        model_name: str,
        fun_mode: bool,
        conversation_id: Optional[str],
        dev_only_use_grok: bool = True,
    ):
        """Initializes a new instance of the `Conversation` class.

        Args:
            stub: gRPC stub used to communicate with the xAI API.
            model_name: Name of the model to use for this conversation.
            fun_mode: True if fun mode shall be enabled for this conversation.
            conversation_id: ID of this conversation. If no ID was provided, a new conversation is
                created when the first API call is issued.
            dev_only_use_grok: By setting this to `False`, the conversation is with the raw model
                instead of with Grok. This means there is no support for searching or fun mode.
        """
        self._stub = stub
        self._model_name = model_name
        self._fun_mode = fun_mode
        self._conversation_id: Optional[str] = conversation_id
        self._conversation: Optional[chat_pb2.Conversation] = None
        self._use_grok = dev_only_use_grok

        # True if this conversation was deleted.
        self._deleted = False

        # A mapping from response IDs to the respective response objects.
        self._responses: dict[str, "Response"] = {}

        # ID of the chat response to which will become the parent of the next response in the
        # response graph. None if a new root response shall be created.
        self._leaf_response_id: Optional[str] = None

    @property
    def conversation_id(self) -> str:
        """Returns the ID of this conversation.

        Raises:
            ValueError: if no actual conversation has been created or loaded yet.
        """
        self._check_not_deleted()
        return self._get_conversation_or_raise().conversation_id

    @property
    def title(self) -> str:
        """Returns the title of this conversation.

        Raises:
            ValueError: if no actual conversation has been created or loaded yet.
        """
        self._check_not_deleted()
        return self._get_conversation_or_raise().title

    @property
    def create_time(self) -> datetime.datetime:
        """Returns the time when this conversation was created.

        Raises:
            ValueError: if no actual conversation has been created or loaded yet.
        """
        self._check_not_deleted()
        return _convert_proto_timestamp(self._get_conversation_or_raise().create_time)

    @property
    def starred(self) -> bool:
        """Returns whether the conversation is starred.

        Raises:
            ValueError: if no actual conversation has been created or loaded yet.
        """
        self._check_not_deleted()
        return self._get_conversation_or_raise().starred

    async def set_title(self, title: str):
        """Updates the title of this conversation.

        Args:
            title: New title of the conversation.
        """
        self._check_not_deleted()
        await self._stub.UpdateConversation(
            chat_pb2.UpdateConversationRequest(
                conversation_id=self._get_conversation_or_raise().conversation_id,
                title=title,
                starred=self._get_conversation_or_raise().starred,
            )
        )
        self._conversation.title = title

    async def generate_title(self) -> str:
        """Automatically generates a title for this conversation.

        Returns:
            The newly generated title.
        """
        self._check_not_deleted()
        response: chat_pb2.GenerateTitleResponse = await self._stub.GenerateTitle(
            chat_pb2.GenerateTitleRequest(
                conversation_id=self._get_conversation_or_raise().conversation_id,
                leaf_response_id=self._leaf_response_id or "",
            )
        )
        self._conversation.title = response.new_title
        return response.new_title

    async def star(self):
        """Stars this conversation."""
        self._check_not_deleted()
        await self._stub.UpdateConversation(
            chat_pb2.UpdateConversationRequest(
                conversation_id=self._get_conversation_or_raise().conversation_id,
                title=self._get_conversation_or_raise().title,
                starred=True,
            )
        )
        self._conversation.starred = True

    async def unstar(self):
        """Unstars this conversation."""
        self._check_not_deleted()
        await self._stub.UpdateConversation(
            chat_pb2.UpdateConversationRequest(
                conversation_id=self._get_conversation_or_raise().conversation_id,
                title=self._get_conversation_or_raise().title,
                starred=False,
            )
        )
        self._conversation.starred = False

    async def load(self):
        """Loads the conversation and all its responses from the API.

        Raises:
            ValueError: If no conversation ID was provided.
        """
        self._check_not_deleted()
        if self._conversation_id is None:
            raise ValueError("Cannot load conversation without providing conversation ID.")

        self._conversation = await self._stub.GetConversation(
            chat_pb2.GetConversationRequest(conversation_id=self._conversation_id)
        )

        # Clear the response cache.
        self._responses = {
            r.response_id: Response(r, self, self._stub) for r in self._conversation.responses
        }

        # Update the leave response ID to the most recently generated message.
        if self._conversation.responses:
            self._leaf_response_id = self._conversation.responses[-1].response_id

    async def delete(self):
        """Deletes this conversation."""
        self._check_not_deleted()
        await self._stub.DeleteConversation(
            chat_pb2.DeleteConversationRequest(
                conversation_id=self._get_conversation_or_raise().conversation_id
            )
        )
        self._deleted = True

    def add_response(
        self, user_message: str
    ) -> tuple[AsyncGenerator[str, "Response"], asyncio.Future["Response"]]:
        """Adds a new response to this conversation.

        The response is added to the graph with its parent being the current `leaf` response.

        Args:
            user_message: Message written by the user. If empty, no user response is generated.

        Yields:
            Text snippets emitted by the model.

        Returns:
            A tuple of the form (token_generator, new_model_response). `token_generator` is an async
                generator that emits the individual tokens produced by the model. This can be used
                for applications that require "streaming responses". `new_model_response` is a
                future that evaluates to the generated model response.
        """
        self._check_not_deleted()
        # This is the future that will resolve to the new model response when the for loop finishes.
        new_model_future = asyncio.Future()

        async def _token_stream():
            """Streams out the tokens the model generates."""
            try:
                # If the conversation hasn't been created yet, create it.
                if self._conversation_id is None:
                    await self._create_conversation()

                # If we haven't loaded the conversation yet, load it.
                if self._conversation is None:
                    await self.load()

                # Start sampling from Grok.
                response = self._stub.AddResponse(
                    chat_pb2.AddResponseRequest(
                        conversation_id=self._conversation_id,
                        message=user_message,
                        model_name=self._model_name,
                        parent_response_id=self._leaf_response_id or "",
                        use_grok=self._use_grok,
                        system_prompt_name="fun" if self._fun_mode else "",
                    )
                )

                # Unroll the responses and emit the tokens.
                async for msg in response:
                    if msg.HasField("user_response"):
                        # This is the user response, which was generated from the input message.
                        user_response = Response(msg.user_response, self, self._stub)
                        self._responses[user_response.response_id] = user_response
                    elif msg.HasField("model_response"):
                        # This indicates that the model has finished sampling. Create a new response
                        # object from the generated model response.
                        model_response = Response(msg.model_response, self, self._stub)
                        self._responses[model_response.response_id] = model_response
                        self._leaf_response_id = model_response.response_id
                        new_model_future.set_result(model_response)
                    elif msg.HasField("query_action"):
                        # This message indicates that the model is currently performing a search.
                        # Again, we don't really need this info in the SDK. However, we'll add a log
                        # message for debugging purposes.
                        query: chat_pb2.QueryAction = msg.query_action
                        logging.debug("Model is performing a %s-query: %s", query.type, query.query)
                    elif msg.HasField("token"):
                        token: sampler_public_pb2.SampleTokensResponse = msg.token

                        # This can either be a real message or a budget update.
                        if token.HasField("token"):
                            # Output the emitted text.
                            yield token.token.final_logit.string_token
                        elif token.HasField("budget"):
                            sampler.log_budget_update(token.budget)
            except Exception as e:
                new_model_future.set_exception(e)

            # Raise an exception if no model response was produced.
            if not new_model_future.done():
                new_model_future.set_exception(
                    RuntimeError(
                        "This should never happen (tm). The xAI API didn't behave as expected and "
                        "finished sampling with an OK status but without emitting the final model "
                        "response."
                    )
                )

        return _token_stream(), new_model_future

    @property
    def root_responses(self) -> Generator["Response", None, None]:
        """Returns all root responses in the response graph."""
        self._check_not_deleted()
        for response in self._responses.values():
            if response.parent_response_id is None:
                yield response

    def get_response(self, response_id: str) -> "Response":
        """Returns a response by its ID.

        Args:
            response_id: ID of the response to return.

        Returns:
            KeyError if the response cannot be found.
        """
        self._check_not_deleted()
        return self._responses[response_id]

    def get_children(self, parent_response_id: str) -> Generator["Response", None, None]:
        """Yields all responses whose parent is `parent_response_id`."""
        self._check_not_deleted()
        for response in self._responses.values():
            if response.response_id == parent_response_id:
                yield response

    def set_leaf_response_id(self, leaf_response_id: Optional[str]):
        """Updates the leaf response ID. Don't use this API directly. Prefer `Response.select()`."""
        self._check_not_deleted()
        self._leaf_response_id = leaf_response_id

    def register_response(self, response: "Response"):
        """Manually adds a response to the response graph.

        Don't use this API unless you know what you're doing.
        """
        self._check_not_deleted()
        self._responses[response.response_id] = response

    async def _create_conversation(self):
        """Creates a new conversation."""
        conversation: chat_pb2.Conversation = await self._stub.CreateConversation(
            chat_pb2.CreateConversationRequest()
        )
        self._conversation_id = conversation.conversation_id
        self._conversation = conversation

    def _get_conversation_or_raise(self) -> chat_pb2.Conversation:
        """Returns the conversation proto or raises an error if the proto hasn't been loaded.

        Raises:
            RuntimeError: If the conversation hasn't been loaded.
        """
        if self._conversation_id is None:
            raise ValueError("Cannot access conversation ID before conversation is created.")

        if self._conversation is None:
            raise ValueError("Must call load() before any conversation properties can be accessed.")

        return self._conversation

    def _check_not_deleted(self):
        """Raises an error if the conversation was deleted."""
        if self._deleted:
            raise RuntimeError("Cannot interact with a deleted conversation.")


class Response:
    """Represents a single response in a conversation.

    Note that the properties of the response are cached client-side. Call the refresh function
    """

    def __init__(
        self, response: chat_pb2.Response, conversation: Conversation, stub: chat_pb2_grpc.ChatStub
    ):
        """Initializes a new instance of the `Response` class.

        Args:
            response: Raw proto response object returned from the API.
            conversation: Conversation this response belongs to.
            stub: Stub used to communicate with the xAI API.
        """
        self._response = response
        self._conversation = conversation
        self._stub = stub

    def replace(
        self, new_message: str
    ) -> tuple[AsyncGenerator[str, "Response"], asyncio.Future["Response"]]:
        """Replaces the text of this message with a new text.

        Note: If this is a user response, a new model response will be sampled. If this is a model
        response, it will be replaced by a new response with the given message. In both cases, the
        return value is a model response.
        """
        if self.sender == "human":
            # Add a new user response and sample a new message.
            self._conversation.set_leaf_response_id(self.parent_response_id)
            return self._conversation.add_response(new_message)
        else:

            async def _create_new_response():
                # This is a model response, actually replace the text by creating a new response
                # manually.
                new_response = await self._stub.AddModelResponse(
                    chat_pb2.AddModelResponseRequest(
                        conversation_id=self._conversation.conversation_id,
                        message=new_message,
                        partial=False,
                        parent_response_id=self.parent_response_id,
                    )
                )
                new_response = Response(new_response, self._conversation, self._stub)
                self._conversation.register_response(new_response)
                self._conversation.set_leaf_response_id(new_response.response_id)

            async def _empty_generator():
                if False:
                    yield None

            _empty_generator(), _create_new_response()

    async def resample(self) -> tuple[AsyncGenerator[str, "Response"], asyncio.Future["Response"]]:
        """Resamples this response.

        This adds a new child to the parent response that is sampled from the model.

        Raises:
            ValueError: If this response was generated by human.
        """
        if self.sender == "human":
            raise ValueError("Cannot resample human responses.")
        self._conversation.set_leaf_response_id(self.parent_response_id)

        # If we don't specify a user message, only a model message is sampled.
        return self._conversation.add_response("")

    def select(self):
        """Selects this response to be the most recent one in the conversation.

        Use this to go back to an earlier response.
        """
        self._conversation.set_leaf_response_id(self.response_id)

    async def share(self) -> str:
        """Shares the conversation up to this point publicly.

        Returns:
            The RUL of the shared conversation.
        """
        if not self.shared:
            await self._stub.ShareConversation(
                chat_pb2.ShareConversationRequest(
                    conversation_id=self._conversation.conversation_id, response_id=self.response_id
                )
            )
            self._response.shared = True
        return f"https://share.x.ai/conversations/{self.response_id}"

    @property
    def parent_response(self) -> Optional["Response"]:
        """Returns the parent response of None if this is a root response.

        Raises:
            KeyError: If the parent response cannot be found.
        """
        if self.parent_response_id is not None:
            try:
                return self._conversation.get_response(self.parent_response_id)
            except KeyError as e:
                raise KeyError(
                    f"Cannot find parent response with ID {self.parent_response_id}."
                ) from e
        return None

    @property
    def children(self) -> list["Response"]:
        """Returns a list of all child responses."""
        return list(self._conversation.get_children(self.response_id))

    @property
    def response_id(self) -> str:
        """Returns the ID of this response."""
        return self._response.response_id

    @property
    def message(self) -> str:
        """Returns the message content."""
        return self._response.message

    @property
    def sender(self) -> str:
        """Returns the sender of this message. "human" indicates the message was sent by a human."""
        return self._response.sender

    @property
    def create_time(self) -> datetime.datetime:
        """Returns the time when this response was created."""
        return _convert_proto_timestamp(self._response.create_time)

    @property
    def parent_response_id(self) -> Optional[str]:
        """Returns the ID of the parent response in the response graph."""
        return self._response.parent_response_id or None

    @property
    def manual(self) -> bool:
        """Returns True if the response was created manually via the API."""
        return self._response.manual

    @property
    def partial(self) -> bool:
        """Returns True if the response represents a partial model output."""
        return self._response.partial

    @property
    def shared(self) -> bool:
        """Returns True if the response was shared publicly."""
        return self._response.shared

    @property
    def query(self) -> str:
        """Returns the query string used by the model if the model performed a query."""
        return self._response.query

    @property
    def query_type(self) -> str:
        """Returns the type of query performed by the model if it performed a query."""
        return self._response.query_type


def _convert_proto_timestamp(timestamp: timestamp_pb2.Timestamp) -> datetime.datetime:
    """Converts a proto timestamp to a Python `datetime` object."""
    return datetime.datetime.fromtimestamp(timestamp.seconds + timestamp.nanos / 1e9)
