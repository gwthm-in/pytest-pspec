# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re


def format_title(title, patterns):
    return _remove_patterns(title, patterns).replace('_', ' ').strip()


def format_class_name(class_name, patterns):
    formatted = ''

    class_name = _remove_patterns(class_name, patterns)
    if ' ' not in class_name:
        for index, letter in enumerate(class_name):
            if letter.isupper() and \
                    _has_lower_letter_besides(index, class_name):
                formatted += ' '

            formatted += letter
    else:
        formatted = class_name

    return formatted.strip()


def format_module_name(module_name, patterns):
    return format_title(module_name.split('/')[-1], patterns)


def _remove_patterns(statement, patterns):
    for glob_pattern in patterns:
        pattern = glob_pattern.replace('*', '')

        if glob_pattern.startswith('*'):
            pattern = '{0}$'.format(pattern)
            statement = re.sub(pattern, '', statement)

        elif glob_pattern.endswith('*'):
            pattern = '^{0}'.format(pattern)
            statement = re.sub(pattern, '', statement)

        elif '*' in glob_pattern:
            infix_patterns = glob_pattern.split('*', 2)
            infix_patterns[0] = '{}*'.format(infix_patterns[0])
            infix_patterns[1] = '*{}'.format(infix_patterns[1])
            statement = _remove_patterns(statement, infix_patterns)

        else:
            pattern = '^{0}'.format(pattern)
            statement = re.sub(pattern, '', statement)

    return statement


def _has_lower_letter_besides(index, string):
    letter_before = string[index - 1] if index > 0 else ''
    letter_after = string[index + 1] if index < len(string) - 1 else ''

    return letter_before.islower() or letter_after.islower()
