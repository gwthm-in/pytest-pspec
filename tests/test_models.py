# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

from pytest_pspec import formatters
from pytest_pspec.models import Node, PatternConfig, Result


@pytest.fixture
def node():
    return Node(title='title', class_name='class_name', module_name='module')


class TestNode(object):

    @pytest.fixture
    def pattern_config(self):
        return PatternConfig(
            files=['test_*.py'],
            functions=['test*'],
            classes=['Test*']
        )

    def test_parse_should_return_a_node_instance(self, pattern_config):
        nodeid = 'tests/test_module.py::test_title'
        node = Node.parse(nodeid, pattern_config)

        assert isinstance(node, Node)

    def test_parse_should_parse_node_id_attributes(self, pattern_config):
        nodeid = 'tests/test_module.py::test_title'
        node = Node.parse(nodeid, pattern_config)

        assert node.title == formatters.format_title('test_title',
                                                     pattern_config.functions)
        assert node.module_name == (
            formatters.format_module_name('tests/test_module.py',
                                          pattern_config.files)
        )

    @pytest.mark.parametrize('nodeid,class_name', (
        ('tests/test_module.py::test_title', None),
        (
            'tests/test_module.py::TestClassName::()::test_title',
            formatters.format_class_name('TestClassName', ['Test*'])
        )
    ))
    def test_parse_with_class_name(self, pattern_config, nodeid, class_name):
        node = Node.parse(nodeid, pattern_config)

        assert node.class_name == class_name

    def test_repr_should_return_a_string_representation_of_itself(self, node):
        from_repr = eval(repr(node))

        assert from_repr.title == node.title
        assert from_repr.class_name == node.class_name
        assert from_repr.module_name == node.module_name


class TestResult(object):

    @pytest.fixture
    def result(self, node):
        return Result('passed', node)

    def test_repr_should_return_a_string_representation_of_itself(
        self,
        node,
        result
    ):
        from_repr = eval(repr(result))

        assert from_repr.outcome == result.outcome
        assert isinstance(from_repr.node, Node)
