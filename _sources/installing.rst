**********************
Day 1: Installing MESA
**********************

The following set of instructions are specific to CASSI 2026, where a Mac laptop is provided, 
and Carnegie's Observatories High-Performance Computing (OBS HPC) are available. A more 
complete set of instructions are available on the MESA  
`documentation <https://docs.mesastar.org/en/latest/installation.html#installing-mesa>`_. 

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

    open -e ~/.zprofile

This will open up the `.zprofile`, which is a configuration script 
that is executed automatically everytime you open a terminal. 

.. note::

    If you have an Ubuntu system (like on OBS HPC), use the `.bash_profile` instead.

Now, let's add the following lines to your `.zprofile`:

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
    
    source ~/.zprofile

or `.bash_profile` if you have an Ubuntu system. 

You should be able to check whether the installation 
went well by running on your terminal:

.. code:: bash

    gfortran --version

You should get something like:

.. code:: bash

    GNU Fortran (GCC) 15.2.0


3. Installing MESA
===================

Now you are ready to download and install MESA. 

Go to `Zenodo <https://zenodo.org/records/19722306>`_, and download the MESA source code. 

Next, unzip the file:

.. code:: bash

    unzip mesa-26.04.1.zip

Now note where you put your MESA directory. You may also move your MESA directory using 
the `mv` command. I'll call this `<path>`. 

Edit your `.zprofile` or `.bash_profile` (e.g., `open -e ~/.zprofile` or 
`gedit ~/.bash_profile`) to add the following:

.. code:: bash

    export MESA_DIR=<path>
    export OMP_NUM_THREADS=2

where `OMP_NUM_THREADS` should be the number of threads on your machine. 

Then either update your terminal with 

.. code:: bash

    source ~/.zprofile

(or `source ~/.bash_profile`), or open a new terminal. 

If you did this correctly, you should be able to change directory into the MESA directory via 

.. code:: bash

    cd $MESA_DIR

After you go to `$MESA_DIR` via the above command, you should be able to start installing MESA:

.. code:: bash

    ./install

If all goes well, you should see the following:

.. code:: bash

    ************************************************
    ************************************************
    ************************************************

    MESA installation was successful

    ************************************************
    ************************************************
    ************************************************



