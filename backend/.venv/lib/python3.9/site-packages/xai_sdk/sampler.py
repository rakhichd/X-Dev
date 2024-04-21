"""Sampler API to generate text completions.

This API gives access to the raw underlying models and is the most versatile and complex way to
interact with our models.
"""

import dataclasses
import logging
import random
from typing import AsyncGenerator, Optional, Sequence, Union

from .proto import sampler_public_pb2, sampler_public_pb2_grpc


class AsyncSampler:
    """Allows sampling from the raw model API. All functions are asynchronous."""

    def __init__(
        self, stub: sampler_public_pb2_grpc.SamplerStub, initial_rng_seed: Optional[int] = None
    ):
        """Initializes a new instance of the `Sampler` class.

        Args:
            stub: The gRPC stub to use for interacting with the API.
            initial_rng_seed: First RNG seed to use for sampling. Each time we sample from the model
                and no RNG seed is explicitly specified, we deterministically generate a new seed
                based on the initial seed. This ensures that the generated responses are
                deterministic given a call order. If no initial seed is specified, we sample a
                random initial seed.
        """
        if initial_rng_seed is None:
            initial_rng_seed = random.randint(0, 100000)

        self._stub = stub
        self._initial_rng_seed = initial_rng_seed

    def _get_next_rng_seed(self) -> int:
        """Deterministically chooses a new RNG seed based on the initial seed."""
        seed = self._initial_rng_seed
        self._initial_rng_seed += 1
        return seed

    async def tokenize(self, prompt: str, model_name: str = "") -> list["Token"]:
        """Converts the given prompt text into a sequence of discrete tokens.

        Args:
            prompt: Text to convert into a sequence of tokens.
            model_name: Model whose tokenizer should be used. Make sure to use the same value when
                tokenizing and when sampling as different models use different tokenizers. Leave
                empty to use the default model's tokenizer.

        Returns:
            A sequence of discrete tokens that represent the original `prompt` text.
        """
        # Nothing to do if the text is empty.
        if not prompt:
            return []

        logging.debug("Tokenizing prompt with {len(prompt)} characters.")
        response: sampler_public_pb2.TokenizeResponse = await self._stub.Tokenize(
            sampler_public_pb2.TokenizeRequest(text=prompt, model_name=model_name)
        )
        tokens = response.tokens
        compression = (1 - len(tokens) / len(prompt)) * 100
        logging.debug(
            "Tokenization done. %d tokens detected (Compression of %.1f%%).",
            len(tokens),
            compression,
        )

        return [Token.from_proto(token) for token in tokens]

    async def sample(
        self,
        prompt: Union[str, Sequence[int], Sequence["Token"]],
        *,
        model_name: str = "",
        max_len: int = 256,
        temperature: float = 0.7,
        nucleus_p: float = 0.95,
        stop_tokens: Optional[list[str]] = None,
        stop_strings: Optional[list[str]] = None,
        rng_seed: Optional[int] = None,
        return_attention: bool = False,
        allowed_tokens: Optional[Sequence[Union[int, str]]] = None,
        disallowed_tokens: Optional[Sequence[Union[int, str]]] = None,
        augment_tokens: bool = True,
    ) -> AsyncGenerator["Token", None]:
        """Generates a model response by continuing `prompt`.

        Args:
            prompt: Prompt to continue. This can either be a string, a sequence of token IDs, or a
                sequence of `Token` instances.
            model_name: Name of the model to sample from. Leave empty to sample from the default
                model.
            max_len: Maximum number of tokens to generate.
            temperature: Temperature of the final softmax operation. The lower the temperature, the
                lower the variance of the token distribution. In the limit, the distribution
                collapses onto the single token with the highest probability.
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
            rng_seed: Seed of the random number generator used to sample from the model outputs. If
                unspecified, a seed is chosen deterministically from the `initial_rng_seed`
                specified in the constructor.
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

        Yields:
            A sequence of `Token` instances.
        """
        # If the prompt is empty, there is nothing we can do.
        if not prompt:
            return

        if rng_seed is None:
            rng_seed = self._get_next_rng_seed()

        logging.debug(
            "Sampling %d tokens [seed=%d, temperature=%f, nucleus_p=%f, stop_tokens=%s, "
            "stop_strings=%s].",
            max_len,
            rng_seed,
            temperature,
            nucleus_p,
            stop_tokens,
            stop_strings,
        )

        if augment_tokens:
            # The underscore character here is not an ordinary underscore _, it's a special utf-8
            # character ▁ used by the tokenizer to indicate whitespace.
            if stop_tokens:
                stop_tokens = stop_tokens + [f"▁{t}" for t in stop_tokens]
            if allowed_tokens:
                allowed_tokens = list(allowed_tokens) + [
                    f"▁{t}" for t in allowed_tokens if isinstance(t, str) and not t.startswith("▁")
                ]
            if disallowed_tokens:
                disallowed_tokens = list(disallowed_tokens) + [
                    f"▁{t}"
                    for t in disallowed_tokens
                    if isinstance(t, str) and not t.startswith("▁")
                ]

        prompt = await self._prompt_to_token_ids(prompt, model_name)
        request = sampler_public_pb2.SampleTokensRequest(
            prompt=prompt,
            settings=sampler_public_pb2.SampleSettings(
                max_len=max_len or 0,
                temperature=temperature,
                nucleus_p=nucleus_p,
                stop_tokens=stop_tokens or [],
                stop_strings=stop_strings or [],
                rng_seed=rng_seed,
                allowed_tokens=[_parse_input_token(t) for t in allowed_tokens or []],
                disallowed_tokens=[_parse_input_token(t) for t in disallowed_tokens or []],
            ),
            return_attention=return_attention,
            model_name=model_name,
        )

        response = self._stub.SampleTokens(request)

        token_counter = 0
        async for token in response:
            if token.HasField("token"):
                token_counter += 1
                if token_counter % 10 == 0:
                    logging.debug("Sampled %d tokens", token_counter)
                yield Token.from_proto(token.token)
            elif token.HasField("budget"):
                # The sample request also sends the current token budget information.
                log_budget_update(token.budget)

    async def _prompt_to_token_ids(
        self, prompt: Union[str, Sequence[int], Sequence["Token"]], model_name: str
    ) -> list[int]:
        """Converts a prompt to a list of token IDs.

        Args:
            prompt: The prompt, which can take one of three formats: A raw string, a sequence of
                integers (which are assumed to be token IDs), or a sequence of `Token` instances.
            model_name: Name of the model to use if we have to call the tokenizer.

        Returns:
            List of token IDs.

        Raises:
            ValueError: If the prompt's type doesn't conform to our assumptions.
        """
        assert prompt, "Prompt must not be empty."

        if isinstance(prompt, str):
            # The prompt is a raw string, tokenize it and extract the token IDs.
            tokens = await self.tokenize(prompt, model_name)
            return [t.token_id for t in tokens]
        elif isinstance(prompt, Sequence):
            # Check the type of the first item in the list and assume all items are of the same
            # type.
            if isinstance(prompt[0], int):
                # The prompt is already in the form of a list of integers. Nothing to do here.
                return list(prompt)
            elif isinstance(prompt[0], Token):
                # Extract the token IDs from the sequence of token instances.
                return [t.token_id for t in prompt]

        raise ValueError(
            f"Prompt must be either a string, a list of token IDs, or a sequence of "
            f"Token instance. Given prompt was neither. Prompt: {prompt}"
        )


