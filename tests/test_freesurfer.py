#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_freesurfer.py

Functions for testing freesurfer interfaces
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from seam.freesurfer import recon_all, recon_input

def test_recon_all():
    good_cmd = 'recon-all -s foo -all -qcache -measure thickness' \
    ' -measure curv -measure sulc -measure area -measure jacobian_white'
    assert good_cmd == recon_all('foo')

def test_recon_input_single():
    subject = 'foo'
    data = '/path/to/data/t1.nii'
    good_cmd = 'recon-all -s foo -i /path/to/data/t1.nii'
    assert good_cmd == recon_input(subject, data)

def test_recon_input_multi():
    subject = 'foo'
    data = ['/path/to/data/first.nii', '/path/to/data/second.nii']
    good_cmd = 'recon-all -s foo -i /path/to/data/first.nii -i /path/to/data/second.nii'
    assert good_cmd == recon_input(subject, data)
