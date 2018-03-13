Requests-Html-Macros
=======================================
.. image:: https://travis-ci.org/erinxocon/requests-html-macros.svg?branch=master
    :target: https://travis-ci.org/erinxocon/requests-html-macros
.. image:: https://img.shields.io/pypi/v/requests-html-macros.svg?maxAge=2592000
    :target: https://pypi.python.org/pypi/requests-html-macros/
.. image:: https://img.shields.io/pypi/l/requests-html-macros.svg?maxAge=2592000
    :target: https://opensource.org/licenses/MIT

**Requests-Html-Macros** is a little sugar on top of an already great html parseing library `Requests-Html <https://github.com/kennethreitz/requests-html>`_

This library aims to help make parsing the web a bit easier than it already is with Requests-Html!  Create macros that can be reused over different web sites/sessions!

Could you do this by hand with requests-html, yes probably pretty simply, but I only realized that like half way through developing this library and then was just like screw it let's push it out anyways!

Example
-------
.. code-block:: python

    from time import sleep

    from requests_html_macro import Macro
    from requests_html import HTMLSession

    # Create a standard requests-html session
    session = HTMLSession()
    response = session.get('http://python.org')

    # Create a macro with the response
    macro = Macro(response=response)

    # Create a macro that uses the parse library to search through the html
    @macro.search_pattern('Python is a {} language', first=True)
    def foo(data):
        print(data[0])

    # Creates a macro that uses a css selector
    @macro.css_selector('#about', first=True)
    def foo1(data):
        print(data.text)


    @macro.xpath('//a', first=True)
    def foo2(data):
        print(data)

    while True:
        macro.parse()
        sleep(30)
        macro.response = session.get('http://python.org')

To Install
----------

::

    $ pip install requests-html-macro

