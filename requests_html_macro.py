#coding=utf-8
from requests_html import HTMLResponse, _Find, _XPath
from typing import Text, List, Union, Mapping

import sys

# Sanity checking.
try:
    assert sys.version_info.major == 3
    assert sys.version_info.minor > 5
except AssertionError:
    raise RuntimeError('TPFD requires Python 3.6+!')


# Typing
_ParseResponse = Union[List, Mapping, _Find, _XPath]


class Rule:

    def __init__(self, rule: Text, func: callable, rule_type: Text, clean: bool = False, first: bool = False) -> None:
        self._rule = rule
        self._func = func
        self._rule_type = rule_type
        self._first = first
        self._clean = clean


    @property
    def rule(self) -> Text:
        return self._rule


    @property
    def function(self) -> callable:
        return self._func


    @property
    def rule_type(self) -> Text:
        return self._rule_type


    @property
    def first(self) -> bool:
        return self._first


    @property
    def clean(self) -> bool:
        return self._clean


class Macro:

    def __init__(self, response: HTMLResponse) -> None:
        self.debug = False
        self._rules = []
        self._response = response


    @property
    def rules(self) -> List[Rule]:
        return self._rules


    @property
    def response(self) -> HTMLResponse:
        return self._result


    @response.setter
    def response(self, response: HTMLResponse) -> None:
        self._response = response


    def search_pattern(self, template: Text, first: bool = False) -> callable:
        """
        Decorator for parse search pattern
        """
        def parse_decorator(func: callable) -> callable:
            r = Rule(rule=template, func=func, rule_type='search', first=first)
            self._rules.append(r)
            return func

        return parse_decorator


    def css_selector(self, selector: Text, first: bool = False, clean: bool = False) -> callable:
        """
        Decorator for css selector rules.
        """
        def find_decorator(func: callable) -> callable:
            r = Rule(rule=selector, func=func, rule_type='find', first=first, clean=clean)
            self._rules.append(r)
            return func

        return find_decorator


    def xpath(self, selector: str, first: bool = False, clean: bool = False) -> callable:
        """
        Decorator for xpath selector rules.
        """
        def xpath_decorator(func: callable) -> callable:
            r = Rule(rule=selector, func=func, rule_type='xpath', first=first, clean=clean)
            self._rules.append(r)
            return func

        return xpath_decorator


    def parse(self) -> _ParseResponse:

        for i in self._rules:

            if i.rule_type is 'search':
                if i.first:
                    r = self._response.html.search(i.rule)
                else:
                    r = self._response.html.search_all(i.rule)

                if r is not None:
                    i.function(r)

            elif i.rule_type is 'find':
                r = self._response.html.find(selector=i.rule, first=i.first, clean=i.clean)

                if r is not None:
                    i.function(r)

            elif i.rule_type is 'xpath':
                r = self._response.html.xpath(selector=i.rule, first=i.first, clean=i.clean)

                if r is not None:
                    i.function(r)
