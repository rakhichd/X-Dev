"""A library that mimics the PromptIDE SDK.

Using this library allows users to run a script developed in the IDE locally.
"""

import contextlib
import contextvars
import dataclasses
import logging
import random
import time
import uuid
from typing import Any, Optional, Sequence, Union

from . import client as _client
from . import sampler

_USER = 1
_MODEL = 2


# The client used by the ide.
_CLIENT: _client.Client | None = None


def set_client(client: _client.Client):
    """Sets the client use by the IDE SDK."""
    global _CLIENT
    _CLIENT = client


def get_client() -> _client.Client:
    """Returns the client used by the IDE."""
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = _client.Client()
    return _CLIENT


async def user_input(text: str) -> str | None:
    """Asks the user to enter a string.

    Args:
        text: The prompt presented to the user.

    Returns:
        A string if the user actually entered some text and `None` if the input is empty.
    """
    response = input(text)
    if not response:
        return None
    return response


@dataclasses.dataclass
class SampleResult:
    """Holds the results of a sampling call."""

    # The of tokens sampled.
    tokens: list[sampler.Token] = dataclasses.field(default_factory=list)
    # When sampling was started.
    start_time: float = dataclasses.field(default_factory=time.time)
    # Time when the first token was added.
    first_token_time: Optional[float] = None
    # When sampling finished.
    end_time: Optional[float] = None

    def as_string(self) -> str:
        """Returns a string representation of this context."""
        return "".join(t.token_str for t in self.tokens)

    def append(self, token: sampler.Token):
        """Adds a token to the result and reports progress in the terminal."""
        self.tokens.append(token)
        self.end_time = time.time()
        if len(self.tokens) == 1:
            self.first_token_time = time.time()
            duration = (self.first_token_time - self.start_time) * 1000
            logging.debug(f"Sampled first token after %.2fms.", duration)
        elif (len(self.tokens) + 1) % 10 == 0:
            self.print_progress()

    def print_progress(self):
        """Prints the sampling progress to stdout."""
        if len(self.tokens) > 1:
            duration = self.end_time - self.first_token_time
            speed = (len(self.tokens) - 1) / duration
            logging.debug(f"Sampled {len(self.tokens)} tokens. " f"%.2f tokens/s", speed)


