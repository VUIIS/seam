#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test utility functions
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from seam.util import get_tmp_filename, wrap_with_xvfb, total, STRING_TYPE, PY2

def test_default_tmp_filename():
    cmp_filename = get_tmp_filename()
    assert len(cmp_filename) == 41 # /tmp/ (5) + 32 + .out (4)
    assert cmp_filename.endswith('.out')
    assert cmp_filename.startswith('/tmp/')

def test_tmp_filename_options():
    base = '/path/to/'
    ext = 'myext'
    length = 10
    computed_length = length + len(ext) + len(base) + 1 # period of filename
    cmp_filename = get_tmp_filename(ext=ext,
        basename=base, fname_length=length)
    assert len(cmp_filename) == computed_length
    assert cmp_filename.startswith(base)
    assert cmp_filename.endswith(ext)

def test_default_wrap_with_xvfb():
    cmd = 'ls -l'
    comp_wrapper = wrap_with_xvfb(cmd)
    assert comp_wrapper.startswith('xvfb-run')
    assert comp_wrapper.endswith(cmd)
    required_flags = ['-f', '-e', '-a', '--wait',
        '--server-args="-screen 0, 1600x1200x24"']
    for flag in required_flags:
        assert flag in comp_wrapper

def test_wrap_with_xvfb_options():
    server_args = '-screen 0, 800x600x16'
    wait = 10
    cmp_wrapper = wrap_with_xvfb('ls -l', wait=wait, server_args=server_args)
    assert server_args in cmp_wrapper
    assert '--wait={:d}'.format(wait) in cmp_wrapper

def test_total():
    assert len(total) == 62

def test_string_type():
    import sys
    if sys.version_info[0] == 2:
        assert STRING_TYPE == basestring
    else:
        assert STRING_TYPE == str

def test_python_version():
    import sys
    assert (sys.version_info[0] == 2) == PY2