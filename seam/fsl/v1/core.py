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

     >>> flirt(input='input.nii',
     ... ref='ref.nii',
     ... omat='in2ref.mat',
     ... out='in_ref_flirt.nii.gz',
     ... flags=['-dof 12'])
     'flirt -in input.nii -ref ref.nii -omat in2ref.mat -out in_ref_flirt.nii.gz -inter spline -dof 12'
    """
    def_flags = ['-inter {inter}']
    if not (omat or out):  # need at least one output
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
    if not (cout or iout):  # we need at least one output
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
    def_flags = ['--interp={interp}']
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


def bet(input, output, frac=.5, mask=False, flags=None):
    """Return FSL's Brain Extraction Tool command

    :param str input: input root
    :param str output: output root
    :param float frac: fractional intensity threshold
    :param bool mask: generate brain mask
    :param list flags: other arguments to bet

    Usage ::

     >>> bet('T1', 'T1_brain', frac=.25, mask=True)
     'bet T1 T1_brain -f 0.25 -m'
     >>> bet('T1', 'T1_brain', frac=.25, mask=True, flags=['-R', '-e'])
     'bet T1 T1_brain -f 0.25 -m -R -e'
    """
    parts = ['bet', '{input}', '{output}', '-f {frac:g}']
    if mask: parts.append('-m')
    if flags: parts.extend(flags)
    return ' '.join(parts).format(**locals())


def probtrackx2(samples, mask, seed, out='fdt_paths', directory='logdir',
                nsamples=5000, nsteps=2000, steplength=0.5, distthresh=0,
                cthr=0.2, fibthresh=0.01, randfib=0, sampvox=0, verbose=0,
                xfm=None, invxfm=None, seedref=None, meshspace='caret',
                opd=True, pd=False, usef=False, loopcheck=False,
                modeuler=False, os2t=True, s2tastext=True, flags=None):
    """Return FSL's probtrackx2 command

    This makes a pretty explicit ``probtrackx2`` command. We believe this
    explicitness is good.

    :param str samples: basename for samples files, e.g. ``merged``
    :param str mask: path to binary mask in diffusion space
    :param str seed: path to volume/surfaces or text file of seeds
    :param str out: output file name ('fdt_paths')
    :param str directory: output directory ('logdir')
    :param int nsamples: number of streamlines per input voxel (5000)
    :param int nsteps: maximum steps per streamline (2000)
    :param float steplength: steplength in mm (0.5)
    :param float distthresh: discard samples shorter than this threshold (0)
    :param float cthr: curvature threshold (0.2)
    :param float fibthresh: Volume fraction before considering other fiber orientations (0.01)
    :param int randfib: (0). 1 to randomly sample initial fibres (with f > fibthresh)
      2 to sample in proportion fibres (with f>fibthresh) to f
      3 to sample ALL populations at random (even if f<fibthresh)
    :param int sampvox: Sample random points within x mm spehere of seed voxel (0)
    :param int verbose: Verbosity level (0), 1, 2
    :param str xfm: path to seed to diffusion transform. If None, assume identity
    :param str invxfm: path to diffusion to seed warp. Must pass if ``xfm`` is warpfield
    :param str seedref: path to seed reference image
    :param str meshspace: mesh reference space ('caret'), 'freesurfer', 'first', 'voxel'
    :param bool opd: output path distributions (True)
    :param bool pd: correct path distribution for length of pathways (False)
    :param bool usef: use fractional anisotropy to constrain tracking (False)
    :param bool loopcheck: perform loopchecks on paths (False)
    :param bool modeuler: Use modified Euler streamlining (False)
    :param bool os2t: output seeds to target (True)
    :param bool s2tastext: output seed-to-target counts as text file (True)
    :param list flags: other flags to pass to ``probtrackx2``

    :note: ``probtrackx2`` has a LOT of flags. I've tried to capture the
      the flags related to the probtracking itself. You're on your own for
      matrix flags.

    Usage::

     >>> probtrackx2('bedpostx/merged', 'nodif_brain_mask', 'cc.nii.gz')
     'probtrackx2 -s bedpostx/merged -m nodif_brain_mask -x cc.nii.gz -o fdt_paths --dir=logdir --opd -P 5000 -S 2000 --steplength=0.5 --distthresh=0 -c 0.2 --fibthresh=0.01 --randib=0 --sampvox=0'
    """
    assert meshspace in ('caret', 'freesurfer', 'first', 'voxel')
    parts = ['probtrackx2', '-s {samples}', '-m {mask}', '-x {seed}',
             '-o {out}', '--dir={directory}', '--forcedir', '-P {nsamples:d}',
             '-S {nsteps:d}', '--steplength={steplength:g}',
             '--distthresh={distthresh:g}', '--cthr={cthr:g}',
             '--fibthresh={fibthresh:g}', '--randfib={randfib:d}',
             '--sampvox={sampvox:d}', '--verbose={verbose:d}', ]
    if xfm: parts.append('--xfm={xfm}')
    if invxfm: parts.append('--invxfm={invxfm}')
    if seedref: parts.append('--seedref={seedref}')
    if meshspace: parts.append('--meshspace={meshspace}')
    if opd: parts.append('--opd')
    if pd: parts.append('--pd')
    if usef: parts.append('--usef')
    if loopcheck: parts.append('--loopcheck')
    if modeuler: parts.append('--modeuler')
    if os2t: parts.append('--os2t')
    if s2tastext: parts.append('--s2tastext')
    if flags: parts.extend(flags)
    return ' '.join(parts).format(**locals())