@dataclasses.dataclass
class Context:
    """A context is a sequence of tokens that are used as prompt when sampling from the model."""

    # The context ID.
    context_id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))
    # The body of this context is a sequence of tokens and child-contexts. The reasons we use a
    # joint body field instead of separate fields is that we want to render the child contexts
    # relative to the tokens of the parent context.
    body: list[Union[sampler.Token, "Context"]] = dataclasses.field(default_factory=list)
    # The parent context if this is not the root context.
    parent: Optional["Context"] = None
    # The seed used for the next call to `sample`.
    next_rng_seed: int = 0
    # Name of the model to use. The model name is tied to the context because different models can
    # use different tokenizers.
    model_name: str = ""

    # If this context has been manually entered, the reset token to reset the global context
    # variable.
    _reset_token: Any = None

    def __post_init__(self):
        """Sends this context to the UI thread to be displayed in the rendering dialogue."""
        if self.parent is not None:
            self.parent.body.append(self)

    def select_model(self, model_name: str):
        """Selects the model name for this context.

        The model name can only be set before any tokens have been added to this context.

        Args:
            model_name: Name of the model to use.
        """
        if self.tokens:
            raise RuntimeError(
                "Cannot change the model name of a non-empty context. A context "
                "stores token sequences and different models may use different "
                "tokenizers. Hence, using tokens across models leads to undefined "
                "behavior. If you want to use multiple models in the same prompt, "
                "consider using a @prompt_fn."
            )
        self.model_name = model_name

    async def tokenize(self, text: str) -> list[sampler.Token]:
        """Tokenizes the given text and returns a list of individual tokens.

        Args:
            text: Text to tokenize.

        Returns:
            List of tokens. The log probability on the logit is initialized to 0.
        """
        return await get_client().sampler.tokenize(text, self.model_name)

    @property
    def tokens(self) -> Sequence[sampler.Token]:
        """Returns the tokens stored in this context."""
        return [t for t in self.body if isinstance(t, sampler.Token)]

    @property
    def children(self) -> Sequence["Context"]:
        """Returns all child contexts."""
        return [c for c in self.body if isinstance(c, Context)]

    def as_string(self) -> str:
        """Returns a string representation of this context."""
        return "".join(t.token_str for t in self.tokens)

    def as_token_ids(self) -> list[int]:
        """Returns a list of token IDs stored in this context."""
        return [t.token_id for t in self.tokens]

    async def prompt(self, text: str, strip: bool = False) -> Sequence[sampler.Token]:
        """Tokenizes the argument and adds the tokens to the context.

        Args:
            text: String to tokenize and add to the context.
            strip: If true, any whitespace surrounding `prompt` will be stripped.

        Returns:
            Tokenized string.
        """
        if strip:
            text = text.strip()
        tokens = await get_client().sampler.tokenize(text, self.model_name)
        self.body.extend(tokens)
        return tokens

    def randomize_rng_seed(self) -> int:
        """Samples a new RNG seed and returns it."""
        self.next_rng_seed = random.randint(0, 100000)
        return self.next_rng_seed

    def create_context(self) -> "Context":
        """Creates a new context and adds it as child context."""
        child = Context(
            parent=self,
            next_rng_seed=self._get_next_rng_seed(),
            model_name=self.model_name,
        )
        return child

    def _get_next_rng_seed(self) -> int:
        """Returns the next RNG seed."""
        self.next_rng_seed += 1
        return self.next_rng_seed - 1

    async def sample(
        self,
        max_len: int = 256,
        temperature: float = 1.0,
        nucleus_p: float = 0.7,
        stop_tokens: Optional[list[str]] = None,
        stop_strings: Optional[list[str]] = None,
        rng_seed: Optional[int] = None,
        add_to_context: bool = True,
        return_attention: bool = False,
        allowed_tokens: Optional[Sequence[Union[int, str]]] = None,
        disallowed_tokens: Optional[Sequence[Union[int, str]]] = None,
        augment_tokens: bool = True,
    ) -> SampleResult:
        """Generates a model response based on the current prompt.

        The current prompt consists of all text that has been added to the context either since the
        beginning of the program.

        Args:
            max_len: Maximum number of tokens to generate.
            temperature: Temperature of the final softmax operation. The lower the temperature, the
                lower the variance of the token distribution. In the limit, the distribution collapses
                onto the single token with the highest probability.
            nucleus_p: Threshold of the Top-P sampling technique: We rank all tokens by their
                probability and then only actually sample from the set of tokens that ranks in the
                Top-P percentile of the distribution.
            stop_tokens: A list of strings, each of which will be mapped independently to a single
                token. If a string does not map cleanly to one token, it will be silently ignored.
                If the network samples one of these tokens, sampling is stopped and the stop token
                *is not* included in the response.
            stop_strings: A list of strings. If any of these strings occurs in the network output,
                sampling is stopped but the string that triggered the stop *will be* included in the
                response. Note that the response may be longer than the stop string. For example, if
                the stop string is "Hel" and the network predicts the single-token response "Hello",
                sampling will be stopped but the response will still read "Hello".
            rng_seed: See of the random number generator used to sample from the model outputs.
            add_to_context: If true, the generated tokens will be added to the context.
            return_attention: If true, returns the attention mask. Note that this can significantly
                increase the response size for long sequences.
            allowed_tokens: If set, only these tokens can be sampled. Invalid input tokens are
                ignored. Only one of `allowed_tokens` and `disallowed_tokens` must be set.
            disallowed_tokens: If set, these tokens cannot be sampled. Invalid input tokens are
                ignored. Only one of `allowed_tokens` and `disallowed_tokens` must be set.
            augment_tokens: If true, strings passed to `stop_tokens`, `allowed_tokens` and
                `disallowed_tokens` will be augmented to include both the passed token and the
                version with leading whitespace. This is useful because most words have two
                corresponding vocabulary entries: one with leading whitespace and one without.

        Returns:
            The generated text.
        """
        if rng_seed is None:
            rng_seed = self._get_next_rng_seed()

        logging.debug(
            f"Generating %d tokens [seed=%d, temperature=%f, "
            f"nucleus_p=%f, stop_tokens=%s, stop_strings=%s].",
            max_len,
            rng_seed,
            temperature,
            nucleus_p,
            stop_tokens,
            stop_strings,
        )

        result = SampleResult()
        async for token in get_client().sampler.sample(
            prompt=self.as_token_ids(),
            max_len=max_len,
            temperature=temperature,
            nucleus_p=nucleus_p,
            stop_tokens=stop_tokens,
            stop_strings=stop_strings,
            rng_seed=rng_seed,
            return_attention=return_attention,
            allowed_tokens=allowed_tokens,
            disallowed_tokens=disallowed_tokens,
            augment_tokens=augment_tokens,
        ):
            result.append(token)
            if add_to_context:
                self.body.append(token)

        result.print_progress()
        return result

    def clone(self) -> "Context":
        """Clones the current prompt."""
        # We can't use deepcopy here because we need to make sure the clone is correctly synced to
        # the UI thread.
        clone = Context(
            # We only clone the tokens, not the child contexts.
            body=list(self.tokens),
            parent=self,
            next_rng_seed=self.next_rng_seed,
        )
        self.body.append(clone)
        return clone

    async def set_title(self, title: str):
        """Sets the title of the context, which is shown in the UI."""
        # This is only relevant in the UI.
        pass

    def __enter__(self):
        """Uses this context as the current context."""
        if self._reset_token is not None:
            raise RuntimeError("Cannot enter a context twice.")
        self._reset_token = _current_ctx.set(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exits the context and resets the global state."""
        _current_ctx.reset(self._reset_token)
        self._reset_token = None


# The current context, which is used by the free-functions below.
_current_ctx = contextvars.ContextVar("root_ctx", default=Context(context_id=""))

# If set, overrides the current context. Useful to ignore newly created contexts in `prompt_fn`.
_force_ctx = contextvars.ContextVar("force_ctx", default=None)


def get_context() -> Context:
    """Returns the current context."""
    if _force_ctx.get() is not None:
        return _force_ctx.get()
    return _current_ctx.get()


@contextlib.contextmanager
def force_context(ctx: Context):
    """Overrides the current context with the provided one."""
    token = _force_ctx.set(ctx)
    try:
        yield
    finally:
        _force_ctx.reset(token)


# The following functions operate on the current context.


def as_string() -> str:
    """See `Context.as_string`."""
    return get_context().as_string()


def select_model(model_name: str):
    """See `Context.select_model`."""
    return get_context().select_model(model_name)


def as_token_ids() -> list[int]:
    """See `Context.as_token_ids`."""
    return get_context().as_token_ids()


async def prompt(text: str, strip: bool = False) -> Sequence[sampler.Token]:
    """See `Context.prompt`."""
    return await get_context().prompt(text, strip)


def randomize_rng_seed() -> int:
    """See `Context.randomize_rng_seed`."""
    return get_context().randomize_rng_seed()


def create_context() -> "Context":
    """See `Context.create_context()`."""
    return get_context().create_context()


async def set_title(title: str):
    """See `Context.set_title`."""
    await get_context().set_title(title)


async def sample(
    max_len: int = 256,
    temperature: float = 1.0,
    nucleus_p: float = 0.7,
    stop_tokens: Optional[list[str]] = None,
    stop_strings: Optional[list[str]] = None,
    rng_seed: Optional[int] = None,
    add_to_context: bool = True,
    return_attention: bool = False,
    allowed_tokens: Optional[Sequence[Union[int, str]]] = None,
    disallowed_tokens: Optional[Sequence[Union[int, str]]] = None,
):
    """See `Context.sample`."""
    return await get_context().sample(
        max_len,
        temperature,
        nucleus_p,
        stop_tokens,
        stop_strings,
        rng_seed,
        add_to_context,
        return_attention,
        allowed_tokens,
        disallowed_tokens,
    )


def clone() -> "Context":
    """See `Context.clone`."""
    return get_context().clone()


def prompt_fn(fn):
    """A context manager that executes `fn` in a fresh prompt context.

    If a function is annotated with this context manager, a fresh prompt context is created that
    the function operates on. This allows solving sub-problems with different prompt and
    incorporating the solution to a sub problems into the original one.

    Example:
        ```
        @prompt_fn
        async def add(a, b):
            prompt(f"{a}+{b}=")
            result = await sample(max_len=10, stop_strings=[" "])
            return result.as_string().split(" ")[0]
        ```

    In order to get access to the context used by an annotated function, the function must return
    it like this:

    ```
        @prompt_fn
        def foo():
            return get_context()
    ```

    You can override the context an annotated function uses. This is useful if you want to continue
    operating on a context that was created by a function.

    ```
        @prompt_fn
        async def bar():
            async prompt("1+1=")
            return get_context()

        @prompt_fn
        async def foo():
            await sample(max_len=24)

        ctx = await bar()
        with force_context(ctx):
            foo()
    ```

    Args:
        fn: An asynchronous function to execute in a newly created context.

    Returns:
        The wrapped function.
    """

    async def _fn(*args, **kwargs):
        with get_context().create_context() as ctx:
            await ctx.set_title(fn.__name__)
            return await fn(*args, **kwargs)

    return _fn


async def read_file(file_name: str) -> bytes:
    """Reads a file that the user has uploaded to the file manager.

    Args:
        file_name: Name of the file to read.

    Returns:
        The file's content as raw bytes array.
    """
    content = await get_client().files.download(file_name)
    return content


async def write_file(
    file_name: str,
    content: bytes,
    mime_type: str = "application/octet-stream",
    overwrite: bool = True,
):
    """Stores a file in the IDE.

    Args:
        file_name: Name of the file to write.
        content: File content as a byte array.
        mime_type: The MIME type of the file.
        overwrite: If the file already exists, overwrite it.
    """
    await get_client().files.upload(file_name, content, mime_type, overwrite)
