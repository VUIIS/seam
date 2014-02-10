#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Tests for DTI_QA functionality
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2013 Vanderbilt University. All Rights Reserved'

from seam.dti_qa import dtiqa_mcode
from seam.dti_qa import v1

v1_single_mcode = """addpath(genpath('/path/to/dti_qa'))
ec = 0;
try
    DTI_QA_Pipeline('/path/to/dti.nii', '/path/to/basedir', '/path/to/dti_qa', 6);
    load /path/to/basedir/extra/Registration_motion.mat
    load /path/to/basedir/extra/Outliers.mat
    csvwrite('/path/to/basedir/extra/Rotation.csv', rotation);
    csvwrite('/path/to/basedir/extra/Translation.csv', translation);
    csvwrite('/path/to/basedir/extra/Outliers.csv', outs);
    boxplotsmat_to_csv('/path/to/basedir/extra/BoxplotsBias.mat', '/path/to/basedir/extra/BoxplotsBias.csv');
    boxplotsmat_to_csv('/path/to/basedir/extra/BoxplotsFA.mat', '/path/to/basedir/extra/BoxplotsFA.csv');
    boxplotsmat_to_csv('/path/to/basedir/extra/BoxplotsFAsigma.mat', '/path/to/basedir/extra/BoxplotsFAsigma.csv');
    boxplotsmat_to_csv('/path/to/basedir/extra/BoxplotsMD.mat', '/path/to/basedir/extra/BoxplotsMD.csv');
catch exception
    disp(exception.message)
    ec = 1;
end
disp(['Exiting with status ' num2str(ec)]);
exit(ec);
"""
v1_multi_mcode = """addpath(genpath('/path/to/dti_qa'))
ec = 0;
try
    DTI_QA_Pipeline_Multi('/path/to/dti_qa', '/path/to/basedir', 6, [], '/path/to/first.nii', '/path/to/second.nii');
    load /path/to/basedir/extra/Registration_motion.mat
    load /path/to/basedir/extra/Outliers.mat
    csvwrite('/path/to/basedir/extra/Rotation.csv', rotation);
    csvwrite('/path/to/basedir/extra/Translation.csv', translation);
    csvwrite('/path/to/basedir/extra/Outliers.csv', outs);
    boxplotsmat_to_csv('/path/to/basedir/extra/BoxplotsBias.mat', '/path/to/basedir/extra/BoxplotsBias.csv');
    boxplotsmat_to_csv('/path/to/basedir/extra/BoxplotsFA.mat', '/path/to/basedir/extra/BoxplotsFA.csv');
    boxplotsmat_to_csv('/path/to/basedir/extra/BoxplotsFAsigma.mat', '/path/to/basedir/extra/BoxplotsFAsigma.csv');
    boxplotsmat_to_csv('/path/to/basedir/extra/BoxplotsMD.mat', '/path/to/basedir/extra/BoxplotsMD.csv');
catch exception
    disp(exception.message)
    ec = 1;
end
disp(['Exiting with status ' num2str(ec)]);
exit(ec);
"""

current_single_mcode = v1_single_mcode
current_multi_mcode = v1_multi_mcode

def single_args_factory():
    return '/path/to/dti.nii', '/path/to/basedir', '/path/to/dti_qa', 6

def single_args_factory_list():
    return ['/path/to/dti.nii'], '/path/to/basedir', '/path/to/dti_qa', 6

def multi_args_factory():
    return ['/path/to/first.nii', '/path/to/second.nii'], '/path/to/basedir', '/path/to/dti_qa', 6


# Test current
def test_current_dtiqa_single():
    args = single_args_factory()
    assert current_single_mcode == dtiqa_mcode(*args)

def test_current_dtiqa_single_list():
    args = single_args_factory_list()
    assert current_single_mcode == dtiqa_mcode(*args)

def test_current_dtiqa_multi():
    args = multi_args_factory()
    assert current_multi_mcode == dtiqa_mcode(*args)

# Testing v1
def test_v1_dtiqa_single():
    args = single_args_factory()
    assert v1_single_mcode == v1.dtiqa_mcode(*args)

def test_v1_dtiqa_single_list():
    args = single_args_factory_list()
    assert v1_single_mcode == v1.dtiqa_mcode(*args)

def test_v1_dtiqa_multi():
    args = multi_args_factory()
    assert v1_multi_mcode == v1.dtiqa_mcode(*args)



