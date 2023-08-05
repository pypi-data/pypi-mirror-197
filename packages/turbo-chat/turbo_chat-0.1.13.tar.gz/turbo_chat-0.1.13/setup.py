# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['turbo_chat']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.4,<4.0.0',
 'openai>=0.27.0,<0.28.0',
 'pydantic>=1.10.5,<2.0.0',
 'tenacity>=8.2.2,<9.0.0']

setup_kwargs = {
    'name': 'turbo-chat',
    'version': '0.1.13',
    'description': 'Idiomatic way to build chatgpt apps using async generators in python',
    'long_description': '# turbo-chat\n\n> Idiomatic way to build chatgpt apps using async generators in python\n\nThe [ChatGPT API](https://openai.com/blog/introducing-chatgpt-and-whisper-apis) uses a new input format called [chatml](https://github.com/openai/openai-python/blob/main/chatml.md). In openai\'s [python client](https://github.com/openai/openai-python/blob/main/chatml.md), the format is used something like this:\n\n```python\nmessages = [\n    {"role": "system", "content": "Greet the user!"},\n    {"role": "user", "content": "Hello world!"},\n]\n```\n\nThe idea here is to incrementally build the messages using an async generator and then use that to generate completions. [Async generators](https://superfastpython.com/asynchronous-generators-in-python/) are incredibly versatile and simple abstraction for doing this kind of stuff. They can also be composed together very easily.\n\n```python\n# Equivalent turbo-chat generator\nasync def example():\n    yield System(content="Greet the user!")\n    yield User(content="Hello World!")\n\n    # To run generation, just yield Generate(),\n    # the lib will take care of correctly running the app, and\n    # return the value back here.\n    output = yield Generate()\n    print(output.content)\n```\n\nSee more detailed example below.\n\n## Installation\n\n```bash\npip install turbo-chat\n```\n\n## Example\n\n```python\nfrom typing import AsyncGenerator, Union\n\nfrom turbo_chat import (\n    turbo,\n    System,\n    User,\n    Assistant,\n    GetUserInput,\n    Generate,\n    run,\n)\n\n# Get user\nasync def get_user(id):\n    return {"zodiac": "pisces"}\n\n# Set user zodiac mixin\n# Notice that no `@turbo()` decorator used here\nasync def set_user_zodiac(context: dict):\n\n    user_id: int = context["user_id"]\n    user_data: dict = await get_user(user_id)\n    zodiac: str = user_data["zodiac"]\n\n    yield User(content=f"My zodiac sign is {zodiac}")\n\n\n# Horoscope app\n@turbo(temperature=0.0)\nasync def horoscope(context: dict):\n\n    yield System(content="You are a fortune teller")\n\n    # Yield from mixin\n    async for output in set_user_zodiac(context):\n        yield output\n\n    # Prompt runner to ask for user input\n    input = yield GetUserInput(message="What do you want to know?")\n\n    # Yield the input\n    yield User(content=input)\n\n    # Generate (overriding the temperature)\n    value = yield Generate(settings={"temperature": 0.9})\n\n\n# Let\'s run this\napp: AsyncGenerator[Union[Assistant, GetUserInput], str] = horoscope({"user_id": 1})\n\n_input = None\nwhile response := await run(app, _input):\n    result, done = response\n\n    if isinstance(result, GetUserInput):\n        _input = input(result.message)\n        continue\n\n    if isinstance(result, Assistant):\n        print(result.content)\n\n    if done:\n        break\n\n# Output\n# >>> What do you want to know? Tell me my fortune\n# >>> As an AI language model, I cannot predict the future or provide supernatural fortune-telling. However, I can offer guidance and advice based on your current situation and past experiences. Is there anything specific you would like me to help you with?\n#\n\n```\n\n### Custom memory\n\nYou can also customize how the messages are persisted in-between the executions.\n\n```python\nfrom turbo_chat import turbo, BaseMemory\n\nclass RedisMemory(BaseMemory):\n    """Implement BaseMemory methods here"""\n\n    async def init(self, context) -> None:\n        ...\n\n    async def append(self, item) -> None:\n        ...\n\n    async def clear(self) -> None:\n        ...\n\n\n# Now use the memory in a turbo_chat app\n@turbo(memory_class=RedisMemory)\nasync def app(context):\n    ...\n```\n\n### Get access to memory object directly (just declare an additional param)\n\n```python\n@turbo()\nasync def app(context: dict, memory: BaseMemory):\n\n    messages = await memory.get()\n    ...\n```\n\n### Generate a response to use internally but don\'t yield downstream\n\n```python\n@turbo()\nasync def example(context):\n    yield System(content="You are a good guy named John")\n    yield User(content="What is your name?")\n    result = yield Generate(yield_downstream=False)\n\n    yield User(content="How are you doing?")\n    result = yield Generate()\n\nb = example()\nresults = [output async for output in b]\n\nassert len(results) == 1\n```\n\n### Add a simple in-memory cache\n\nYou can also subclass the `BaseCache` class to create a custom cache.\n\n```python\ncache = SimpleCache()\n\n@turbo(cache=cache)\nasync def example(context={}):\n    yield System(content="You are a good guy named John")\n    yield User(content="What is your name?")\n    result = yield Generate()\n\nb = example()\nresults = [output async for output in b]\n\nassert len(cache.cache) == 1\n\n```\n\n---\n\n![turbo](https://user-images.githubusercontent.com/931887/222912628-8662fad0-091f-4cb8-92f3-6cce287716e9.jpg)\n',
    'author': 'Diwank Singh Tomer',
    'author_email': 'singh@diwank.name',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
