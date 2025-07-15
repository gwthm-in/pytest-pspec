#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Demo script to show the current parametrized test issue and the fix
"""
import tempfile
import subprocess
import os

def test_current_behavior():
    """Test the current behavior with parametrized tests"""
    test_content = '''
import pytest

@pytest.mark.parametrize("test_input, expected", [
    ("3 + 5", 8),
    ("2 + 4", 6),
    ("6 * 9", 54),
])
def test_math(test_input, expected):
    assert eval(test_input) == expected

@pytest.mark.parametrize("value", [1, 2, 3])
def test_simple(value):
    assert value > 0

@pytest.mark.parametrize("x, y", [(1, 2), (3, 4), (5, 6)])
def test_addition(x, y):
    assert x + y > 0

# Test with docstring should work fine
@pytest.mark.parametrize("a, b", [(1, 2), (3, 4)])
def test_with_docstring(a, b):
    """Testing {a} + {b} = {result}""".format(a=a, b=b, result=a+b)
    assert a + b > 0
'''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_content)
        temp_file = f.name

    try:
        # Run pytest with pspec
        result = subprocess.run([
            'python', '-m', 'pytest', temp_file, '--pspec'
        ], capture_output=True, text=True, cwd='/app')
        
        print('Current output:')
        print(result.stdout)
        return result.stdout
    finally:
        os.unlink(temp_file)

if __name__ == "__main__":
    test_current_behavior()