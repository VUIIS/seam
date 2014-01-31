#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" __init__.py

Freesurfer V1
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'

import sys
if sys.version_info > (3, 0):
    STRING_TYPE = str
else:
    STRING_TYPE = basestring


def recon_all(subject_id):
    parts = ['recon-all',
             '-s {}'.format(subject_id),
             '-all',
             '-qcache',
             '-measure thickness',
             '-measure curv',
             '-measure sulc',
             '-measure area',
             '-measure jacobian_white']
    return ' '.join(parts)


def recon_input(subject_id, data):
    parts = ['recon-all',
             '-s {}'.format(subject_id)]
    if isinstance(data, STRING_TYPE):
        parts.append('-i {}'.format(data))
    else:
        # We were passed a list of images
        parts.extend(['-i {}'.format(image) for image in data])
    return ' '.join(parts)
