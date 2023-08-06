# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kor', 'kor.experimental']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.110,<0.0.111', 'openai>=0.27,<0.28']

setup_kwargs = {
    'name': 'kor',
    'version': '0.3.0',
    'description': 'Extract information with LLMs from text',
    'long_description': '**⚠ WARNING: Prototype with unstable API. 🚧**  \n\n[![test](https://github.com/eyurtsev/kor/actions/workflows/test.yml/badge.svg?branch=main&event=push)](https://github.com/eyurtsev/kor/actions/workflows/test.yml)\n\n# Kor\n\nThis is a half-baked prototype that "helps" you extract structured data from text using LLMs 🧩.\n\nSpecify the schema of what should be extracted and provide some examples.\n\nKor will generate a prompt, send it to the specified LLM and parse out the\noutput. You might even get results back.\n\n\n```python\n\nfrom kor.extraction import Extractor\nfrom kor.nodes import Object, Text\nfrom langchain.chat_models import ChatOpenAI\n\nllm = ChatOpenAI(model_name="gpt-3.5-turbo")\nmodel = Extractor(llm)\n\nschema = Object(\n    id="player",\n    description=(\n        "User is controling a music player to select songs, pause or start them or play"\n        " music by a particular artist."\n    ),\n    attributes=[\n        Text(id="song", description="User wants to play this song", examples=[]),\n        Text(id="album", description="User wants to play this album", examples=[]),\n        Text(\n            id="artist",\n            description="Music by the given artist",\n            examples=[("Songs by paul simon", "paul simon")],\n        ),\n        Text(\n            id="action",\n            description="Action to take one of: `play`, `stop`, `next`, `previous`.",\n            examples=[\n                ("Please stop the music", "stop"),\n                ("play something", "play"),\n                ("next song", "next"),\n            ],\n        ),\n    ],\n)\n\nmodel("can you play all the songs from paul simon and led zepplin", schema)\n```\n\n```python\n{\'player\': [{\'artist\': [\'paul simon\', \'led zepplin\']}]}\n```\n\nSee [documentation](https://eyurtsev.github.io/kor/).\n\n## Compatibility\n\n`Kor` is tested against python 3.8, 3.9, 3.10, 3.11.\n\n## Installaton \n\n```sh\npip install kor\n```\n\n## 💡 Ideas\n\nIdeas of some things that could be done with Kor.\n\n* Extract data from text: Define what information should be extracted from a segment\n* Convert an HTML form into a Kor form and allow the user to fill it out using natural language. (Convert HTML forms -> API? Or not.)\n* Add some skills to an AI assistant\n\n## 🚧 Prototype\n\nThis a prototype and the API is not expected to be stable as it hasn\'t been\ntested against real world examples.\n\n##  ✨ Where does Kor excel?  🌟 \n\n* Making mistakes! Plenty of them. Quality varies with the underlying language model, the quality of the prompt, and the number of bugs in the adapter code.\n* Slow! It uses large prompts with examples, and works best with the larger slower LLMs.\n* Crashing for long enough pieces of text! Context length window could become\n  limiting when working with large forms or long text inputs.\n* Incorrectly grouping results (see documentation section on objects).\n\n## Limtations\n\nThis package has no limitations; however, look at the section directly above as\nwell as at compatibility.\n\n## Potential Changes\n\n* Adding validators\n* Built-in components to quickly assemble schema with examples\n* Add routing layer to select appropriate extraction schema for a use case when\n  many schema exist\n\n## 🎶 Why the name?\n\nFast to type and sufficiently unique.\n\n## Contributing\n\nIf you have any ideas or feature requests, please open an issue and share!\n\nSee [CONTRIBUTING.md](https://github.com/eyurtsev/kor/blob/main/CONTRIBUTING.md) for more information.\n\n## Other packages\n\nProbabilistically speaking this package is unlikely to work for your use case.\n\nSo here are some great alternatives:\n\n* [Promptify](https://github.com/promptslab/Promptify)\n* [MiniChain](https://srush.github.io/MiniChain/examples/stats/)\n',
    'author': 'Eugene Yurtsev',
    'author_email': 'eyurtsev@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.github.com/eyurtsev/kor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0.0',
}


setup(**setup_kwargs)
