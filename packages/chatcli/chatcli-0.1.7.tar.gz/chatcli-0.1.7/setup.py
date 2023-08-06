# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['chatcli']
install_requires = \
['fire>=0.5.0,<0.6.0',
 'openai>=0.27.0,<0.28.0',
 'prompt-toolkit>=3.0.38,<4.0.0']

entry_points = \
{'console_scripts': ['chatcli = chatcli:chatcli']}

setup_kwargs = {
    'name': 'chatcli',
    'version': '0.1.7',
    'description': "Streaming CLI interface for OpenAI's Chat API",
    'long_description': '# ChatCLI\n\nChatCLI is a command line interface for OpenAI\'s Chat API.\n\n ChatCLI aims to provide a similar experience the ChatGPT frontend; like ChatGPT, ChatCLI streams tokens from the model as they are generated.\n\n```console\n$ chatcli\nChatCLI v0.1.5 | [↩] to submit | [ALT/⌥] + [↩] for newline\n>>> Write 3 funny prompts for yourself.\n1. If you could only communicate through interpretive dance for the next 24 hours, how would you go about your day?\n\n2. You wake up in a world where everyone speaks in rhyme. How do you adapt to this unusual circumstance?\n\n3. You can only speak in questions for the rest of the day. How do you navigate conversations with friends, co-workers, and strangers?\n```\n\n## Installation\n\nTo install ChatCLI, use pip:\n\n```\npip install chatcli\n```\n\nYou\'ll need an OpenAI API key to use ChatCLI. You can get one [here](https://beta.openai.com/).\n\nChatCLI reads your key from the `OPENAI_API_KEY` environment variable, so you\'ll also need to set that.\n\n## Usage\n\n### CLI Usage\n\nTo use ChatCLI, simply run the `chatcli` command:\n\n```\nchatcli\n```\n\nThis will start a chat session with the default OpenAI model. You can type your messages and the AI will respond.\n\nYou can exit the chat at any time by typing "exit" into the prompt or pressing Ctrl+C.\n\n### Python Usage\n\nChatCLI can also be used as a Python library. Here\'s an example:\n\n```python\nimport chatcli\n# Create the chat generator\ngenerator = chatcli.ChatGenerator()\n\n# Send a message to the generator\nresponse = generator.send("Prove Riemann\'s Hypothesis.")\n\n# Print the response\nprint(response["message"]["content"])\n```\n\nThis will send a message to the API and then print the response stream as it is generated.\n\n## License\n\nChatCLI is licensed under the MIT license. See [LICENSE](LICENSE) for details.\n',
    'author': 'IsaacBreen',
    'author_email': 'mail@isaacbreen.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
