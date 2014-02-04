#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_freesurfer.py

Functions for testing freesurfer functionality
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from seam.freesurfer import recon_all, recon_input, tkmedit_screenshot_tcl,\
    tkmedit_screenshot_cmd
from seam.freesurfer import v1

# Version specific
v1_recon_all = 'recon-all -s foo -all -qcache -measure thickness' \
    ' -measure curv -measure sulc -measure area -measure jacobian_white'
v1_recon_input = 'recon-all -s foo -i /path/to/data/t1.nii'
v1_recon_input_multi = 'recon-all -s foo -i /path/to/data/first.nii -i /path/to/data/second.nii'
v1_tkmedit_screenshot_tcl = """for { set i 5 } { $i < 256 } { incr i 10 } {
SetSlice $i
RedrawScreen
SaveTIFF /path/to/screenshots/tkmedit-$i.tiff
}
exit
"""
v1_tkmedit_screenshot_cmd = "tkmedit foo brain.mgz -aseg -surfs -tcl /path/tkmedit.tcl"

# Current
current_recon_all = v1_recon_all
current_recon_input = v1_recon_input
current_tkmedit_screenshot_tcl = v1_tkmedit_screenshot_tcl
current_tkmedit_screenshot_cmd = v1_tkmedit_screenshot_cmd


# Current tests
def test_current_recon_all():
    assert current_recon_all == recon_all('foo')

def test_current_recon_input():
    assert current_recon_input == recon_input('foo', '/path/to/data/t1.nii')

def test_current_tkmedit_screenshot_tcl():
    assert current_tkmedit_screenshot_tcl == tkmedit_screenshot_tcl('/path/to/screenshots/')

def test_current_tkmedit_Screenshot_cmd():
    cmd = tkmedit_screenshot_cmd('foo', 'brain.mgz', '/path/tkmedit.tcl', ['-aseg', '-surfs'])
    assert current_tkmedit_screenshot_cmd == cmd


# V1 tests
def test_v1_recon_all():
    assert v1_recon_all == v1.recon_all('foo')
    with_flags = v1_recon_all + ' -use-gpu -mprage -log /path/to/file'
    assert with_flags == v1.recon_all('foo', flags=['-use-gpu',
        '-mprage', '-log /path/to/file'])

def test_v1_recon_input():
    assert v1_recon_input == v1.recon_input('foo', '/path/to/data/t1.nii')
    assert v1_recon_input_multi == v1.recon_input('foo',
        ['/path/to/data/first.nii', '/path/to/data/second.nii'])

def test_v1_tkmedit_screenshot_tcl():
    assert v1_tkmedit_screenshot_tcl == v1.tkmedit_screenshot_tcl('/path/to/screenshots/')

def test_v1_tkmedit_screenshot_cmd():
    cmd = v1.tkmedit_screenshot_cmd('foo', 'brain.mgz', '/path/tkmedit.tcl', ['-aseg', '-surfs'])
    assert v1_tkmedit_screenshot_cmd == cmd
