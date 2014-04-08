#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" util.py

Utility functions/constants across seam
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

import sys
import os
from string import digits, ascii_letters
from random import choice

PY2 = sys.version_info[0] == 2
if PY2:
    STRING_TYPE = basestring
else:
    STRING_TYPE = str

total = digits + ascii_letters

def get_tmp_filename(ext='out', basename='/tmp', fname_length=32):
    fname = ''.join(choice(total) for _ in range(fname_length))
    return os.path.join(basename, '{}.{}'.format(fname, ext))

def wrap_with_xvfb(command, wait=5, server_args='-screen 0, 1600x1200x24'):
    parts = ['xvfb-run',
        '-a', # automatically get a free server number
        '-f {}'.format(get_tmp_filename()),
        '-e {}'.format(get_tmp_filename(ext='err')),
        '--wait={:d}'.format(wait),
        '--server-args="{}"'.format(server_args),
        command]
    return ' '.join(parts)
