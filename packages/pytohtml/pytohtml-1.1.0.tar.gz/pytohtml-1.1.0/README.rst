Writing XML with Pythonic code
==============================

.. image:: https://img.shields.io/github/license/mashape/apistatus.svg
   :target: http://opensource.org/licenses/MIT
.. image:: https://badge.fury.io/py/pytohtml.svg
    :target: https://badge.fury.io/py/pytohtml

Installation
------------

.. code:: bash

    $ pip install py-to-html

Example
-------

.. image:: https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/597237/436215da-f815-4473-687e-7fc21b04bab3.gif

`QR-Code Generator Source Code <https://github.com/am230/py2html/blob/master/examples/qr%20generator.py>`_.

.. image:: https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/597237/40173212-8f2e-0e4e-c924-3140d6ff1722.gif

`Simple Chat Source Code <https://github.com/am230/py2html/blob/master/examples/form.py>`_.

Syntax
------

.. code:: python

    from py2html.elements import html, head, body, meta, title, h1


    print(
        html(lang="en")[
            head[
                meta(charset="UTF-8"),
                meta({"http-equiv": "X-UA-Compatible", "content": "IE=edge"}),
                meta(name="viewport", content="width=device-width, initial-scale=1.0"),
                title["py2html"]
            ],
            body[
                h1[
                    "Hello, Py2HTML!"
                ]
            ]
        ].render()
    )
    

\*formatted output

.. code:: html

    <html lang="en">
    <head>
    <meta charset="UTF-8"></meta>
    <meta http-equiv="X-UA-Compatible" content="IE=edge"></meta>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"></meta>
    <title>py2html</title>
    </head>
    <body>
    <h1>Hello, Py2HTML!</h1>
    </body>
    </html>

