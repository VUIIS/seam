FSL
===

FSL is a set of scripts and compiled tools for image processing from the `FMRIB Group <http://www.fmrib.ox.ac.uk>`_ at Oxford. They are widely used in structural, functional & diffusion MR image analysis.

Recipes
+++++++

None yet :(

Functions
+++++++++

Low-level functions to build FSL commands.

Registration-related
--------------------

.. autofunction:: seam.fsl.v1.core.flirt
.. autofunction:: seam.fsl.v1.core.fnirt
.. autofunction:: seam.fsl.v1.core.invwarp
.. autofunction:: seam.fsl.v1.core.applywarp
.. autofunction:: seam.fsl.v1.core.convert_xfm

Structural Tools
----------------

.. autofunction:: seam.fsl.v1.core.bet

Diffusion Imaging Tools
-----------------------

.. autofunction:: seam.fsl.v1.core.probtrackx2
