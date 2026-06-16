**********************
Day 1: Installing MESA
**********************

The following set of instructions are specific to CASSI 2026, where a Mac laptop is provided, 
and Carnegie's Observatories High-Performance Computing (OBS HPC) are available. 

1. Prerequisites for MESA SDK
=============================

The MESA SDK (documentation `here <https://docs.mesastar.org/en/latest/installation.html#install-the-mesa-sdk>`_) 
provides a set of compilers and libraries for running MESA. 
Before installing the MESA SDK, you would need to install a set of prerequisites. 


If you are on a MAC, you would first need to install Xcode. On your terminal, 

.. code:: bash

   xcode-select --install

You would also need to install Xquartz from `here <https://www.xquartz.org/>`_. 

.. note::

    If you are on OBS HPC, I believe the prerequisites for installing the MESA SDK are 
    satisfied. Otherwise, following Rich Townsend's `instructions <http://user.astro.wisc.edu/~townsend/static.php?ref=mesasdk>`_. 

2. Installing MESA SDK
=======================

Now you're ready to install the MESA SDK. 

First, go to Rich Townsend's `website <http://user.astro.wisc.edu/~townsend/static.php?ref=mesasdk>`_.

Next, go to the operating system corresponding to your machine (MAC OS or Linux), 
and download the MESA SDK. 

.. note::

    If you have OBS HPC, after downloading the MESA SDK, you need to unpack the file. 
    On your terminal, do:

    .. code:: bash

        tar xvfz package_name -C ~/

If everything goes well, on your terminal:

.. code:: bash

    open -e ~/.bash_profile

This will open up the `.bash_profile`, which is a configuration script 
that is executed automatically everytime you open a terminal. 

Now, let's add the following lines to your `.bash_profile`:

.. code:: bash

    export MESASDK_ROOT=/Applications/mesasdk
    source $MESASDK_ROOT/bin/mesasdk_init.sh

.. note::

    If you have an Ubuntu machine, like on OBS HPC, open up your `.bash_profile` by

    .. code:: bash

        gedit ~/.bash_profile

    Then add: 

    .. code:: bash

        export MESASDK_ROOT=~/mesasdk
        source $MESASDK_ROOT/bin/mesasdk_init.sh

    to your `.bash_profile`. 

If all goes well, open up a new terminal, or refresh the instructions on your terminal:

.. code:: bash
    
    source ~/.bash_profile

you should be able to check whether the installation 
went well by running on your terminal:

.. code:: bash

    gfortran --version

You should get something like:

.. code:: bash

    GNU Fortran (GCC) 15.2.0


3. Installing MESA
===================


