#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" core.py

FSL core functions
"""
__author__ = 'Scott Burns <scott.s.burns@vanderbilt.edu>'
__copyright__ = 'Copyright 2014 Vanderbilt University. All Rights Reserved'

def flirt(input, ref, omat=None, out=None, inter='spline', flags=None):
    """Return FSL's Linear Image Registration Tool command

    :param str input: input image (jiggled to reference)
    :param str ref: reference image (stationary)
    :param str omat: path to affine xfm output
    :param str out: path to xfm'd out image
    :param list flags: other flags to pass to flirt
    :note: at least one of *omat* or *out* must be passed

    Usage::

     >>> flirt(input='/path/to/input.nii',
     ... ref='/path/to/ref.nii',
     ... omat='/path/to/in2ref.mat',
     ... out='/path/to/in_ref_flirt.nii.gz',
     ... flags=['-dof 12'])
     'flirt -in /path/to/input.nii -ref /path/to/ref.nii -omat /path/to/in2ref.mat -out /path/to/in_ref_flirt.nii.gz -inter spline -dof 12'
    """
    def_flags = ['-inter {inter}']
    if not (omat or out): # need at least one output
        msg = "flirt requires at least one output (omat or out)"
        raise ValueError(msg)
    parts = ['flirt', '-in {input}', '-ref {ref}']
    if omat: parts.append('-omat {omat}')
    if out: parts.append('-out {out}')
    parts.extend(def_flags)
    if flags: parts.extend(flags)
    return ' '.join(parts).format(**locals())


def fnirt(input, ref, cout=None, iout=None, aff=None, flags=None):
    """Return FSL's Nonlinear Image Registration Tool command

    :param str input: input image (jiggled to reference)
    :param str ref: reference image (stationary)
    :param str cout: path to output warp coefficient image
    :param str iout: path to output registered image
    :param list flags: other flags to pass to fnirt
    :param str aff: path to affine matrix (from flirt)
    :note: at least one of *cout* or *iout* must be passed

    Usage::

     >>> fnirt(input='/path/to/input.nii',
     ... ref='/path/to/ref.nii',
     ... cout='/path/to/in2ref_warp.nii.gz',
     ... iout='/path/to/in_ref_fnirt.nii.gz',
     ... flags=['--config=T1_2_MNI152_2mm.cnf'])
     'fnirt --in=/path/to/input.nii --ref=/path/to/ref.nii --cout=/path/to/in2ref_warp.nii.gz --iout=/path/to/in_ref_fnirt.nii.gz --config=T1_2_MNI152_2mm.cnf'
    """
    if not (cout or iout): # we need at least one output
        msg = 'fnirt requires at least one output argument (cout or iout)'
        raise ValueError(msg)
    parts = ['fnirt', '--in={input}', '--ref={ref}']
    if cout: parts.append('--cout={cout}')
    if iout: parts.append('--iout={iout}')
    if aff: parts.append('--aff={aff}')
    if flags: parts.extend(flags)
    return ' '.join(parts).format(**locals())


def invwarp(warp, ref, out, flags=None):
    """Return FSL's invwarp command

    :param str warp: warp file to invert
    :param str ref: reference image, what was originally input to FNIRT
    :param str output: output path to inverted warp
    :param list flags: additional flags to pass to invwarp

    Usage::

     >>> invwarp(warp='t12mni_warp.nii.gz', ref='t1.nii.gz', out='mni2t1_warp.nii.gz')
     'invwarp -w t12mni_warp.nii.gz -r t1.nii.gz -o mni2t1_warp.nii.gz'
    """
    parts = ['invwarp', '-w {warp}', '-r {ref}', '-o {out}']
    if flags: parts.extend(flags)
    return ' '.join(parts).format(**locals())

def applywarp(input, warp, ref, out, super=True, superlevel='a',
        interp='spline', flags=None):
    """Return FSL's applywarp command

    :param str input: path to input image
    :param str ref: reference image (output will have properties of this image)
    :param str out: output image with warp applied
    :param str warp: path to warp field
    :param bool super: use intermediary supersampling
    :param str/int superlevel: level of intermediate supersampling,
      'a' for auto or integer
    :param str interp: type of output interpolation (nn, trilinear, sinc, spline)
    :param list flags: other flags to pass to applywarp

    Usage::

     >>> applywarp(input='mni.nii', ref='t1.nii', out='mni_t1.nii',
     ... warp='mni2t1_warp.nii')
     'applywarp -i mni.nii -r t1.nii -o mni_t1.nii -w mni2t1_warp.nii --interp=spline -s --superlevel=a'
    """
    allowed_interps = ('nn', 'trilinear', 'sinc', 'spline')
    if interp not in allowed_interps:
        msg = 'interp param must be in {}'.format(' '.join(allowed_interps))
        raise ValueError(msg)
    def_flags = ['--interp={interp}',]
    if super: def_flags.extend(['-s', '--superlevel={superlevel}'])
    parts = ['applywarp', '-i {input}', '-o {out}', '-r {ref}', '-w {warp}']
    parts.extend(def_flags)
    if flags: parts.extend(flags)
    return ' '.join(parts).format(**locals())

def convert_xfm(omat, inverse=None, concat=None, fixscaleskew=None):
    """Return FSL's convert_xfm command

    :param str omat: output matrix path
    :param str inverse: path to matrix to invert
    :param list concat: [BtoC, AtoB]
    :param str fixscaleskew: second matrix filename to help fix

    Usage::

     >>> convert_xfm(omat='mni2t1.mat', inverse='t12mni.mat')
     'convert_xfm -omat mni2t1.mat -inverse t12mni.mat'
     >>> convert_xfm(omat='a2c.mat', concat=('b2c.mat', 'a2b.mat'))
     'convert_xfm -omat a2c.mat -concat b2c.mat a2b.mat'
    """
    if (inverse is None) + (concat is None) != 1:
        msg = "Must pass either inverse or concat but not both"
        raise ValueError(msg)
    parts = ['convert_xfm', '-omat {omat}']
    if inverse:
        parts.append('-inverse {inverse}')
    else:
        parts.append('-concat {} {}'.format(*concat))
    if fixscaleskew: parts.append('-fixscaleskew {fixscaleskew}')
    return ' '.join(parts).format(**locals())
