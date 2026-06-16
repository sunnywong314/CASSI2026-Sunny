**********************
Day 2: First MESA run
**********************

Having installed MESA, we're now ready to make our first MESA run. 

A lot of this material is taken from Josiah Schwab's MESA summer school 
`lectures <https://jschwab.github.io/mesa-2021/>`_. 

1. First run
================

We will start from a clean MESA work directory, and gradually modify it:

.. code:: 

    cp -r $MESA_DIR/star/work <path>/first_run

where we name our new work directory `first_run`.

Now go to `first_run`:

.. code::

    cd <path>/first_run

Clean and compile it:

.. code::

    ./clean 
    ./mk

The ``./clean`` executable clears any previous compiled code, and the ``./mk`` executable 
compiles the Fortran code (translates the Fortran source code into machine readable code 
and links all necessary libraries into a single executable). 



If all goes well, you're ready to do your first MESA run by 

.. code::

    ./rn


2. Opening Inlist
========================

When MESA starts, it will look for an ``inlist``, which is a Fortran namelist 
containing all the runtime parameters that you want to change from their 
default values. 

Let's take a look at ``inlist`` in your work directory. 

.. code::

    less -S inlist

will open up the contents of ``inlist`` on your terminal. And you should see

.. code-block:: fortran

    ! This is the first inlist file that MESA reads when it starts.

    ! This file tells MESA to go look elsewhere for its configuration
    ! info. This makes changing between different inlists easier, by
    ! allowing you to easily change the name of the file that gets read.

    &star_job

    read_extra_star_job_inlist(1) = .true.
    extra_star_job_inlist_name(1) = 'inlist_project'

    / ! end of star_job namelist


    &eos

    read_extra_eos_inlist(1) = .true.
    extra_eos_inlist_name(1) = 'inlist_project'

    / ! end of eos namelist


    &kap

    read_extra_kap_inlist(1) = .true.
    extra_kap_inlist_name(1) = 'inlist_project'

    / ! end of kap namelist


    &controls

    read_extra_controls_inlist(1) = .true.
    extra_controls_inlist_name(1) = 'inlist_project'

    / ! end of controls namelist


    &pgstar

    read_extra_pgstar_inlist(1) = .true.
    extra_pgstar_inlist_name(1) = 'inlist_pgstar'

    / ! end of pgstar namelist

3. Understanding Inlists
========================

You'll notice that there are 5 different blocks in ``inlist``:

.. hlist::
    :columns: 1

    * ``star_job``: options for the program that evolves the star
    * ``eos``: options for the MESA eos module
    * ``kap``: options for the MESA kap module
    * ``controls``: options for the MESA star module
    * ``pgstar``: options for on-screen plotting

star_job
--------

contains options that answer questions like:

.. hlist::
    :columns: 1 

    * how should MESA obtain the initial model?
    * are there any changes MESA should make to the initial model?
    * what additional equations or boundary conditions should MESA solve? 

See the documentation `here <https://docs.mesastar.org/en/26.4.1/reference/star_job.html>`_. 

controls
--------

contains options that answer questions like:

.. hlist::
    :columns: 1 

    * what physics, e.g., convection, or angular momentum transport, and their related parameters, 
    should MESA consider? 
    * what numerical tolerances should MESA's solvers use?
    * when should MESA stop evolving the model?

See the documentation `here <https://docs.mesastar.org/en/26.4.1/reference/controls.html>`_. 

eos
---

EOS stands for equation of state. It is relates thermodynamic quantities, e.g., density 
and temperature to gas pressure, sound speed, and so on. 

The MESA EOS is made of several component EOSes. Each has its different physical assumptions 
that may be more valid in different parameter spaces. The ``eos`` inlist section contains options 
that answer questions like:

.. hlist::
    :columns: 1 

    * what component EOSes should be used and where should they be blended?

See the documentation `here <https://docs.mesastar.org/en/26.4.1/reference/eos.html>`_. 

kap
---

kap stands for :math:`\kappa` (kappa), which is the opacity. It dictates how quickly heat is transported 
out of the star through radiation or electron conduction, and whether convection happens. 

The MESA opacity is made of several component opacity tables. 
The ``kap`` inlist section contains options that answer questions like:

.. hlist::
    :columns: 1 

    * what composition should be assumed when calculating the opacity?

See the documentation `here <https://docs.mesastar.org/en/26.4.1/reference/kap.html>`_. 










