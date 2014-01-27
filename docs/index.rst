.. seam documentation master file, created by
   sphinx-quickstart on Mon Jan 27 13:49:39 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Seam
====

Seam is a simple layer between neuroimaging tools and your data. It makes no decisions about how to organize your data or execute data analyses. It simply provides commands to intelligently call standard neuroimaging tools.

It's designed to be extremely easy to use:

    from seam.freesurfer import recon_all
    recon_all_command = recon_all(subject='sub0001', input='/path/to/data.nii')
    with open('script.sh', 'w') as f:
        f.write(recon_all_command)

Philosophy
----------

Software is best written in layers. Each layer should encapsulate knowledge about how to best use the next lower layer. Its functionality should be exposed through as simple an API as possible.

Seam extends this rationale to neuroimaging data analysis. It is up to you to organize your data and run analyses, but seam will generate commands for you to apply your data against standard neuroimaging tools.

Seam will have no dependencies and minimal effort will be required to use it. It should integrate into any application ranging from a single script to something much more complicated.

Installation
------------

Install seam by running:

    $ pip install seam

It has no dependencies.

Contribute
----------

- Issue Tracker: github.com/VUIIS/seam/issues
- Source Code: github.com/VUIIS/seam

Support
-------

If you are having issues, please raise an issue on Github.

License
-------

The project is licensed under the MIT license.


Contents:

.. toctree::
   :maxdepth: 2


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

