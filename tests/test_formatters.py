# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from pytest_pspec import formatters


class TestFormatTitle(object):

    @pytest.fixture
    def patterns(self):
        return ['test*']

    def test_should_replace_underscores_with_spaces(self, patterns):
        assert formatters.format_title('a_test_name', patterns) == (
            'a test name'
        )

    def test_should_remove_test_pattern(self, patterns):
        assert formatters.format_title('test_a_thing', patterns) == 'a thing'
        assert formatters.format_title('a_thing_test', patterns) == (
            'a thing test'
        )


class TestFormatClassName(object):

    @pytest.fixture
    def patterns(self):
        return ['Test*']

    def test_should_add_spaces_before_upercased_letters(self, patterns):
        formatted = formatters.format_class_name('AThingBuilder', patterns)
        assert formatted == 'A Thing Builder'

    def test_should_remove_test_pattern(self, patterns):
        assert formatters.format_class_name('TestAThing', patterns) == (
            'A Thing'
        )
        assert formatters.format_class_name('AThingTest', patterns) == (
            'A Thing Test'
        )

    @pytest.mark.parametrize('class_name,expected', (
        ('SimpleHTTPServer', 'Simple HTTP Server'),
        ('MyAPI', 'My API'),
    ))
    def test_should_not_split_letters_in_an_abbreviation(
        self,
        class_name,
        expected,
        patterns
    ):
        formatted = formatters.format_class_name(class_name, patterns)
        assert formatted == expected


class TestFormatModuleName(object):

    @pytest.fixture
    def patterns(self):
        return ['test*.py']

    def test_should_remove_py_file_pattern(self, patterns):
        assert formatters.format_module_name('pymodule.py', patterns) == (
            'pymodule'
        )

    def test_should_replace_underscores_with_spaces(self, patterns):
        assert formatters.format_module_name('a_test_name', patterns) == (
            'a test name'
        )

    def test_should_remove_test_pattern(self, patterns):
        assert formatters.format_module_name('test_a_thing.py', patterns) == (
            'a thing'
        )
        assert formatters.format_module_name('a_test.py', patterns) == 'a test'

    def test_should_remove_folders_from_the_name(self, patterns):
        formatted = formatters.format_module_name(
            'tests/sub/test_module.py',
            patterns
        )

        assert formatted == 'module'

    def test_should_remove_infix_glob_patterns(self):
        formatted = formatters.format_module_name(
            'test_module.py',
            ['test_*.py']
        )

        assert formatted == 'module'
