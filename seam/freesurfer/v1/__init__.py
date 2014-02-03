#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py

Freesurfer V1
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'

from ...util import STRING_TYPE

base_parts = ['recon-all', '-s {subject_id}']

def recon_all(subject_id, flags=None):
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
    parts = list(base_parts)
    if isinstance(data, STRING_TYPE):
        parts.append('-i {}'.format(data))
    else:
        # We were passed a list of images
        parts.extend(['-i {}'.format(image) for image in data])
    return ' '.join(parts).format(**locals())