@dataclasses.dataclass(frozen=True)
class Token:
    """A token is an element of our vocabulary that has a unique index and string representation.

    A token can either be sampled from a model or provided by the user (i.e. prompted). If the token
    comes from the mode, we may have additional metadata such as its sampling probability, the
    attention pattern used when sampling the token, and alternative tokens.
    """

    # The integer representation of the token. Corresponds to its index in the vocabulary.
    token_id: int
    # The string representation of the token. Corresponds to its value in the vocabulary.
    token_str: str
    # If this token was sampled, the token sampling probability. 0 if not sampled.
    prob: float
    # If this token was sampled, alternative tokens that could have been sampled instead.
    top_k: list["Token"]
    # If this token was sampled with the correct options, the token's attention pattern. The array
    # contains one value for every token in the context.
    attn_weights: list[float]
    # 1 if this token was created by a user and 2 if it was created by model.
    token_type: int

    @classmethod
    def from_proto(cls, proto: sampler_public_pb2.Token) -> "Token":
        """Converts the protocol buffer instance to a `Token` instance."""
        return Token(
            token_id=proto.final_logit.token_id,
            token_str=proto.final_logit.string_token,
            prob=proto.final_logit.prob,
            top_k=[
                Token.from_proto(
                    sampler_public_pb2.Token(
                        final_logit=logit,
                        top_k=[],
                        attention=[],
                        token_type=sampler_public_pb2.Token.TokenType.MODEL,
                    )
                )
                for logit in proto.top_k
            ],
            attn_weights=[a for a in proto.attention],
            token_type=proto.token_type,
        )


def log_budget_update(budget: sampler_public_pb2.TokenBudget) -> None:
    """Logs a budget update."""
    logging.info(
        "xAI Tokens used: %d (%f.1%%). Token limit: %d",
        budget.tokens_spent,
        budget.tokens_spent / budget.token_limit * 100,
        budget.token_limit,
    )


def _parse_input_token(token: Union[int, str]) -> sampler_public_pb2.InputToken:
    """Converts the argument to an `InputToken` proto."""
    if isinstance(token, int):
        return sampler_public_pb2.InputToken(token_id=token)
    elif isinstance(token, str):
        return sampler_public_pb2.InputToken(string_token=token)
    else:
        raise ValueError(f"Invalid token type {type(token)}.")
