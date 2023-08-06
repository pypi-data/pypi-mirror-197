quickGPT
========

|PyPI - Downloads| |PyPI|

**quickGPT** is a lightweight and easy-to-use Python library that
provides a simplified interface for working with the new API interface
of OpenAI’s ChatGPT. With quickGPT, you can easily generate natural
language responses to prompts and questions using state-of-the-art
language models trained by OpenAI.

For the record, this README.md was (mostly) generated with ChatGPT.
That’s why it’s a little braggy.

Installation
------------

You can install **quickGPT** using pip:

.. code:: sh

   pip install quickgpt

Usage
-----

To use quickgpt, you’ll need an OpenAI API key, which you can obtain
from the OpenAI website. Once you have your API key, you can specify
your API key using an environment variable:

::

   export OPENAI_API_KEY="YOUR_API_KEY_HERE"

or by passing it to the ``api_key`` parameter of ``QuickGPT``:

::

   chat = QuickGPT(api_key="YOUR_API_KEY_HERE")

See the examples for more information on how it works. Or, you can use
the ``quickgpt`` tool for an interactive ChatGPT session in your command
line. Make sure ``~/.local/bin/`` is in your ``$PATH``.

Documentation
-------------

There’s no documentation yet. Stay tuned.

Contributing
------------

If you find a bug or have an idea for a new feature, please submit an
issue on the GitHub repository. Pull requests are also welcome!

License
-------

This project is licensed under the MIT License.

.. |PyPI - Downloads| image:: https://img.shields.io/pypi/dm/quickgpt?style=for-the-badge
   :target: https://pypi.org/project/quickgpt/
.. |PyPI| image:: https://img.shields.io/pypi/v/quickgpt?style=for-the-badge
   :target: https://pypi.org/project/quickgpt/
