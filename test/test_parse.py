import os

import pytest
from requests_file import FileAdapter
from requests_html import HTMLSession

from requests_html_macro import Macro

session = HTMLSession()
session.mount('file://', FileAdapter())


def get():
    path = os.path.sep.join((os.path.dirname(os.path.abspath(__file__)), 'python.html'))
    url = 'file://{}'.format(path)
    response = session.get(url)
    return Macro(response=response)


@pytest.mark.ok
def test_css_selector():
    macro = get()

    @macro.css_selector('#about', first=True)
    def foo(data):
        for menu_item in (
            'About', 'Applications', 'Quotes', 'Getting Started', 'Help',
            'Python Brochure'
        ):
            assert menu_item in data.text.split('\n')
            assert menu_item in data.full_text.split('\n')

    macro.parse()


@pytest.mark.ok
def test_search_template():
    macro = get()

    @macro.search_pattern('Python is a {} language', first=True)
    def foo(data):
        assert data[0] == 'programming'

    macro.parse()


@pytest.mark.ok
def test_xpath():
    macro = get()

    @macro.xpath('/html', first=True)
    def foo(data):
        assert 'no-js' in data.attrs['class']

    macro.parse()

if __name__ == '__main__':
    pytest.main()
