# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest


class TestReport(object):

    @pytest.fixture
    def testdir(self, testdir):
        testdir.makeconftest("""
            pytest_plugins = 'pytest_pspec.plugin'
        """)
        return testdir

    def test_should_print_a_green_passing_test(self, testdir):
        testdir.makepyfile("""
            def test_a_feature_is_working():
                assert True
        """)

        result = testdir.runpytest('--pspec')

        expected = '\033[92m ✓ a feature is working\033[0m'
        assert expected in result.stdout.str()

    def test_should_not_modify_nodeid_when_disabled_test(self, testdir):
        testdir.makepyfile("""
            def test_a_feature_is_working():
                assert True
        """)

        result = testdir.runpytest('-v')

        expected = 'test_should_not_modify_nodeid_when_disabled_test.py::test_a_feature_is_working'
        assert expected in result.stdout.str()

    def test_should_print_a_red_failing_test(self, testdir):
        testdir.makepyfile("""
            def test_a_failed_test_of_a_feature():
                assert False
        """)

        result = testdir.runpytest('--pspec')
        expected = '\033[91m ✗ a failed test of a feature\033[0m'

        assert expected in result.stdout.str()

    def test_should_print_a_yellow_skipped_test(self, testdir):
        testdir.makepyfile("""
            import pytest

            @pytest.mark.skip
            def test_a_skipped_test():
                pass
        """)

        result = testdir.runpytest('--pspec')
        expected = '\033[93m » a skipped test\033[0m'

        assert expected in result.stdout.str()

    def test_should_not_print_colors_when_disabled_by_parameter(self, testdir):
        testdir.makepyfile("""
            def test_a_feature_is_working():
                assert True
        """)
        result = testdir.runpytest('--color=no', '--pspec')

        assert '\033[92m' not in result.stdout.str()

    def test_should_output_plaintext_using_a_config_option(self, testdir):
        testdir.makeini("""
            [pytest]
            pspec_format=plaintext
        """)
        testdir.makepyfile("""
            def test_a_feature_is_working():
                assert True
        """)
        result = testdir.runpytest('--pspec')

        expected = '\033[92m [x] a feature is working\033[0m'
        assert expected in result.stdout.str()

    def test_should_print_the_test_class_name(self, testdir):
        testdir.makepyfile("""
            class TestFoo(object):
                def test_foo(self):
                    pass

            class TestBar(object):
                def test_bar(self):
                    pass
        """)
        result = testdir.runpytest('--pspec')

        lines = result.stdout.get_lines_after('Foo')
        assert '✓ foo' in lines[0]

        lines = result.stdout.get_lines_after('Bar')
        assert '✓ bar' in lines[0]

    def test_should_print_the_module_name_of_a_test_without_class(
        self,
        testdir
    ):
        testdir.makefile('.py', test_module_name="""
            def test_a_failed_test_of_a_feature():
                assert False
        """)

        result = testdir.runpytest('--pspec')
        result.stdout.fnmatch_lines(['module name'])

    def test_should_print_test_summary(self, testdir):
        testdir.makefile('.py', test_module_name="""
            def test_a_passing_test():
                assert True
        """)

        result = testdir.runpytest('--pspec')
        assert '1 passed' in result.stdout.str()

    def test_should_use_python_patterns_configuration(self, testdir):
        testdir.makeini("""
            [pytest]
            python_classes=Describe*
            python_files=*spec.py
            python_functions=it*
        """)
        testdir.makefile('.py', module_spec="""
            class DescribeTest(object):
                def it_runs(self):
                    pass
        """)

        result = testdir.runpytest('--pspec')

        lines = result.stdout.get_lines_after('Test')
        assert '✓ runs' in lines[0]

    def test_should_print_doc_string_if_present(self, testdir):
        testdir.makepyfile("""
            def test_a_feature_is_working():
                "test must return as header"
                assert True
        """)

        result = testdir.runpytest('--pspec')

        expected = '\033[92m ✓ must return as header\033[0m'
        assert expected in result.stdout.str()

    def test_should_print_func_name_if_doc_is_not_present(self, testdir):
        testdir.makepyfile("""
            def test_a_feature_is_working():
                assert True
        """)

        result = testdir.runpytest('--pspec')

        expected = '\033[92m ✓ a feature is working\033[0m'
        assert expected in result.stdout.str()

    def test_should_print_class_name_if_doc_is_present(self, testdir):
        testdir.makepyfile("""
            class TestBar(object):
                "This is PySpec Class"
                def test_a_feature_is_working(self):
                    assert True
        """)

        result = testdir.runpytest('--pspec')

        expected = 'This is PySpec Class'
        assert expected in result.stdout.str()

    def test_should_print_class_name_if_node_length_gt_two(self, testdir):
        "This is doc"

        testdir.makepyfile("""
            import unittest
            class TestBar(unittest.TestCase):
                "This is PySpec Class"
                def test_a_feature_is_working(self):
                    assert True
        """)

        result = testdir.runpytest('--pspec')

        expected = 'This is PySpec Class'
        assert expected in result.stdout.str()
