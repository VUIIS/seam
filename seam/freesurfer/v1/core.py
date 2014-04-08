#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" core.py

Core functions
"""

__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

import os

from ...util import STRING_TYPE

base_parts = ['recon-all', '-s {subject_id}']

def recon_all(subject_id, flags=None):
    """
    This function supplies the ``recon-all -all`` command. This command
    will run the entire anatomical analysis suite of Freesurfer.

    :note: Use :func:`seam.freesurfer.recon_input` to setup this subject
    :param str subject_id: Subject identifier on which to run ``recon-all``
    :param list flags: command-line flags to pass to ``recon-all``
    :return: command that will execute ``recon-all -all``
    :rtype: str

    Usage::

      >>> from seam.freesurfer import recon_all
      >>> recon_all('sub0001', flags=['-use-gpu'])
      'recon-all -s sub0001 -all -qcache -measure thickness -measure curv -measure sulc -measure area -measure jacobian_white -use-gpu'
    """
    parts = base_parts + ['-all',
                          '-qcache',
                          '-measure thickness',
                          '-measure curv',
                          '-measure sulc',
                          '-measure area',
                          '-measure jacobian_white']
    if flags:
        parts.extend(flags)
    return ' '.join(parts).format(**locals())


def recon_input(subject_id, data):
    """
    The function supplies the ``recon-all -i`` command. This command
    initializes the Freesurfer directory for a subject and converts
    the raw data into an internal format for use by the rest of the
    ``recon-all`` pipeline.`

    :param str subject_id: Subject identifier
    :param str,list data: path(s) to input data
    :return: command that will execute ``recon-all -i`` command
    :rtype: str

    Usage::

      >>> from seam.freesurfer import recon_input
      >>> recon_input('sub0001', '/full/path/to/data.nii')
      'recon-all -s sub0001 -i /full/path/to/data.nii'
      >>> # or with multiple inputs...
      >>> recon_input('sub0001', ['/path/first.nii', '/path/second.nii'])
      'recon-all -s sub0001 -i /path/first.nii -i /path/second.nii'
    """
    parts = list(base_parts)
    if isinstance(data, STRING_TYPE):
        parts.append('-i {}'.format(data))
    else:
        # We were passed a list of images
        parts.extend(['-i {}'.format(image) for image in data])
    return ' '.join(parts).format(**locals())


def tkmedit_screenshot_tcl(basepath, beg=5, end=256, step=10):
    """
    Supplies a tcl string that can be used to take screenshots of a volume
    using `tkmedit <http://surfer.nmr.mgh.harvard.edu/fswiki/TkMeditGuide/TkMeditGeneralUsage/TkMeditInterface>`_

    Images are written to ``*basepath*/tkmedit-$i.tiff``
    where *beg* <= i <= *end* in increments of *step*

    :param basepath: base directory to write images in
    :param int beg: Beginning slice where screenshots begin
    :param int end: End slice where screenshots end
    :param int step: Value to increment successive screenshots

    Usage::

      >>> from seam.freesurfer import tkmedit_screenshot_tcl
      >>> f = open('tmedit_screenshots.tcl', 'w')
      >>> f.write(tkmedit_screenshot_tcl('/path/to/image_dir'))
      >>> f.close()
      $ tkmedit sub0001 brain.finalsurfs.mgz -aseg -surfs -tcl tkmedit_screenshots.tcl
    """
    template = """for {{ set i {beg} }} {{ $i < {end} }} {{ incr i {step} }} {{
SetSlice $i
RedrawScreen
SaveTIFF {tiff_path}
}}
exit
"""
    tiff_path = os.path.join(basepath, 'tkmedit-$i.tiff')
    return template.format(**locals())


def tkmedit_screenshot_cmd(subject_id, volume, tcl_path, flags=None):
    """
    Supplies a command to execute a tcl script in ``tkmedit`` for
    *subject_id*'s *volume*

    :param str subject_id: subject identifier
    :param str volume: Volume for tkmedit to load
    :param str tcl_path: Path to tcl script
    :param list flags: Flags to pass to ``tkmedit``

    Usage::

      >>> from seam.freesurfer import tkmedit_screenshot_cmd
      >>> tkmedit_screenshot_cmd('sub0001', 'brain.finalsurfs.mgz', '/path/tkmedit.tcl', ['-aseg', '-surfs'])
      'tkmedit sub0001 brain.finalsurfs.mgz -aseg -surfs -tcl /path/tkmedit.tcl'
    """
    template = "tkmedit {subject_id} {volume} {flag_string} -tcl {tcl_path}"
    if flags:
        flag_string = ' '.join(flags)
    return template.format(**locals())


def tksurfer_screenshot_tcl(basepath, annot='aparc.a2009s.annot'):
    """
    Supplies a tcl command to take screenshots of a surface using
    `tksurfer <https://surfer.nmr.mgh.harvard.edu/fswiki/tksurfer>`_

    Four screenshots are taken:

    * lateral view (default view when ``tksurfer`` opens) saved to *basepath*-lateral.tiff
    * medial view saved to *basepath*-medial.tiff
    * Lateral view with an annotation loaded (given by *annot*)
      saved to *basepath*-annot-lateral.tiff
    * Medial view with an annotation loaded (given by *annot*)
      saved to *basepath*-annot-medial.tiff

    :param str basepath: prefix for images to be saved
    :param str annot: annotation file to load for overlay on the surface

    Usage::

     >>> from seam.freesurfer import tksurfer_screenshot_tcl
     >>> f = open('tksurfer.lh.tcl', 'w')
     >>> f.write(tksurfer_screenshot_tcl('/path/to/screenshots/lh'))
     >>> f.close()
    """
    template = """make_lateral_view;
