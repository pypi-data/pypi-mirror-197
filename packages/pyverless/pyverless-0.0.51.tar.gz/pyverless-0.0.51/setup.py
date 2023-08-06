# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyverless',
 'pyverless.api_gateway_handler',
 'pyverless.config',
 'pyverless.events_handler',
 'pyverless.serialization',
 'pyverless.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT<2.0.0',
 'PyYAML>=5.1',
 'aws-lambda-powertools==1.25.7',
 'python-json-logger==2.0.2',
 'sentry-sdk>=0.5.1']

setup_kwargs = {
    'name': 'pyverless',
    'version': '0.0.51',
    'description': 'A mini-framework providing tools to help you make complex APIs with serverless',
    'long_description': "[![Build Status](https://travis-ci.org/QuantumBA/pyverless.svg?branch=master)](https://travis-ci.org/QuantumBA/pyverless)\n[![PyPI pyversions](https://img.shields.io/pypi/pyversions/pyverless.svg)](https://pypi.python.org/pypi/pyverless/)\n[![PyPI license](https://img.shields.io/pypi/l/pyverless.svg)](https://pypi.python.org/pypi/pyverless/)\n[![PyPI status](https://img.shields.io/pypi/status/pyverless.svg)](https://pypi.python.org/pypi/pyverless/)\n# Pyverless\n\nDeveloping complex APIs within AWS lambdas can be somewhat of a messy task. Lambdas are independent functions that have to work together in order to create a full-blown app, like atoms to a complex organism.\n\nIn order to define the infrastructure you may use a framework like [Serverless](https://serverless.com/), but you may find yourself copying and pasting blobs of code within your handler functions, namely for authentication, data validation, error handling and response creation to name a few.\n\n**Enter Pyverless**\n\nPyverless is a mini-framework with a bunch of utilities that aims to help you create APIs using AWS Lambdas fast and in a consistent way. Pyverless provides the following.\n\n- Class-Based Handlers\n- Serializers\n- Authentication handling\n- JWT and cryptography\n- Exceptions\n- Configuration\n- Warmup handling\n\nBring more consistency and development speed to your lambda-based APIs!\n\n## Class-Based Handlers\n\nClass based handlers (CBH) use the approach of Django's Class-Based Views to provide code reuse, consistency and generally abstract simple and common tasks. The aim of class-based handlers is to suit a wide range of applications by providing generic Handler classes and mixins.\n\nWithin AWS Lambda, a handler is a function that takes an event and a context and returns a response.\n\nGeneric CBH are based off the following base handler\n\n### BaseHandler\n\nThis class provides the `as_handler()` method that returns a handler function (taking `event` and `context` as arguments).\n\nUsage:\n\n```python\nclass MyHandler(BaseHandler):\n    pass\n\n_myHandler = MyHandler.as_handler()\n```\n\nThere is a set of generic CBHs to handle basic CRUD operations within an API:\n\n### CreateHandler\nHandler that reads the request body and creates the object with each (key, value) pair as a parameter for the constructor.\n\nThe `model` attribute must be set on the handler and the `create_object` method can be overwritten.\n\nUsage:\n\n```python\nclass UserCreateHandler(CreateHandler):\n\n    model = MyUserClass # MyUserClass(k1=v1, k2=v2, ...) for each k,v on body\n    required_body_keys = ['email', 'password']\n```\n\n### RetrieveHandler\nHandler that returns a serialized Object.\n\nThe `model` attribute must be set and `id` must be present on the pathParameters.\n\nThe user must overwrite either the `serializer` attribute or the `serialize` method.\n\nUsage:\n\n```python\nclass UserRetrieveHandler(RetrieveHandler):\n\n    model = MyUserClass\n    serializer = serialize_user\n```\n\n### UpdateHandler\nHandler that sets self.object and for each (key, value) pair of the body\nsets self.object.key = value.\n\nThe `model` attribute must be set and `id` must be present on the pathParameters.\n\nReturns the serialized node and sets the HTTP status code to 200\n\nUsage:\n\n```python\nclass UserUpdateHandler(UpdateHandler):\n    model = MyUserClass\n    required_body_keys = ['title', 'body']\n    serializer = serialize_user\n```\n\n\n### DeleteHandler\nHandler that sets self.object, calls its delete() method and sets the HTTP status code to 204.\n\nThe `model` attribute must be set and `id` must be present on the pathParameters.\n\nThe user can also overwrite the `get_queryset` method to limit the search.\n\nUsage:\n\n```python\nclass UserDeleteHandler(DeleteHandler):\n    model = MyUserClass\n```\n### ListHandler\nHandler that returns a list of serialized nodes and sets the HTTP status code to 200.\n\nThe `model` attribute must be set and the user must overwrite either the `serializer` attribute\nor the `serialize` method.\n\n```python\nclass UserListHandler(ListHandler):\n    model = MyUserClass\n    serializer = user_serializer\n    \n    def get_queryset(self):\n        return only_some_users\n```\n\n## Mixins\nThere are also a set of **mixins** available:\n\n### RequestBodyMixin\n\nThis mixin provides the `get_body()` method which is in charge of gathering the request body dictionary. Define `required_body_keys` and `optinal_body_keys` as follows. Within the handler, you can access the body via `self.body` or by calling `get_body()`\n\n```python\nclass MyHandler(RequestBodyMixin, BaseHandler):\n    required_body_keys = ['name', 'email']\n    optinal_body_keys = ['phone']\n\n_myHandler = MyHandler.as_handler()\n```\n\n### AuthorizationMixin\n\nThis mixin provides the `get_user()` method in charge of getting the user out of an authenticated API call.\nWithin the handler, you can access the body via `self.user` or by calling `get_user()`. The user will be a object\nof the class specified on pyverless settings as `USER_MODEL`.\n\n### RequestBodyMixin\n\nThis mixin provides the `get_object()` method in charge of gathering a particular object,\nyou can access the object via `self.object`.\nThe `id` of the object will be taken from the pathParameters and\nthe user must set the `model` attribute on the handler.\n\n### ListMixin\n\nThis mixin provides the `get_queryset()` method in charge of getting a list of objects,\nyou can access the list via `self.queryset`. The user must set the `model` attribute\nand either the `serializer` attribute or `serialize()` method on the handler.\n\n### S3FileMixin\n\nThis mixin provides the `get_file()` and `get_message_part()` methods in charge of\nreading an event from aws S3, you can access the file via `self.file`.\n\nThe file will be a `dict()` with the following keys: bucket, owner, file_name, size.\n\n***Warning: Only tested with objectCreated!!!!***\n\n### SQSMessagesMixin\n\nThis mixin provides the `get_messages()` method in charge of reading an SQS event from aws.\nYou can access the list of messages via `self.messages`.\n\nEach message will be a `dict()` with the following keys: attributes, text_message, queue_source, region.\n\n## Serializers\n\n**TODO**\n",
    'author': 'rperez',
    'author_email': 'rperez@op2aim.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/QuantumBA/pyverless',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
