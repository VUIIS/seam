#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" util.py

Utility functions/constants across seam
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

import sys
PY2 = sys.version_info[0] == 2
if PY2:
    STRING_TYPE = basestring
else:
    STRING_TYPE = str
