WAPT Packages
====

WAPT Packages repository provides recipes of WAPT packages that can be used to build up 
WAPT Packages. It does not host binaries, msi, exe, etc.

WAPT is a software deployment tool whose core set of features is licensed under the GPLv3.

The recipes in this repository are also licensed under the GPLv3. The softwares that are to be 
downloaded to make a proper package are not part of this repository and are licensed under 
their own license.

* Official WAPT Site : https://wapt.fr/
* WAPT Documentation : https://wapt.fr/en/doc-1.5
* Official WAPT git repo : https://github.com/tranquilit/WAPT
* Mailing list : https://list.tranquil.it/listinfo/wapt/
* Forum : https://forum.tranquil.it


Recommendations
===============

Binaries should not be uploaded to this repository. 

In order to build a package, the writer of the recipe has to write a `def update_source()` method
in the `setup.py` file

For more information how to write a ``update_source()` method, please refer to the official 
documentation.