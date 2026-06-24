************************
Day 4.5: Second MESA run
************************

Now let's make a second run. The instructions here will be brief, just so you get some practice with running MESA. 

1. Task List
================

Start from a clean MESA work directory (see :doc:`first_run`), name your new work directory ``zams_model``, and gradually modify it. 

**Inlist parameters** wanted:

.. hlist::
    :columns: 1

    * Change the initial mass of the model to :math:`1.1 M_{\odot}`. 

    * Change the initial metallicity of the star to $Z = 0.018$, and initial hydrogen mass fraction to $X=0.712$. 

    * Change the stopping conditions so that the model stops at the zero age main sequence (ZAMS). 

    * When MESA terminates at ZAMS, have it save the model as ``"zams_1.1Msun.mod"``. 

.. note::

    - Not all of these are in the ``controls`` section of the inlist. Consult the MESA documentation for `star_job <https://docs.mesastar.org/en/26.4.1/reference/star_job.html>`_ and `controls <https://docs.mesastar.org/en/26.4.1/reference/controls.html>`_. 
    - When you change the initial metallicity of the model, you also want to change the metallicity that the opacity uses. Look through the opacity documentation (`kap <https://docs.mesastar.org/en/26.4.1/reference/kap.html>`_) to see what you need to change. 
    - It is up to you whether you want to play around with pgstar. 

**Profile quantities** wanted:

Much like ``history_columns.list``, MESA star also has a ``profile_columns.list`` which controls what 
quantities in the stellar structure get saved into the profiles. 

Follow the instructions for ``history_columns.list`` (see :ref:`here <history_columns>`), but adjust it for 
``profile_columns.list`` instead, and have MESA output the following quantities:

- ``cp`` : specific heat capacity at constant pressure
- ``entropy`` : specific entropy

**Sanity checks**

When the run is finished, check to see 

- Your work directory should now contain a new data file called ``zams_1.1Msun.mod``
- Check the terminal messages to make sure that you correctly set the metallicity, and that the run stops because the star has reached ZAMS. 
- Check whether ``LOGS/profile*.data`` contain ``cp`` and ``entropy`` as data columns. 





