#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" recipe.py

Main Recipe for V1 Recon stuff
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

import os
from stat import S_IRWXU
from os.path import join
from datetime import datetime
from warnings import warn
from argparse import ArgumentParser

from ... import __version__ as version
from ...util import wrap_with_xvfb
from .core import recon_input, recon_all, tkmedit_screenshot_cmd, \
    tkmedit_screenshot_tcl, tksurfer_screenshot_cmd, tksurfer_screenshot_tcl, \
    annot2label_cmd


def recon_script_name(subject_id):
    return "{}.recon.sh".format(subject_id)

def tkmedit_tcl_name(subject_id):
    return "{}.tkmedit.tcl".format(subject_id)

def tksurfer_tcl_name(subject_id, hemi):
    return "{}.tksurfer.{}.tcl".format(subject_id, hemi)

def screenshots_dir(subject_id):
    return "{}_screenshots".format(subject_id)

def tksurfer_screenshot_basepath(script_dir, subject_id, hemi):
    return join(script_dir, screenshots_dir(subject_id), hemi)

def a2009s_file(subject_id, sd, hemi):
    return join(label_directory(subject_id, sd), '{}.aparc.a2009s.annot'.format(hemi))

def label_directory(subject_id, sd):
    return join(sd, subject_id, 'label')

def recon_parts(subject_id, input_data, recon_flags=None):
    "Build the recon_input and recon_all commands"
    recon_input_cmd = recon_input(subject_id, input_data)
    recon_all_cmd = recon_all(subject_id, recon_flags)
    return recon_input_cmd, recon_all_cmd

def tkmedit_parts(subject_id, script_dir, use_xvfb=False):
    ss_dir = join(script_dir, screenshots_dir(subject_id))
    tkmedit_tcl_script = tkmedit_screenshot_tcl(ss_dir)
    tkmedit_tcl_path = join(script_dir, tkmedit_tcl_name(subject_id))
    tkmedit_cmd = tkmedit_screenshot_cmd(subject_id, 'brain.finalsurfs.mgz',
        tkmedit_tcl_path, flags=['-aseg', '-surfs'])
    if use_xvfb:
        tkmedit_cmd = wrap_with_xvfb(tkmedit_cmd)
    return tkmedit_tcl_script, tkmedit_tcl_path, tkmedit_cmd

def tksurfer_parts(subject_id, script_dir, hemi, use_xvfb=False):
    tksurfer_tcl_path = join(script_dir,
        tksurfer_tcl_name(subject_id, hemi))
    # Basepath to screenshots
    ss_basepath = tksurfer_screenshot_basepath(script_dir, subject_id, hemi)
    # Script string
    tksurfer_tcl_script = tksurfer_screenshot_tcl(ss_basepath)
    tksurfer_cmd = tksurfer_screenshot_cmd(subject_id, hemi, 'inflated',
        tksurfer_tcl_path, ['-gray'])
    if use_xvfb:
        tksurfer_cmd = wrap_with_xvfb(tksurfer_cmd)
    return tksurfer_tcl_script, tksurfer_tcl_path, tksurfer_cmd

