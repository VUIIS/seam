#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
DTI_QA
======

This interface assists in executing `Bennett Landman's DTI_QA <http://www.ncbi.nlm.nih.gov/pubmed/23637895>`_
toolkit.

TBD: More documentation here.

Because DTI_QA is built upon matlab, the generated commands are m-code.

Functions
+++++++++
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'


from .v1 import dtiqa_mcode

__all__ = ['dtiqa_mcode']
