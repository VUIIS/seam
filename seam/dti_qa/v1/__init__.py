#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
V1 defines the following:

* :func:`seam.dti_qa.v1.dtiqa_mcode` that generates m-code to run DTI_QA.
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'

import os

from ...util import STRING_TYPE

def dtiqa_mcode(images, basedir, dtiqa_path, n_b0=1):
    """
    Returns m-code that can be executed in matlab to run DTI_QA

    :param str,list images: path to single raw DTI image or list of multiple
    :param str basedir: base directory to write results
    :param str dtiqa_path: path to DTI_QA installation
    :param int n_b0: # of b0 averages (default is 1)

    Usage::

      >>> from seam.dti_qa.v1 import dtiqa_mcode
      >>> images = ['/path/to/first.nii', '/path/to/second.nii']
      >>> basedir, n_b0, dtiqa_path = '/path/to/output', 6, '/path/to/dtiqa'
      >>> f = open('dti_qa.m', 'w')
      >>> f.write(dtiqa_mcode(images, basedir, dtiqa_path, n_b0))
      >>> f.close()
    """
    template = """addpath(genpath('{dtiqa_path}'))
ec = 0;
try
    {pipeline_command}
    load {regmat}
    load {outmat}
    csvwrite('{rotcsv}', rotation);
    csvwrite('{transcsv}', translation);
    csvwrite('{outcsv}', outs);
    boxplotsmat_to_csv('{biasmat}', '{biascsv}');
    boxplotsmat_to_csv('{famat}', '{facsv}');
    boxplotsmat_to_csv('{fasigmamat}', '{fasigmacsv}');
    boxplotsmat_to_csv('{mdmat}', '{mdcsv}');
catch exception
    disp(exception.message)
    ec = 1;
end
disp(['Exiting with status ' num2str(ec)]);
exit(ec);
"""
    if isinstance(images, STRING_TYPE):
        # single image passed as string
        pipeline_template = "DTI_QA_Pipeline('{images}', '{basedir}', '{dtiqa_path}', {n_b0});"
        pipeline_command = pipeline_template.format(**locals())
    elif len(images) == 1:
        # one image in the list, still need to run regular
        pipeline_template = "DTI_QA_Pipeline('{image_string}', '{basedir}', '{dtiqa_path}', {n_b0});"
        image_string = images[0]
        pipeline_command = pipeline_template.format(**locals())
    else:
        # Multiple images, run DTI_QA_Pipeline_Multi
        pipeline_template = "DTI_QA_Pipeline_Multi('{dtiqa_path}', '{basedir}', {n_b0}, [], {image_string});"
        image_string = ', '.join("'{}'".format(im) for im in images)
        pipeline_command = pipeline_template.format(**locals())
    regmat = os.path.join(basedir, 'extra', 'Registration_motion.mat')
    outmat = os.path.join(basedir, 'extra', 'Outliers.mat')
    rotcsv = os.path.join(basedir, 'extra', 'Rotation.csv')
    transcsv = os.path.join(basedir, 'extra', 'Translation.csv')
    outcsv = os.path.join(basedir, 'extra', 'Outliers.csv')
    biasmat = os.path.join(basedir, 'extra', 'BoxplotsBias.mat')
    biascsv = os.path.join(basedir, 'extra', 'BoxplotsBias.csv')
    famat = os.path.join(basedir, 'extra', 'BoxplotsFA.mat')
    facsv = os.path.join(basedir, 'extra', 'BoxplotsFA.csv')
    fasigmamat = os.path.join(basedir, 'extra', 'BoxplotsFAsigma.mat')
    fasigmacsv = os.path.join(basedir, 'extra', 'BoxplotsFAsigma.csv')
    mdmat = os.path.join(basedir, 'extra', 'BoxplotsMD.mat')
    mdcsv = os.path.join(basedir, 'extra', 'BoxplotsMD.csv')
    return template.format(**locals())