def build_recipe(subject_id, input_data, script_dir, use_xvfb=False,
    recon_flags=None):
    """This function builds a complete pipeline around Freesufer.

    It does the following:

    * Imports data using ``recon-all -i``
    * Runs the main ``recon-all`` command with the following flags:
        * ``-qcache``
        * ``-measure thickness``
        * ``-measure curv``
        * ``-measure sulc``
        * ``-measure area``
        * ``-measure jacobian_white``
    * Takes volumetric snapshots using ``tkmedit``
    * Per hemisphere:
        * Converts the aparc.a2009s.annot file to labels in the subject's
          ``label`` directory
        * Takes screenshots of the inflated surface with and without the
          advanced labels.

    :param str subject_id: subject identifier
    :param str,list input_data: list of paths or string to subject's T1 images
    :param str script_dir: directory to write scripts & screenshots
    :param boolean use_xvfb: Wrap ``tksurfer`` & ``tkmedit`` commands in xvfb-run,
      useful if running in a non-graphical (ie cluster) environment.
    :param list recon_flags: other flags to pass to ``recon-all``

    :rtype: tuple
    :return: paths to recon script, tkmedit script and lh & rh tksurfer scripts
    :note: the main script is set as executable
    :note: This function is exposed on the command line through ``build-recon-v1``
    """
    to_return = []
    if 'SUBJECTS_DIR' not in os.environ:
        msg = """You have not set your $SUBJECTS_DIR environment variable.

Using {} as your SUBJECTS_DIR""".format(script_dir)
        warn(msg, category=UserWarning)
        sd = script_dir
    else:
        sd = os.environ['SUBJECTS_DIR']
    # Check script directory
    if not os.path.isdir(script_dir):
        os.makedirs(script_dir)
    ss_dir = join(script_dir, screenshots_dir(subject_id))
    if not os.path.isdir(ss_dir):
        os.makedirs(ss_dir)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # recon commands
    input_cmd, all_cmd = recon_parts(subject_id, input_data, recon_flags)
    # tkmedit parts
    tkm_tcl_script, tkm_tcl_path, tkm_cmd = tkmedit_parts(subject_id,
        script_dir, use_xvfb)
    with open(tkm_tcl_path, 'w') as f:
        f.write(tkm_tcl_script)

    final_script = os.path.join(script_dir, recon_script_name(subject_id))
    to_return.append(final_script)
    to_return.append(tkm_tcl_path)
    ingredients = ["#!/bin/bash",
        "# Generated by seam version {} at {}".format(version, now),
        "",
        "# Recon Input Command",
        input_cmd,
        "",
        "# Recon All command",
        all_cmd,
        "",
        "# TKMedit Screenshots command",
        tkm_cmd,]
    for hemi in ('lh', 'rh'):
        # annot2label on the 2009 atlas
        annot_file = a2009s_file(subject_id, sd, hemi)
        label_dir = label_directory(subject_id, sd)
        a2l_cmd = annot2label_cmd(subject_id, hemi=hemi, annot_path=annot_file,
            outdir=label_dir, surface='white')
        ingredients.extend(["", "# Convert 2009 {} annotation to labels".format(hemi),
            a2l_cmd])
        # tksurfer parts
        tks_tcl_script, tks_tcl_path, tks_cmd = tksurfer_parts(subject_id,
            script_dir, hemi, use_xvfb)
        with open(tks_tcl_path, 'w') as f:
            f.write(tks_tcl_script)
        to_return.append(tks_tcl_path)
        ingredients.extend(["",
            "# TKSurfer {} Screenshot command".format(hemi),
            tks_cmd])

    with open(final_script, 'w') as f:
        f.write('\n'.join(ingredients))
        f.write('\n')
    os.chmod(final_script, S_IRWXU)
    return tuple(to_return)


def get_parser():
    desc = "Build an opinionated & complete Freesurfer script"
    epi = "Unknown flags will be passed to recon-all"
    ap = ArgumentParser(prog='build-recon-v1', description=desc,
        add_help=True, epilog=epi)
    ap.add_argument('subject_id', help="Subject Identifier")
    ap.add_argument('script_dir', help="Directory to write scripts")
    ap.add_argument('-i', '--input', action='append', help="Input images",
        dest="inputs")
    ap.add_argument('--use-xvfb', action='store_true', default=False,
        dest="use_xvfb", help="Use xvfb-run for graphical programs")
    return ap


def main():
    ap = get_parser()
    args, recon_flags = ap.parse_known_args()
    written_files = build_recipe(subject_id=args.subject_id,
        input_data=args.inputs, script_dir=args.script_dir,
        use_xvfb=args.use_xvfb, recon_flags=recon_flags)
    main_script, tkm_script, tks_lh, tks_rh = written_files
    print("Main executable script written to {}".format(main_script))

if __name__ == '__main__':
    main()