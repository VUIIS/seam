#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
V1 adds the basic ``recon-all -all`` and ``recon-all -i`` commands.
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'

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
