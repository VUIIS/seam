#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py

FSL V1 API
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from .core import flirt, fnirt, invwarp, applywarp, convert_xfm

__all__ = ['flirt', 'fnirt', 'invwarp', 'applywarp', 'convert_xfm']