redraw;
save_tiff {basepath}-lateral.tiff;
rotate_brain_y 180;
redraw;
save_tiff {basepath}-medial.tiff;
labl_import_annotation {annot};
redraw;
make_lateral_view;
redraw;
save_tiff {basepath}-annot-lateral.tiff;
rotate_brain_y 180;
redraw;
save_tiff {basepath}-annot-medial.tiff;
exit;"""
    return template.format(**locals())


def tksurfer_screenshot_cmd(subject_id, hemi, surface, tcl_path, flags=None):
    """
    Supply a command that will run ``tksurfer`` using the *surface* from
    *subject_id*'s *hemi* hemisphere and execute a tcl script.

    :param str subject_id: subject identifier
    :param str hemi: 'lh' or 'rh', hemisphere to open in tksurfer
    :param str surface: surface to view
    :param str tcl_path: path to tcl script to execute
    :param list flags: flags to pass into ``tksurfer``

    Usage::

      >>> from seam.freesurfer import tksurfer_screenshot_cmd
      >>> tksurfer_screenshot_cmd('sub0001', 'lh', 'inflated', '/path/tksurfer.lh.tcl', ['-gray'])
      'tksurfer sub0001 lh inflated -gray -tcl /path/tksurfer.lh.tcl'
    """
    template = "tksurfer {subject_id} {hemi} {surface} {flag_string}-tcl {tcl_path}"
    if flags:
        flag_string = ' '.join(flags) + ' '
    else:
        flag_string = ''
    return template.format(**locals())


def annot2label_cmd(subject_id, hemi, annot_path, outdir, surface='white'):
    """
    Build the mri_annotation2label commandline string.

    :param str subject_id: subject identifier
    :param str hemi: 'lh' or 'rh', hemisphere to use
    :param str annot_path: path to annotation file
    :param str outdir: output directory to place labels
    :param str surface: surface to use when generating coords in labels
    """
    template = "mri_annotation2label --subject {subject_id} --hemi {hemi} --annotation {annot_path} --outdir {outdir} --surface {surface}"
    return template.format(**locals())
