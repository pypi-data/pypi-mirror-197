leukeleu-thumbor-multidir
=========================

Thumbor file loader that checks multiple paths

Introduction
------------

[Thumbor](https://github.com/globocom/thumbor/wiki) is a smart imaging service. 
It enables on-demand crop, resizing and flipping of images.

By default, the Thumbor file loader only loads images from a single path. 
Using this loader, multiple paths can be specified. The first path that contains 
the requrest image is then used.

Usage
-----

To enable this loader, add the following to `thumbor.conf`:

    LOADER = 'tc_multidir.loader'

Then, configure the paths to check for the image:

    # List of paths to check for file to load (required)
    TC_MULTIDIR_PATHS = ['/home/media', '/mnt/media']
