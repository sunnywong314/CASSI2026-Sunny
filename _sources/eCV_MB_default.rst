******************************************
Day 7: Improvements on Evolved CV Model
******************************************

Here we will make a couple of changes to our evolved CV model. 

1. New Opacities
================

First, the opacities that MESA uses at low temperatures do not extend to the high densities of our helium WD. 
We will implement a new opacity coming from the AESOPUS code. However, the MESA implementation does not allow 
extrapolation of this table beyond its range of validity. We will attempt to do this; while unphysical, it 
allows our model to continue evolving. The AESOPUS table itself extends to much higher densities, so the 
model will rarely run into this problem. 

.. dropdown:: Changing the source code (Click to expand)

    .. admonition:: Task

        Download the following file :download:`kap_aesopus.f90 <kap_aesopus.f90>`. 

        Then, on your terminal, go to :

        .. code-block:: bash

            cd $MESA_DIR/kap

            cp ~/Downloads/kap_aesopus.f90 ./private/

        Here I assume that your ``kap_aesopus.f90`` file is downloaded to the Downloads directory. 
        Modify the path as necessary. 

        Then, 

        .. code-block:: bash

            ./mk

            ./export

        This compiles the new code, and exports the new code to MESA's libraries. If you did all this 
        correctly, you should see 
        the terminal message

        .. code-block:: bash

            COMPILE_CMD ../private/kap_aesopus.f90
            LIB_TOOL_libkap.a

    Because we made a change to MESA's source code, all our new runs need to be recompiled. 
    This will be included in our next step. 

2. Inlist Changes
====================

Now we're ready to make more complicated runs in preparation for 
making an AM CVn binary through the evolved CV channel. 


.. admonition:: Task

    Make a copy of your evolved CV run from the end day 6. Name it something new. 
    Then recompile the code. 

    Change your inlists parameters according to the following. 
    You will need to figure out to which inlist each goes. 

.. dropdown:: Binary options (Click to expand)

    - Initial binary parameters: star 1 mass of 1.1 solar masses, star 2 mass of 0.75 solar mass, and orbital period of 1.5 days. 
    - Set ``max_tries_to_achieve = 30``. At each time step, MESA will iterate to solve for the mass transfer rate up to some number of times. If the mass transfer rate is not determined by then, MESA will retry and take a smaller timestep. We make this number slightly larger to avoid a retry.
    Consult `binary controls <https://docs.mesastar.org/en/26.4.1/reference/binary_controls.html>`_ if you are stuck.

.. dropdown:: Star options part 1 (Click to expand)

    The following inlist options will be in different sections of the inlist. 
    
    First, we will have MESA use new opacities for both the low-temperature regime and at higher temperatures. 
    Take a quick look at the MESA documenation for `kap <https://docs.mesastar.org/en/26.4.1/reference/kap.html>`_ and implement:

    - Have MESA use AESOPUS for its low-temperature range, and load an AESOPUS file called ``AESOPUS_eCV.h5``. Hint: this requires two kap inlist options. 
    - Have MESA use an opacity file with prefix ``'oplib_gs98'``. This makes use of updated and more densely tabulated opacities from the OPLIB collaboration, implemented by Farag et al. 2024. 
    - Have MESA blend between the higher temperature and lower temperature tables at logT between 4.42 and 4.5. 
    - Have MESA do a cubic interpolation in X and Z. 
    - Finally, download this AESOPUS opacity file :download:`AESOPUS_eCV.h5 <AESOPUS_eCV.h5>` and put it in your work directory. 

    We will also make some equation of state (EOS) changes. 
    Take a quick look at the MESA documenation for `eos <https://docs.mesastar.org/en/26.4.1/reference/eos.html>`_ and implement:

    - ``use_simple_skye_blends = .true.``
    - ``logT_min_for_any_skye = 7.0d0``
    - ``logT_min_for_all_skye = 7.2d0``

    MESA's EOS is a blend between different tables. The above options change the blending region. Sometimes this is done for 
    numerical reasons. 

    
.. dropdown:: Star options part 2 (Click to expand)

    The rest will be star_job and controls. 
    Consult the MESA documentation for `star_job <https://docs.mesastar.org/en/26.4.1/reference/star_job.html>`_ and `controls <https://docs.mesastar.org/en/26.4.1/reference/controls.html>`_.
 

    Finally, 

    - Set ``prune_bad_cz_min_Hp_height = 0.3d0`` and ``prune_bad_cz_min_log_eps_nuc = 99d0``. These remove tiny convection zones that appear due to numerical errors, and avoid further numerical problems due to their appearance. 
    - Set ``eps_mdot_leak_frac_factor = 0d0``. This is a control that avoids numerical problems when MESA runs into high mass transfer rates and bad thermodynamic quantities from the EOS. 
      
    Once you are done, you might want to rearrange your the `controls` options into different groups for better book-keeping. 

.. admonition:: Task

    Run the model and observe its orbital evolution. 
    Note also the surface hydrogen abundance. 

If you have time, try running the same model but with different initial orbital periods. 
Do not change it by more than 1 day. And do not overwrite your binary run. 