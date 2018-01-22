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
        help='TestDox report format (plaintext|utf8)',
        default='utf8'
    )


@pytest.mark.trylast
def pytest_configure(config):
    if config.option.pspec:
        # Get the standard terminal reporter plugin and replace it with ours
        standard_reporter = config.pluginmanager.getplugin('terminalreporter')
        pspec_reporter = TestdoxTerminalReporter(standard_reporter.config)
        config.pluginmanager.unregister(standard_reporter)
        config.pluginmanager.register(pspec_reporter, 'terminalreporter')


def pytest_collection_modifyitems(config, items):
    for item in items:
        node = item.obj
        parent = item.parent.obj
        nodeid_parts = item.nodeid.split('::')
        if node.__doc__:
            nodeid_parts[-1] = node.__doc__.strip()
        if parent.__doc__:
            nodeid_parts[-2] = parent.__doc__.strip()
        item._nodeid = '::'.join(nodeid_parts)


class TestdoxTerminalReporter(TerminalReporter):

    def __init__(self, config, file=None):
        TerminalReporter.__init__(self, config, file)
        self._last_header = None
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

    def _register_stats(self, report):
        """
        This method is not created for this plugin, but it is needed in order
        to the reporter display the tests summary at the end.

        Originally from:
        https://github.com/pytest-dev/pytest/blob/47a2a77/_pytest/terminal.py#L198-L201
        """
        res = self.config.hook.pytest_report_teststatus(report=report)
        category = res[0]
        self.stats.setdefault(category, []).append(report)
        self._tests_ran = True

    def pytest_runtest_logreport(self, report):
        self._register_stats(report)

        if report.when != 'call' and not report.skipped:
            return

        result = models.Result.create(report, self.pattern_config)

        for wrapper in self.result_wrappers:
            result = wrapper(result)

        if result.header != self._last_header:
            self._last_header = result.header
            self._tw.sep(' ')
            self._tw.line(result.header)

        try:
            self._tw.line(unicode(result))
        except NameError:
            self._tw.line(str(result))
