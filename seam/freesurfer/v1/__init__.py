#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
V1 adds the following:

* ``recon-all -all`` exposed through :func:`seam.freesurfer.v1.recon_all`
* ``recon-all -i`` exposed through :func:`seam.freesurfer.v1.recon_input`
* :func:`seam.freesurfer.v1.tkmedit_screenshot_tcl` for generating tcl
  to take screenshots of a volume loaded in ``tkmedit``.
* :func:`seam.freesurfer.v1.tkmedit_screenshot_cmd` for supplying a
  command to execute ``tkmedit`` with a tcl script.

"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'

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
