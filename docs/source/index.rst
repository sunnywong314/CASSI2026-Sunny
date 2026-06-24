.. CASSI-2026 documentation master file, created by
   sphinx-quickstart on Mon Jun 15 16:27:18 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

CASSI-2026 documentation
========================

These notes document some exercises that I provide to my CASSI 2026 student, for running MESA and 
understanding stellar evolution. The formatting is taken from Mike Zingale's MESA summer school 2026 
lectures. 

These notes are a collection of Jupyter notebooks.  You can download
them and work through them on your own laptop or run them in the cloud
(e.g., with Google Colab):

Working on your own computer
============================

Clicking on the :octicon:`download` icon in the upper right let's you
download the raw notebook so you can run it on your local computer.

You'll need to install `mesa_reader <https://github.com/wmwolf/py_mesa_reader>`_.
This can be done via pip as:

.. code:: bash

   pip install mesa_reader

Using Google Colab
==================

Clicking on the :octicon:`rocket` icon in the upper right (on pages that are notebooks) will allow
launch the notebook directly in the cloud.

As with the local install, you'll need mesa_reader.  These
can be installed from within Colab by executing

.. code:: bash

   !pip install mesa_reader

(note the ``!``) in a cell.

Some of the notebooks need data files.  These can be uploaded by selecting the
:octicon:`file-directory` icon on the vertical menu bar on the left.


.. toctree::
   :maxdepth: 3
   :caption: Week 1:

   installing
   first_run

.. toctree::
   :maxdepth: 3
   :caption: Week 2:

   first_run_nb.ipynb
   first_run_nb2.ipynb
   second_run

.. toctree::
   :maxdepth: 2
   :caption: Useful:

   commands
   fortran_basics

