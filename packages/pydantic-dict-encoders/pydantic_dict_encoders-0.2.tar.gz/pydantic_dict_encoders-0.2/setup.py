# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_dict', 'pydantic_dict.mixins']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-dict-encoders',
    'version': '0.2',
    'description': 'Pydantic mixins for support custom encoding dict',
    'long_description': "# Pydantic Dict Encoders\n\nSimple wrapper of pydantic for support custom dict encoders like json encoders\n\n[![CI](https://github.com/i8enn/pydantic_dict_encoders/actions/workflows/testing.yml/badge.svg?branch=master)](https://github.com/i8enn/pydantic_dict_encoders/actions?query=branch%3Amaster+workflow%3Atesting)\n[![Coverage](https://codecov.io/gh/i8enn/pydantic_dict_encoders/branch/master/graph/badge.svg?token=TER6OGX2Z7)](https://codecov.io/gh/i8enn/pydantic_dict_encoders)\n[![pypi](https://img.shields.io/pypi/v/pydantic_dict_encoders.svg)](https://pypi.python.org/pypi/pydantic_dict_encoders)\n[![downloads](https://pepy.tech/badge/pydantic_dict_encoders/month)](https://pepy.tech/project/pydantic_dict_encoders)\n[![versions](https://img.shields.io/pypi/pyversions/pydantic_dict_encoders.svg)](https://github.com/i8enn/pydantic_dict_encoders)\n[![license](https://img.shields.io/github/license/i8enn/pydantic_dict_encoders.svg)](https://github.com/i8enn/pydantic_dict_encoders/blob/master/LICENSE)\n\n\nThis wrapper created for solve serialization problem in ariadne resolvers, where needed return dict only with simple objects.\nAfter research [some problems](https://github.com/pydantic/pydantic/issues/1409) and pydantic features, it was decided to make this wrapper more like a crutch for solve my problem.\n\nThis should be resolved in [Pydantic V2](https://github.com/pydantic/pydantic/discussions/4456), but it's not production ready yet.\nAnd even there is a [PR](https://github.com/pydantic/pydantic/pull/4978) that was made some time ago. But for now, it seemed to me sufficient to use this solution and perhaps it will be useful to someone else.\n\n*Thanks to @samuelcolvin for create and being active on pydantic and starting to solve problems before some people think about them! :)*\n\n> **IMPORTANT!** Remember: this is a crutch that you use at your own risk. It will most likely not be needed after some time, but if everything suits you - go for it ;)\n\n---\n\n## Usage\n\nThis wrapper has 2 possibilities:\n\n1. Define custom dict encoders that work the same as pydantic [`json_encoders`](https://docs.pydantic.dev/usage/exporting_models/#json_encoders) when calling `model.dict()`\n2. Encode each field value as if they were passed to pydantic json.\n\nTo use this just inherit your model from `PydanticDictEncodersMixin`:\n\n```python\nclass AnyModel(PydanticDictEncodersMixin, BaseModel):\n    any_field: str | None = None\n\n    class Config:\n        dict_encoders = {}\n        jsonify_dict_encode = False\n```\n\n> **WARNING!** Please, remember about python MRO: BaseModel MUST BE after mixin.\n\n---\n## Pros and cons\n\n### Pros:\n- Pretty simple and fast way to get the required behavior when exporting to a python dict\n\n### Cons:\n- In nested models that do not inherit from the mixin, serialization will break\n- Dirty decision\n",
    'author': 'Ivan Galin',
    'author_email': 'i.galin@devartsteam.ru',
    'maintainer': 'Ivan Galin',
    'maintainer_email': 'i.galin@devartsteam.ru',
    'url': 'https://github.com/i8enn/pydantic_dict_encoders',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
