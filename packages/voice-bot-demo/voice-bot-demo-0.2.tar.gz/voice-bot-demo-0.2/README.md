# voice-bot-demo

[![PyPI](https://img.shields.io/pypi/v/voice-bot-demo.svg)](https://pypi.org/project/voice-bot-demo/)
[![Changelog](https://img.shields.io/github/v/release/helloworld/voice-bot-demo?include_prereleases&label=changelog)](https://github.com/helloworld/voice-bot-demo/releases)
[![Tests](https://github.com/helloworld/voice-bot-demo/workflows/Test/badge.svg)](https://github.com/helloworld/voice-bot-demo/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/helloworld/voice-bot-demo/blob/master/LICENSE)

AI conversational bot

## Installation

Install this tool using `pip`:

    pip install voice-bot-demo

## Usage

For help, run:

    voice-bot-demo --help

You can also use:

    python -m voice_bot_demo --help

For now, only the [Assembly AI](https://www.assemblyai.com/) speech-to-text model works fully. To run:

```
export ASSEMBLYAI_API_SECRET=YOUR_KEY_HERE
voice-bot-demo start --speech-text-model assembly
```

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd voice-bot-demo
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
