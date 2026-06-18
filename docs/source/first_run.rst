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

.. dropdown:: Click to expand

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

    * what physics, e.g., convection, or angular momentum transport, and their related parameters, should MESA consider? 
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

kap stands for :math:`\kappa` (kappa), which is the opacity. 
A higher opacity means that the material is more opaque, so that it takes longer 
for heat to get transported out. 

The MESA opacity is made of several component opacity tables. 
The ``kap`` inlist section contains options that answer questions like:

.. hlist::
    :columns: 1 

    * what composition should be assumed when calculating the opacity?

See the documentation `here <https://docs.mesastar.org/en/26.4.1/reference/kap.html>`_. 

4. Changing Inlists
========================

Now we're ready to change our inlists. 

You'll notice that in ``inlist`` of your current work directory, it actually points 
to other inlists. The ``star_job``, ``controls``, ``kap`` and ``eos`` sections point to 
``inlist_project``, whereas the ``pgstar`` section points to ``inlist_pgstar``, via e.g., 

.. code-block:: fortran

    &star_job

    read_extra_star_job_inlist(1) = .true.
    extra_star_job_inlist_name(1) = 'inlist_project'

    / ! end of star_job namelist

Now let's edit ``inlist_project``. 

This MESA run evolves a star from the pre-main sequence to the start of the 
main sequence. This is achieved with the ``star_job`` option 
``create_pre_main_sequence_model = .true.``. 

Next, change the following runtime parameters:

* Change the initial mass of the model to :math:`1 M_{\odot}`. 
* Change the stopping conditions so that the model does not stop at the zero age main sequence (ZAMS), but instead when the central hydrogen mass fraction drops below 1e-5. 

.. dropdown:: Hint (Click to expand)
   
   The initial mass of the model (when creating a pre-main sequence model) and stopping conditions are both in the ``controls`` section of an inlist. The documentation is `here <https://docs.mesastar.org/en/26.4.1/reference/controls.html>`_.

.. dropdown:: Partial solution (Click to expand)
   
   In the ``controls`` section of ``inlist_project``, set

   .. code-block:: fortran

        initial_mass = 1d0

        stop_near_zams = .false.

        xa_central_lower_limit_species(1) = 'h1'
        xa_central_lower_limit(1) = 1d-5

In the ``pgstar`` section of ``inlist_pgstar``, set 

.. code-block:: fortran

    HR_logT_min = 3.5
    HR_logT_max = 4.0
    HR_logL_min = -1.0
    HR_logL_max = 3.0

This adjusts the x and y-axis limits on the HR diagram. 

Now run the model again:

.. code-block:: bash

    ./rn

5. On-screen Plotting
======================

As the model is running, let's add some more things. 
MESA's ``pgstar`` is a super useful plotting tool, and allows you to see what the 
model is doing in real time. 

We can add some more useful plots. In your ``inlist_pgstar``, add the following:

.. code-block:: fortran

    abundance_win_flag = .true.

This opens up a new pgstar window, that shows the mass fractions of different isotopes within the star. 

After running for a while, let's kill the run by doing ``ctrl+c`` on the terminal. 

6. Changing pgstar and history_colunns
======================================

Now we'll try to combine the different pgstar plots into one, and also change the output quantities 
from MESA. 

First, edit your ``inlist_pgstar``, and set 

.. code-block:: fortran

    HR_win_flag = .false.

    TRho_Profile_win_flag = .false.

    abundance_win_flag = .false.

    grid2_win_flag = .true.

The first three options turn off the HR diagram plot, the TRho profile plot, and the 
abundance plot. The last option instead turn on a new plot called grid2, and you'll see 
that it combines several different plots into one single grid. 

Next, edit your ``inlist_project``, and set ``disable_pgstar_during_relax_flag = .false.`` 
in the ``&star_job`` section. This turns on the pgstar plot in the beginning, while MESA is 
'relaxing' the model. 

If you do ``./rn`` now, you'll get the error message:

.. code-block:: bash

    ERROR: failed to find log_center_Rho in history data

    ERROR: failed to find log_center_T in history data

This error message occurs because the ``grid2`` plot tries to grab the values of 
``log_center_Rho`` and ``log_center_T``, but isn't able to find them in MESA's history file. 

To change what MESA outputs in its history file, we need to do the following:

.. code-block:: bash

    cp $MESA_DIR/star/defaults/history_columns.list .

Then edit this file:

.. code-block:: bash

    open -e history_columns.list

and uncomment the lines (do a ``cmd+F`` to search for these two terms, and remove the ``!`` to uncomment):

.. code-block:: fortran

    log_center_T
    log_center_Rho

You can also uncomment other items to have MESA output these quantities. We'll get to this in the future. 

Now if you run again (``./rn``), you should be able to run MESA smoothly and see a new 
plot that combines the abundance, TRho profile, and HR diagram plots. 

7. Stellar Evolution I
======================

While the model is running, observe the pgstar plot and answer the following:

* How does the star move on the HR diagram during the pre-main sequence evolution? 
* How does its central density and temperature change during the pre-main sequence evolution, and on the main sequence, respectively? 
* On the main sequence, how do the central abundances change? Pay particular attention to H, He, C, N and O. 





