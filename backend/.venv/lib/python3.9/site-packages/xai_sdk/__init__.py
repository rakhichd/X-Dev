"""xAI Software Development Kit (SDK).

This SDK lets you interact with the xAI API. In order to access the API, you need to generate an
API key in our IDE, which is available under ide.x.ai. After signing in, click on your username in
the top right hand corner and select "API Keys". Generate a new API key and make sure to assign the
correct ACLs. In order to sample from the model, you need the `chat:write` or `sampler:write` ACLs.
"""

import asyncio

from .client import Client


def does_it_work():
    """Prints "Yes, it does." if API access works.

    This function can be used to quickly check if API access works by running the following command:

    ```shell
    python -c "import xai_sdk; xai_sdk.does_it_work()"
    ```
    """

    async def _run():
        prompt = "Yes, it does. Yes, it does. Yes, it does. Yes, it does. Yes, it does."
        print("Does it work?", end="")
        async for token in Client().sampler.sample(prompt, stop_strings=["."]):
            print(token.token_str, end="")
        print("")

    asyncio.run(_run())
