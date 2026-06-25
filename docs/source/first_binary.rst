************************
Day 6: First Binary Run
************************

Congrats on making it this far! 
Now we will take it further, and learn about binary runs in MESA. 

1. Getting started
==================

Much like MESA `star`, in `binary` we start with a clean work directory. 
Let's call it ``first_binary``

.. code-block:: bash

    cp -r $MESA_DIR/binary/work <path>/first_binary

|

If you change directory into this, and list all the items:

.. code-block:: bash

    cd <path>/first_binary

    ls 

You should see:

.. code-block:: bash

    clean          inlist_project inlist2        mk             rn
    inlist         inlist1        make           re             src

This is a very similar structure to the MESA `star` work directory -- 
you see several inlists, the `src` directory, and some executables like `clean`, `mk`, and `rn`. 

2. Understanding binary inlist
===============================

Using a text editor, open ``inlist``, you will see:

.. dropdown:: Click to expand

    .. code-block:: fortran

        &binary_job

        read_extra_binary_job_inlist(1) = .true.
        extra_binary_job_inlist_name(1) = 'inlist_project'

        / ! end of binary_job namelist


        &binary_controls

        read_extra_binary_controls_inlist(1) = .true.
        extra_binary_controls_inlist_name(1) = 'inlist_project'

        / ! end of binary_controls namelist


        &pgbinary

        read_extra_pgbinary_inlist(1) = .true.
        extra_pgbinary_inlist_name(1) = 'inlist_project'

        / ! end of pgbinary namelist

The structure is very similar to MESA `star` inlist. 
This points to ``inlist_project``, so let's open it with a text editor:

.. dropdown:: Click to expand

    .. code-block:: fortran

        &binary_job

        inlist_names(1) = 'inlist1' 
        inlist_names(2) = 'inlist2'

        evolve_both_stars = .false.

        / ! end of binary_job namelist

        &binary_controls

        m1 = 1.0d0 ! donor mass in Msun
        m2 = 1.4d0 ! companion mass in Msun
        initial_period_in_days = 2d0

        ! transfer efficiency controls
        limit_retention_by_mdot_edd = .true.

        max_tries_to_achieve = 20

        / ! end of binary_controls namelist


In a binary inlist, there are three sections:

- ``binary_job``: This allows modifications to the initial binary model, and interacts with the MESA `star` module. 
- ``binary_controls``: This sets some specifications for the starting binary model, outputs, timestep controls, when to stop, and implements some binary physics like mass loss and angular momentum loss from the system. 
- ``pgbinary``: This allows plotting for binary runs. We won't be using this much. 

binary_job
___________

contains options that answer questions like:

- Should MESA evolve the stellar structure of both stars? (e.g., ``evolve_both_stars = .true.``)
- When MESA evolves the stellar structure of star 1 (and sometimes star 2), where does MESA find the inlists for the `star` module? (``inlist_names(1) = 'inlist1'``)
- Should MESA make any modifications to the binary model? (we won't be using these at all)

.. note:: 

    Take a look at ``inlist1`` and ``inlist2``. These should look like a normal MESA `star` inlist, 
    containing some of the usual `star_job`, `kap`, `eos`, `controls`, `pgstar` sections. 
    
    Essentially, the `binary` inlist (in this case, ``inlist`` and ``inlist_project``) tells MESA 
    how to evolve the binary, the `star` inlist(s) tells MESA how to evolve the individual stars 
    of the binary (in this case, ``inlist1`` for star 1, and ``inlist2`` for star 2). 

See the `binary_job <https://docs.mesastar.org/en/26.4.1/reference/binary_job.html>`_ documentation. 

binary_controls
________________

contains options that answer questions like:

- Specifications for the starting model, like initial component masses and orbital period. 
- What binary physics should MESA consider? For example, how should MESA calculate the mass transfer rate, and should any mass be lost from the system? 

See the `binary_controls <https://docs.mesastar.org/en/26.4.1/reference/binary_controls.html>`_ documentation. 


3. First run
=============

Before we do the first run, let's make some edits to make the pgstar plot look better. 

.. admonition:: Task

    - Copy ``history_columns.list`` from the `star` module into your work directory, and uncomment the items ``log_center_T`` and ``log_center_Rho``.
    
    - In ``inlist1``, replace the entire content of the `pgstar` section with the following:

        .. code-block:: fortran

            read_extra_pgstar_inlist(1) = .true.
            extra_pgstar_inlist_name(1) = 'inlist_pgstar'

    - Download ``inlist_pgstar`` from :download:`here <first_binary/inlist_pgstar>` to your working directory. 

    Having done all of the above, you are ready to clean, mk and rn. 

During the run, you will see the usual grid2 pgstar window, but now it has 
some additional plots specifically for the binary. 

.. admonition:: Task

    Observe:

    - How does the orbital period change? 
    - When does the star start transferring mass? On the main sequence, or post-main sequence?
    - What is the peak mass transfer rate?
    - As the star loses mass, what happens to nuclear burning?

The run will take quite a while. Feel free to kill the run using ``ctrl+c`` 
once the model number goes beyond 2000. 

|

Let's also do some python plotting. 

.. admonition:: Task

    Using the ``LOGS1/history.data`` file from this run 
    (note that this now lives in ``LOGS1``), first look at:
    
    - what history quantities are available 
    - and what their names are, 

    then plot:

    - Mass change rate by star 1 (``lg_mstar_dot_1``),  
    - Orbital period, 
    - Component masses of the binary

    as a function of age of star 1. For the mass loss rate, please adjust the 
    y-axis limits as is appropriate. 

    |

    Finally, plot 

    - absolute value of Jdot by magnetic braking (``jdot_mb``), 
    - absolute value of Jdot by gravitational waves (``jdot_gr``), 
    - absolute value of the total Jdot (``Jdot``)

    as a function of orbital period, *all in the same figure*. Make the plot 
    log-scale on the y-axis using the ``plt.semilogy()`` command. 

    Jdot here refers to the rate of orbital angular momentum loss from various sources. 
    It is a negative number, which is why in the above we are plotting its absolute value.

    
















