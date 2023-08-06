# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vocode',
 'vocode.input_device',
 'vocode.models',
 'vocode.output_device',
 'vocode.telephony',
 'vocode.user_implemented_agent']

package_data = \
{'': ['*']}

install_requires = \
['anyio==3.6.2',
 'certifi==2022.12.7',
 'cffi==1.15.1',
 'charset-normalizer==3.0.1',
 'click==8.1.3',
 'decorator==5.1.1',
 'fastapi==0.92.0',
 'h11==0.14.0',
 'idna==3.4',
 'numpy==1.24.2',
 'ply==3.11',
 'pycparser==2.21',
 'pydantic==1.10.5',
 'python-dotenv==0.21.1',
 'requests==2.28.2',
 'six==1.16.0',
 'sniffio==1.3.0',
 'sounddevice==0.4.6',
 'starlette==0.25.0',
 'typing-extensions==4.5.0',
 'urllib3==1.26.14',
 'uvicorn==0.20.0',
 'websockets==10.4']

setup_kwargs = {
    'name': 'vocode',
    'version': '0.1.36',
    'description': 'The all-in-one voice SDK',
    'long_description': '# vocode Python SDK\n\n```\npip install vocode\n```\n\n```python\nimport asyncio\nimport signal\n\nfrom vocode.conversation import Conversation\nfrom vocode.helpers import create_microphone_input_and_speaker_output\nfrom vocode.models.transcriber import DeepgramTranscriberConfig\nfrom vocode.models.agent import LLMAgentConfig\nfrom vocode.models.synthesizer import AzureSynthesizerConfig\n\nif __name__ == "__main__":\n    microphone_input, speaker_output = create_microphone_input_and_speaker_output(use_first_available_device=True)\n\n    conversation = Conversation(\n        input_device=microphone_input,\n        output_device=speaker_output,\n        transcriber_config=DeepgramTranscriberConfig.from_input_device(microphone_input),\n        agent_config=LLMAgentConfig(prompt_preamble="The AI is having a pleasant conversation about life."),\n        synthesizer_config=AzureSynthesizerConfig.from_output_device(speaker_output)\n    )\n    signal.signal(signal.SIGINT, lambda _0, _1: conversation.deactivate())\n    asyncio.run(conversation.start())\n```\n',
    'author': 'Ajay Raj',
    'author_email': 'ajay@vocode.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
