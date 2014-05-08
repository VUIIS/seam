#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" test_fsl.py

Testing FSL functions
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

import pytest
from seam.fsl.v1 import flirt, fnirt, invwarp, applywarp, convert_xfm, bet,\
    probtrackx2


def test_v1_flirt():
    flirt_cmd = 'flirt -in input -ref ref -omat in2ref.mat -out in_ref_flirt -inter spline'
    comp_cmd = flirt(input='input', ref='ref', omat='in2ref.mat',
        out='in_ref_flirt')
    assert flirt_cmd == comp_cmd

    with pytest.raises(ValueError):
        # assert we raise with no output
        flirt(input='foo', ref='ref')


def test_v1_flirt_flags():
    flirt_cmd = 'flirt -in input -ref ref -omat in2ref.mat -out in_ref_flirt -inter spline -cost bbr'
    comp_cmd = flirt(input='input', ref='ref', omat='in2ref.mat',
        out='in_ref_flirt', flags=['-cost bbr'])
    assert flirt_cmd == comp_cmd


def test_v1_fnirt():
    fnirt_cmd = 'fnirt --in=input --ref=ref --cout=in2ref_warp --iout=in_ref_fnirt --config=T1_2_MNI152_2mm.cnf'
    comp_cmd = fnirt(input='input', ref='ref',
        cout='in2ref_warp', iout='in_ref_fnirt',
        flags=['--config=T1_2_MNI152_2mm.cnf', ])
    assert fnirt_cmd == comp_cmd

    with pytest.raises(ValueError):
        # assert we raise with no output
        fnirt(input='foo', ref='ref')


def test_v1_invwarp():
    invwarp_cmd = 'invwarp -w t12mni_warp -r mni -o mni2t1_warp'
    assert invwarp_cmd == invwarp(warp='t12mni_warp',
                                  ref='mni',
                                  out='mni2t1_warp')


def test_v1_applywarp():
    # test defaults
    applywarp_cmd = 'applywarp -i t1 -o t1_mni -r mni -w t12mni_warp --interp=spline -s --superlevel=a'
    assert applywarp_cmd == applywarp(input='t1', out='t1_mni', warp='t12mni_warp', ref='mni')

    # no supersampling, different interp
    applywarp_cmd = 'applywarp -i t1 -o t1_mni -r mni -w t12mni_warp --interp=nn'
    assert applywarp_cmd == applywarp(input='t1', out='t1_mni',
        warp='t12mni_warp', ref='mni', super=False, interp='nn')

    with pytest.raises(ValueError):
        # should raise ValueError with bad kind of interpolation
        applywarp(input='t1', out='t1_mni', warp='t12mni_warp', ref='mni',
            interp='foo')


def test_v1_convert_xfm():
    good_invert = 'convert_xfm -omat mni2t1.mat -inverse t12mni.mat'
    assert good_invert == convert_xfm(omat='mni2t1.mat', inverse='t12mni.mat')

    good_concat = 'convert_xfm -omat a2c.mat -concat b2c.mat a2b.mat'
    assert good_concat == convert_xfm(omat='a2c.mat', concat=('b2c.mat', 'a2b.mat'))

    good_fix = 'convert_xfm -omat mni2t1.mat -inverse t12mni.mat -fixscaleskew other.mat'
    assert good_fix == convert_xfm(omat='mni2t1.mat', inverse='t12mni.mat',
        fixscaleskew='other.mat')


def test_v1_bet():
    input, output = 'T1', 'T1_brain'
    bet_default = 'bet T1 T1_brain -f 0.5'
    assert bet_default == bet(input, output)

    bet_other = 'bet T1 T1_brain -f 0.25 -m -R -e'
    assert bet_other == bet(input, output, frac=0.25, mask=True,
                            flags=['-R', '-e'])


def test_v1_probtrackx2():
    s, m, x = 'merged', 'nodif_brain', 'roi'
    # totally default call
    default = probtrackx2(samples=s, mask=m, seed=x)
    good_default = 'probtrackx2 -s merged -m nodif_brain -x roi -o fdt_paths --dir=logdir --forcedir -P 5000 -S 2000 --steplength=0.5 --distthresh=0 --cthr=0.2 --fibthresh=0.01 --randfib=0 --sampvox=0 --verbose=0 --meshspace=caret --opd --os2t --s2tastext'
    assert default == good_default

    custom = probtrackx2(samples=s, mask=m, seed=x, out='paths',
        directory='results', nsamples=2000, nsteps=1000, steplength=1.0,
        distthresh=0.05, cthr=0.1, fibthresh=0, randfib=1, sampvox=5, verbose=1,
         xfm='str2dif_warp.nii.gz', invxfm='dif2str_warp.nii.gz',
         seedref='str.nii.gz', meshspace='freesurfer', opd=True, pd=True,
         usef=True, loopcheck=True, modeuler=True, flags=['--targetmasks=targets.txt', '--omatrix1'])
    good_custom = 'probtrackx2 -s merged -m nodif_brain -x roi -o paths --dir=results --forcedir -P 2000 -S 1000 --steplength=1 --distthresh=0.05 --cthr=0.1 --fibthresh=0 --randfib=1 --sampvox=5 --verbose=1 --xfm=str2dif_warp.nii.gz --invxfm=dif2str_warp.nii.gz --seedref=str.nii.gz --meshspace=freesurfer --opd --pd --usef --loopcheck --modeuler --os2t --s2tastext --targetmasks=targets.txt --omatrix1'
    assert good_custom == custom
