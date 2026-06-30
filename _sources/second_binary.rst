*************************
Day 6: Second Binary Run 
*************************

Now we will delve further into binary evolution. 

1. Fully Conservative Mass Transfer with No Angular Momentum Loss
==================================================================

In this binary run, we will try to learn what happens to the binary orbit 
when there is no mass and angular momentum losses from the binary, 
particularly to the orbital period/ separation. 

.. admonition:: Task

    Make a copy of your first binary run. Name it something new. 

    Set the following:

    - Initial binary parameters: star 1 mass of 1.4 solar masses, star 2 mass of 1.0 solar mass, and orbital period of 1 day. 
    - Set ``do_jdot_* = .false.`` , which turns off all the orbital angular momentum loss. The asterisk ``*`` here means that there are several options you need to use. 
    - Set ``limit_retention_by_mdot_edd = .false.``. By default, this option is on, meaning that star 2 will only accrete up to its Eddington limit, and the rest is lost from the system. Here we want to model fully conservative mass transfer, so we want to turn this off. 

    Consult `binary controls <https://docs.mesastar.org/en/26.4.1/reference/binary_controls.html>`_ if you are stuck.

Now you are ready to run. While it is running, 

.. admonition:: Task

    Observe: 

    - What happens to the orbital period initially? 
    - The orbital period eventually reverses trend. At this point, what are the masses of star 1 and star 2? 
    - What is the peak mass transfer rate? 
    - Kill the run once it reaches model number 500. You can do this manually on the terminal with ``ctrl+c``. 

Hopefully this gives your more intuition into what happens to the binary orbit 
depending on the mass ratio. 

2. On the way to making an evolved CV
=======================================

Now we're ready to make more complicated runs in preparation for 
making an AM CVn binary through the evolved CV channel. 


.. admonition:: Task

    Once again, make a copy of your first binary run. Name it something new. 

    Change your inlists parameters according to the following. 
    You will need to figure out to which inlist each goes. 

.. dropdown:: Binary options (Click to expand)

    - Initial binary parameters: star 1 mass of 1.1 solar masses, star 2 mass of 0.75 solar mass, and orbital period of 1.5 days. 
    - Set ``limit_retention_by_mdot_edd = .false.``. By default, this option is on, meaning that star 2 will only accrete up to its Eddington limit, and the rest is lost from the system. While we still want to make the mass transfer non-conservative, we'll deploy another option (keep reading). 
    - Set ``mass_transfer_beta = 1.0d0``. This means that whatever the donor donates, will be lost from the accretor as a fast wind. The wind mass loss will carry the specific angular momentum of the accretor. 
    .. - Set ``mdot_scheme = 'Kolb'``. This means MESA will calculate the mass transfer rate following Kolb et al. 1990, which varies with how much the donor is overfilling its Roche lobe and stellar conditions near the Roche lobe. 

    Consult `binary controls <https://docs.mesastar.org/en/26.4.1/reference/binary_controls.html>`_ if you are stuck.

.. dropdown:: Star options (Click to expand)

    The following inlist options will be in different sections of the inlist. 
    Consult the MESA documentation for `star_job <https://docs.mesastar.org/en/26.4.1/reference/star_job.html>`_ and `controls <https://docs.mesastar.org/en/26.4.1/reference/controls.html>`_.

    First, 

    - Have MESA load ``zams_1.1Msun.mod`` (from :doc:`second_run`). You will need to make sure that MESA has the right path to this model. 
    - Set the initial model number to 0.
    - Set the initial star age to 0. 

    Hint: each of these three above requires two options. Of the two, one requires you setting some flag to true, and the other requires you setting some value. 

    Then, 
    
    - Change the base metallicity for the opacity calculations (you did this in :doc:`second_run` too), to :math:`Z=0.018`. 

    Finally, 

    - Set the profile output frequency to every 200 models. 
    - Set the history file output frequency to every 5 models. 
    - Set ``energy_eqn_option = 'eps_grav'``. By default, this option is ``'dedt'``. Both are just different ways of rewriting the energy equation. ``'dedt'`` is great at numerical energy conservation, but is worse for temperature (technically, entropy) evolution under electron degeneracy. See the MESA VI paper for more discussion. 
    - Set ``use_ledoux_criterion = .true.``. When determining whether a region is convective or radiative, the Ledoux criterion considers the stabilizing effect of a chemical gradient, in addition to the temperature gradient. 
    - Set ``redo_limit`` to some ridiculously large integer number. This prevents our model from stopping early from having too many redos. 
    - Set ``atm_T_tau_opacity = 'iterated'``. This changes how the opacity in the atmosphere is calculated. 
    - Set ``limit_for_rel_error_in_energy_conservation = 1d-2`` and ``hard_limit_for_rel_error_in_energy_conservation = 1d-1``. MESA limits its timesteps based on numerical energy conservation. Here we relax the timesteps for convenience. 
    - Set: 

    .. code-block:: Fortran

        overshoot_scheme(1) = 'exponential'
        overshoot_zone_type(1) = 'nonburn'
        overshoot_zone_loc(1) = 'shell'
        overshoot_bdy_loc(1) = 'bottom'

        overshoot_f(1) = 0.01d0
        overshoot_f0(1) = 0.005d0

    Inside the convection zone, fluid elements have some acceleration and rise to the surface 
    until they reach the convective boundary, where they have zero acceleration. 
    However, this doesn't mean they have zero velocity. They can still go beyond the convective boundary 
    until they reach zero velocity. Convective overshooting considers this mechanical effect in 
    mixing chemicals. In our case, this is in part a numerical convenience to mix the core materials 
    into the envelope. 

    **History quantities**: Find the history columns quantity that lets you output the 
    surface abundance of all the isotopes present in the model. 

.. admonition:: Task

    Run the model and observe its orbital evolution. 
    Note also the surface hydrogen abundance. 

If you have time, try running the same model but with different initial orbital periods. 
Do not change it by more than 1 day. And do not overwrite your binary run. 