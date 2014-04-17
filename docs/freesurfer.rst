Freesurfer
==========

`Freesurfer <http://surfer.nmr.mgh.harvard.edu>`_ is a set of software
tools for the study of cortical and subcortical anatomy. In the cortical
surface stream, the tools construct models of the boundary between
white matter and cortical gray matter as well as the pial surface.
Once these surfaces are known, an array of anatomical measures becomes
possible, including: cortical thickness, surface area, curvature, and
surface normal at each point on the cortex. The surfaces can be
inflated and/or flattened for improved visualization. The surfaces can
also be used to constrain the solutions to inverse optical, EEG and MEG
problems. In addition, a cortical surface-based atlas has been defined
based on average folding patterns mapped to a sphere. Surfaces from
individuals can be aligned with this atlas with a high-dimensional
nonlinear registration algorithm. The registration is based on aligning
the cortical folding patterns and so directly aligns the anatomy instead
of image intensities. The spherical atlas naturally forms a coordinate
system in which point-to-point correspondence between subjects can be
achieved. This coordinate system can then be used to create group maps
(similar to how Talairach space is used for volumetric measurements).

Most of the FreeSurfer pipeline is automated, which makes it ideal
for use on large data sets.

Recipes
+++++++

.. autofunction:: seam.freesurfer.v1.recipe.build_recipe

Functions
+++++++++

These are lower-level functions to be used when more customization is needed than
provided by the above recipes.

.. autofunction:: seam.freesurfer.v1.core.recon_input
.. autofunction:: seam.freesurfer.v1.core.recon_all
.. autofunction:: seam.freesurfer.v1.core.tkmedit_screenshot_tcl
.. autofunction:: seam.freesurfer.v1.core.tkmedit_screenshot_cmd
.. autofunction:: seam.freesurfer.v1.core.tksurfer_screenshot_tcl
.. autofunction:: seam.freesurfer.v1.core.tksurfer_screenshot_cmd
.. autofunction:: seam.freesurfer.v1.core.annot2label_cmd

**Versions**:

.. automodule:: seam.freesurfer.v1