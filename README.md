seam
====

Seam is a simple layer between standard neuroimaging tools and your data. It generates useful commands around these tools so you can apply them against your data.

Documentation
-------------

The [official documentation][2].

Initial planned support
-----------------------

- Freesurfer's `recon-all` and `trac-all` commands with helper functions for taking `tksurfer` & `tkmedit` screenshots, etc.
- FSL's `dtifit`, `bedpost` & `probtrackx2`.
- Others as contributed or determined useful

Philosophy
----------

Software is best written in layers. Each layer should encapsulate knowledge about how to best use the next lower layer. Its functionality should be exposed through as simple an API as possible.

Seam will have no dependencies and minimal effort will be required to use it. It should integrate into any application ranging from a single script to something much more complicated.

Seam makes no decisions about the organization of your data or how the generated commands will ultimately be executed. That is up to you as the scientist & engineer.

A simple example
----------------

```python
from seam.freesurfer import recon_all

subject_data = {'sub001': '/path/to/first/t1.nii',
                'sub002': '/path/to/other/t1.nii',
                'sub003': '/path/to/third/t1.nii'}

for subject_id, path_to_t1 in subject_data.iteritems():
    recon_command = recon_all(subject=subject_id, input=path_to_t1)
    script_name = 'recon_{}.sh'.format(subject_id)
    with open(script_name, 'w') as f:
        f.write(recon_command)
```

The generated `recon_all` commands will be the exact three for each subject,  though obviously with different inputs.


Support/Questions/Development
-----------------------------

Seam is very much a work-in-progress. It is supported through [the Vanderbilt Univeristy Institute for Imaging Science][1]. Please use github for questions and issues but I cannot guarantee support.

[1]:    http://vuiis.vanderbilt.edu
[2]:    http://seam.rtfd.org