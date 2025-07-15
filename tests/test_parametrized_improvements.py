# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from _pytest.config import ExitCode

from pytest_pspec.plugin import _format_parametrized_test_name


class TestParametrizedTestFormatting(object):
    """Tests for the improved parametrized test formatting"""

    @pytest.fixture
    def testdir(self, testdir):
        testdir.makeconftest("""
            pytest_plugins = 'pytest_pspec.plugin'
        """)
        return testdir

    def test_should_format_parametrized_test_without_docstring(self, testdir):
        """Test that parametrized tests without docstrings are formatted nicely"""
        testdir.makepyfile("""
            import pytest

            @pytest.mark.parametrize("value", [1, 2, 3])
            def test_simple(value):
                assert value > 0
        """)

        result = testdir.runpytest('--pspec')

        assert 'simple with value=1' in result.stdout.str()
        assert 'simple with value=2' in result.stdout.str()
        assert 'simple with value=3' in result.stdout.str()

    def test_should_format_multiple_parameters(self, testdir):
        """Test formatting of multiple parameters"""
        testdir.makepyfile("""
            import pytest

            @pytest.mark.parametrize("x, y", [(1, 2), (3, 4)])
            def test_addition(x, y):
                assert x + y > 0
        """)

        result = testdir.runpytest('--pspec')

        assert 'addition with x=1, y=2' in result.stdout.str()
        assert 'addition with x=3, y=4' in result.stdout.str()

    def test_should_format_string_parameters_with_quotes(self, testdir):
        """Test that string parameters are formatted with quotes"""
        testdir.makepyfile("""
            import pytest

            @pytest.mark.parametrize("test_input, expected", [
                ("3 + 5", 8),
                ("2 + 4", 6),
            ])
            def test_math(test_input, expected):
                assert eval(test_input) == expected
        """)

        result = testdir.runpytest('--pspec')

        assert "math with test input='3 + 5', expected=8" in result.stdout.str()
        assert "math with test input='2 + 4', expected=6" in result.stdout.str()

    def test_should_still_use_docstring_when_available(self, testdir):
        """Test that docstrings still work and take precedence"""
        testdir.makepyfile("""
            import pytest

            @pytest.mark.parametrize("value", [1, 2])
            def test_with_docstring(value):
                '''Testing value {value} is positive'''
                assert value > 0
        """)

        result = testdir.runpytest('--pspec')

        assert 'Testing value 1 is positive' in result.stdout.str()
        assert 'Testing value 2 is positive' in result.stdout.str()

    def test_should_handle_docstring_formatting_errors(self, testdir):
        """Test that docstring formatting errors fall back to parametrized format"""
        testdir.makepyfile("""
            import pytest

            @pytest.mark.parametrize("value", [1, 2])
            def test_with_bad_docstring(value):
                '''Testing {missing_key} is positive'''
                assert value > 0
        """)

        result = testdir.runpytest('--pspec')

        assert 'with bad docstring with value=1' in result.stdout.str()
        assert 'with bad docstring with value=2' in result.stdout.str()


class TestFormatParametrizedTestNameFunction(object):
    """Tests for the _format_parametrized_test_name helper function"""

    def test_should_remove_test_prefix(self):
        """Test that 'test_' prefix is removed"""
        class MockCallspec:
            params = {'value': 1}
        
        result = _format_parametrized_test_name('test_simple', MockCallspec())
        assert result == 'simple with value=1'

    def test_should_replace_underscores_with_spaces(self):
        """Test that underscores are replaced with spaces"""
        class MockCallspec:
            params = {'value': 1}
        
        result = _format_parametrized_test_name('test_my_complex_test', MockCallspec())
        assert result == 'my complex test with value=1'

    def test_should_handle_string_values_with_quotes(self):
        """Test that string values get quotes"""
        class MockCallspec:
            params = {'test_input': '3 + 5', 'expected': 8}
        
        result = _format_parametrized_test_name('test_math', MockCallspec())
        assert result == "math with test input='3 + 5', expected=8"

    def test_should_handle_no_parameters(self):
        """Test handling when there are no parameters"""
        class MockCallspec:
            params = {}
        
        result = _format_parametrized_test_name('test_simple', MockCallspec())
        assert result == 'simple'

    def test_should_handle_none_callspec(self):
        """Test handling when callspec is None"""
        result = _format_parametrized_test_name('test_simple', None)
        assert result == 'simple'