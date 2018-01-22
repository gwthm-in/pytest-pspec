# -*- coding: utf-8 -*-
from __future__ import unicode_literals


class Wrapper(object):

    def __init__(self, wrapped):
        self.wrapped = wrapped

    def __getattr__(self, name):
        return getattr(self.wrapped, name)


class ColorWrapper(Wrapper):

    _COLOR_BY_OUTCOME = {
        'passed': '\033[92m',
        'failed': '\033[91m',
        'skipped': '\033[93m',
    }
    _color_reset = '\033[0m'

    def __str__(self):
        color = self._COLOR_BY_OUTCOME.get(self.wrapped.outcome, '')
        reset = self._color_reset if color else ''

        return '{color}{result}{reset}'.format(
            color=color,
            result=self.wrapped,
            reset=reset
        )


class UTF8Wrapper(Wrapper):

    _CHARACTER_BY_OUTCOME = {
        'passed': '✓',
        'failed': '✗',
        'skipped': '»',
    }

    _default_character = '»'

    def __str__(self):
        outcome = self._CHARACTER_BY_OUTCOME.get(
            self.wrapped.outcome,
            self._default_character
        )
        return ' {outcome} {node}'.format(
            outcome=outcome,
            node=self.wrapped.node
        )
