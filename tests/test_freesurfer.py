#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_freesurfer.py

Functions for testing freesurfer interfaces
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

# Version specific
v1_recon_all = 'recon-all -s foo -all -qcache -measure thickness' \
    ' -measure curv -measure sulc -measure area -measure jacobian_white'
v1_recon_input = 'recon-all -s foo -i /path/to/data/t1.nii'
v1_recon_input_multi = 'recon-all -s foo -i /path/to/data/first.nii -i /path/to/data/second.nii'

# Current
current_recon_all = v1_recon_all
current_recon_input = v1_recon_input


def test_v1_recon_all():
    from seam.freesurfer.v1 import recon_all
    assert v1_recon_all == recon_all('foo')
    with_flags = v1_recon_all + ' -use-gpu -mprage -log /path/to/file'
    assert with_flags == recon_all('foo', flags=['-use-gpu',
        '-mprage', '-log /path/to/file'])

def test_v1_recon_input():
    from seam.freesurfer.v1 import recon_input
    assert v1_recon_input == recon_input('foo', '/path/to/data/t1.nii')
    assert v1_recon_input_multi == recon_input('foo',
        ['/path/to/data/first.nii', '/path/to/data/second.nii'])

def test_current_recon_all():
    from seam.freesurfer import recon_all
    assert current_recon_all == recon_all('foo')

def test_current_recon_input():
    from seam.freesurfer import recon_input
    assert current_recon_input == recon_input('foo', '/path/to/data/t1.nii')
