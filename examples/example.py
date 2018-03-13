from time import sleep

from requests_html_macro import Macro
from requests_html import HTMLSession

session = HTMLSession()
response = session.get('http://python.org')

macro = Macro(response=response)

@macro.search_pattern('Python is a {} language', first=True)
def foo(data):
    print(data[0])


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