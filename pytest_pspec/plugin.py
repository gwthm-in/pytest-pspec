# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest
from _pytest.terminal import TerminalReporter

from . import models, wrappers


def pytest_addoption(parser):
    group = parser.getgroup('terminal reporting', 'reporting', after='general')
    group.addoption(
        '--pspec', action='store_true', dest='pspec', default=False,
        help='Report test progress in pspec format'
    )
    parser.addini(
        'pspec_format',
        help='pspec report format (plaintext|utf8)',
        default='utf8'
    )


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if config.option.pspec:
        # Get the standard terminal reporter plugin and replace it with ours
        standard_reporter = config.pluginmanager.getplugin('terminalreporter')
        pspec_reporter = PspecTerminalReporter(standard_reporter.config)
        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(pspec_reporter, 'terminalreporter')


def _format_parametrized_test_name(function_name, callspec):
    """
    Format a parametrized test name to be more readable.
    
    Args:
        function_name: The original function name (e.g., 'test_math')
        callspec: The pytest callspec object containing parameters
        
    Returns:
        A formatted string like 'math with test input=3 + 5, expected=8'
    """
    # Remove 'test_' prefix and replace underscores with spaces
    clean_name = function_name.replace('test_', '').replace('_', ' ')
    
    # Format parameter values
    if callspec and hasattr(callspec, 'params'):
        param_strs = []
        for key, value in callspec.params.items():
            # Replace underscores with spaces in parameter names
            clean_key = key.replace('_', ' ')
            # Handle string values by adding quotes for clarity
            if isinstance(value, str):
                param_strs.append(f"{clean_key}='{value}'")
            else:
                param_strs.append(f"{clean_key}={value}")
        
        if param_strs:
            return f"{clean_name} with {', '.join(param_strs)}"
    
    return clean_name


def pytest_collection_modifyitems(config, items):
    if not config.option.pspec:
        return
    
    for item in items:
        node = item.obj
        parent = item.parent.obj
        node_parts = item.nodeid.split('::')
        
        # Check if this is a parametrized test
        if hasattr(item, "callspec") and item.callspec:
            # If there's a docstring, try to format it with parameters
            if node.__doc__:
                try:
                    node_str = node.__doc__.format(**item.callspec.params)
                except (KeyError, ValueError):
                    # If formatting fails, fall back to better parametrized format
                    node_str = _format_parametrized_test_name(node.__name__, item.callspec)
            else:
                # No docstring, use the improved parametrized format
                node_str = _format_parametrized_test_name(node.__name__, item.callspec)
        else:
            # Regular test (not parametrized)
            node_str = node.__doc__ or node_parts[-1]

        mode_str = node_parts[0]
        klas_str = ''
        node_parts_length = len(node_parts)

        if node_parts_length > 3:
            klas_str = parent.__doc__ or node_parts[-3]
        elif node_parts_length > 2:
            klas_str = parent.__doc__ or node_parts[-2]

        item._nodeid = '::'.join([mode_str, klas_str, node_str])


class PspecTerminalReporter(TerminalReporter):

    def __init__(self, config, file=None):
        TerminalReporter.__init__(self, config, file)
        self._last_header = None
        self._last_file = None
        self._tests_completed = 0
        self._total_tests = 0
        self.pattern_config = models.PatternConfig(
            files=self.config.getini('python_files'),
            functions=self.config.getini('python_functions'),
            classes=self.config.getini('python_classes')
        )
        self.result_wrappers = []

        if config.getini('pspec_format') != 'plaintext':
            self.result_wrappers.append(wrappers.UTF8Wrapper)

        if config.option.color != 'no':
            self.result_wrappers.append(wrappers.ColorWrapper)

    def pytest_collection_finish(self, session):
        """Called after collection is complete."""
        self._total_tests = len(session.items)
        # Call parent implementation if it exists
        if hasattr(super(), 'pytest_collection_finish'):
            super().pytest_collection_finish(session)

    def _register_stats(self, report):
        """
        This method is not created for this plugin, but it is needed in order
        to the reporter display the tests summary at the end.

        Originally from:
        https://github.com/pytest-dev/pytest/blob/47a2a77/_pytest/terminal.py#L198-L201
        """
        res = self.config.hook.pytest_report_teststatus(
                report=report,
                config=self.config)
        category = res[0]
        self.stats.setdefault(category, []).append(report)
        self._tests_ran = True

    def _get_progress_string(self):
        """Calculate and return progress percentage string."""
        if self._total_tests > 0:
            percentage = (self._tests_completed * 100) // self._total_tests
            return f'[{percentage:3d}%]'
        return ''

    def pytest_runtest_logreport(self, report):
        self._register_stats(report)

        if report.when != 'call' and not report.skipped:
            return

        self._tests_completed += 1

        # Update parent's progress tracking
        if hasattr(self, '_progress_nodeids_reported'):
            self._progress_nodeids_reported.add(report.nodeid)

        result = models.Result.create(report, self.pattern_config)

        for wrapper in self.result_wrappers:
            result = wrapper(result)

        # Get current file from nodeid
        current_file = report.nodeid.split('::')[0]

        # Show progress when switching to a new file
        if self._last_file is not None and current_file != self._last_file:
            progress = self._get_progress_string()
            if progress:
                self._tw.line(f'{" " * 90}{progress}')

        if result.header != self._last_header:
            self._last_header = result.header
            self._last_file = current_file
            self._tw.sep(' ')
            self._tw.line(result.header)

        try:
            self._tw.line(unicode(result))
        except NameError:
            self._tw.line(str(result))

