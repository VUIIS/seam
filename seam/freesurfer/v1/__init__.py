#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
V1 defines the following recipes:

* :func:`seam.freesurfer.v1.build_recipe` for building a complete
  script for executing the recon-all pipeline.

V1 defines the following functions:

* ``recon-all -all`` exposed through :func:`seam.freesurfer.v1.recon_all`
* ``recon-all -i`` exposed through :func:`seam.freesurfer.v1.recon_input`
* :func:`seam.freesurfer.v1.tkmedit_screenshot_tcl` for generating tcl
  to take screenshots of a volume loaded in ``tkmedit``.
* :func:`seam.freesurfer.v1.tkmedit_screenshot_cmd` for supplying a
  command to execute ``tkmedit`` with a tcl script.
* :func:`seam.freesurfer.v1.tksurfer_screenshot_tcl` for generating a
  tcl script to take screenshots of a hemisphere using ``tksurfer``
* :func:`seam.freesurfer.v1.tksurfer_screenshot_cmd` for supplying a
  command to run ``tksurfer`` and generate screenshots.
* :func:`seam.freesurfer.v1.annot2label_cmd` for building a
  ``mri_annotation2label`` command.
* :func:`seam.freesurfer.v1.mri_binarize` for building ``mri_binarize`` commands.
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

from .core import recon_all, recon_input, tkmedit_screenshot_tcl, \
    tkmedit_screenshot_cmd, tksurfer_screenshot_tcl, tksurfer_screenshot_cmd, \
    annot2label_cmd, mri_binarize
from .recipe import build_recipe
