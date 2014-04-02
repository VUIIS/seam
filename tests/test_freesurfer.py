#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_freesurfer.py

Functions for testing freesurfer functionality
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from seam.freesurfer import recon_all, recon_input, tkmedit_screenshot_tcl,\
    tkmedit_screenshot_cmd, tksurfer_screenshot_tcl, tksurfer_screenshot_cmd,\
    annot2label_cmd
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
v1_tksurfer_screenshot_tcl = """make_lateral_view;
redraw;
save_tiff /path/to/screenshots/lh-lateral.tiff;
rotate_brain_y 180;
redraw;
save_tiff /path/to/screenshots/lh-medial.tiff;
labl_import_annotation aparc.a2009s.annot;
redraw;
make_lateral_view;
redraw;
save_tiff /path/to/screenshots/lh-annot-lateral.tiff;
rotate_brain_y 180;
redraw;
save_tiff /path/to/screenshots/lh-annot-medial.tiff;
exit;"""
v1_tksurfer_screenshot_cmd = "tksurfer foo lh inflated -gray -tcl /path/tksurfer.lh.tcl"
v1_tksurfer_screenshot_cmd_no_flags = "tksurfer foo lh inflated -tcl /path/tksurfer.lh.tcl"
v1_annot2label_cmd = 'mri_annotation2label --subject foo --hemi lh --annotation bar.annot --outdir /path/to/bat/ --surface white'

# Current
current_recon_all = v1_recon_all
current_recon_input = v1_recon_input
current_tkmedit_screenshot_tcl = v1_tkmedit_screenshot_tcl
current_tkmedit_screenshot_cmd = v1_tkmedit_screenshot_cmd
current_tksurfer_screenshot_tcl = v1_tksurfer_screenshot_tcl
current_tksurfer_screenshot_cmd = v1_tksurfer_screenshot_cmd
current_annot2label_cmd = v1_annot2label_cmd

# Current tests
def test_current_recon_all():
    assert current_recon_all == recon_all('foo')

def test_current_recon_input():
    assert current_recon_input == recon_input('foo', '/path/to/data/t1.nii')

def test_current_tkmedit_screenshot_tcl():
    assert current_tkmedit_screenshot_tcl == tkmedit_screenshot_tcl('/path/to/screenshots/')

def test_current_tkmedit_screenshot_cmd():
    cmd = tkmedit_screenshot_cmd('foo', 'brain.mgz', '/path/tkmedit.tcl', ['-aseg', '-surfs'])
    assert current_tkmedit_screenshot_cmd == cmd

def test_current_tksurfer_screenshot_tcl():
    assert current_tksurfer_screenshot_tcl == tksurfer_screenshot_tcl('/path/to/screenshots/lh')

def test_current_tksurfer_screenshot_cmd():
    cmd = tksurfer_screenshot_cmd('foo', 'lh', 'inflated', '/path/tksurfer.lh.tcl', ['-gray'])
    assert current_tksurfer_screenshot_cmd == cmd


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

def test_v1_tksurfer_screenshot_tcl():
    assert v1_tksurfer_screenshot_tcl == v1.tksurfer_screenshot_tcl('/path/to/screenshots/lh')

def test_v1_tksurfer_screenshot_cmd():
    cmd = v1.tksurfer_screenshot_cmd('foo', 'lh', 'inflated', '/path/tksurfer.lh.tcl', ['-gray'])
    assert v1_tksurfer_screenshot_cmd == cmd
    cmd_no_flags = v1.tksurfer_screenshot_cmd('foo', 'lh', 'inflated', '/path/tksurfer.lh.tcl')
    assert v1_tksurfer_screenshot_cmd_no_flags == cmd_no_flags

def test_v1_annot2label_cmd():
    cmd = v1.annot2label_cmd('foo', hemi='lh', annot_path='bar.annot', outdir='/path/to/bat/')
    assert cmd == v1_annot2label_cmd

# Recipe Testing
def test_script_filename():
    assert v1.recipe.recon_script_name('foo') == 'foo.recon.sh'

def test_tkmedit_tcl_fname():
    assert v1.recipe.tkmedit_tcl_name('foo') == 'foo.tkmedit.tcl'

def test_screenshot_dirname():
    assert v1.recipe.screenshots_dir('foo') == 'foo_screenshots'

def test_annot_path():
    known_file = '/path/to/subjects/foo/label/lh.aparc.a2009s.annot'
    assert v1.recipe.a2009s_file('foo', '/path/to/subjects', 'lh') == known_file

def test_label_dir():
    known = '/path/to/subjects/foo/label'
    assert v1.recipe.label_directory('foo', '/path/to/subjects') == known

def test_parser():
    ap = v1.recipe.get_parser()
    cmd_line = 'foo /path/to/scripts -i /path/to/image.nii --use-xvfb --recon-flag \'-mprage\''
    args = ap.parse_args(cmd_line.split())
    assert args.subject_id == 'foo'
    assert args.script_dir == '/path/to/scripts'
    assert args.inputs == ['/path/to/image.nii']
    assert args.use_xvfb == True
    assert args.recon_flags == '\'-mprage\''
