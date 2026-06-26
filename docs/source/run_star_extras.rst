************************************
run_star_extras (if possible)
************************************

1. Intro to run_star_extras
===============================

We have seen that we can change the runtime parameters using the inlists, and 
the outputs using ``history_columns.list`` and ``profile_columns.list``. 

However, what if we want to change some runtime parameter during the run, or if 
we want an output quantity that is not included in MESA's preset list? This is where 
`run_star_extras` come in handy. 

`run_star_extras` contains a set of Fortran subroutines and functions, that get called by MESA 
regularly. When they get called, they allow the user to specify 

- custom stopping conditions
- custom history or profile quantities
- custom physics 

Here we will give some examples on how to implement our own history and profile quantities. 

2. Getting started with run_star_extras
========================================

In this example, we will use the ``zams_model`` work directory from :doc:`second_run`.

.. admonition:: Task

    Using a text editor, open ``src/run_star_extras.f90``. 

.. dropdown:: What do you see? (Click to expand)

    .. code-block:: fortran

        module run_star_extras

            use star_lib
            use star_def
            use const_def
            use math_lib

            implicit none

        ! these routines are called by the standard run_star check_model
        contains

            include 'standard_run_star_extras.inc'

        end module run_star_extras

    Here, ``use star_lib`` and ``use math_lib`` act kind of like Python's ``import <module>``. 
    It imports a set of useful subroutines and functions 
    from MESA's ``star`` and ``math`` modules, which you use anywhere within `run_star_extras`. 
    So for example, you can use the function ``safe_log10()`` to take logarithms in base 10. 
    
    Similarly, ``use star_def`` and ``use const_def`` import some variable definitions, 
    so that you can safely use, say, a variable called ``Msun``, whose value is something like ``1.99d33``. 

|

In `run_star_extras`, there is a statement saying ``include 'standard_run_star_extras.inc'``. 
This imports a set of subroutines and functions from an external file called ``'standard_run_star_extras.inc'``. 
If we want to modify our `run_star_extras`, we need to replace the `include` statement with our own set of 
subroutines and functions. 

.. admonition:: Task

    Using a text editor, open ``$MESA_DIR/include/standard_run_star_extras.inc``. Copy and paste 
    the contents into your own `run_star_extras`, replacing the ``include 'standard_run_star_extras.inc'`` line. 

.. dropdown:: What should your `run_star_extras` look like? (Click to expand)

    If you did this correctly, your `run_star_extras` should look like:

    .. dropdown:: (Click to expand)

        .. code-block:: fortran

            module run_star_extras

                use star_lib
                use star_def
                use const_def
                use math_lib

                implicit none

            ! these routines are called by the standard run_star check_model
            contains

                subroutine extras_controls(id, ierr)
                    integer, intent(in) :: id
                    integer, intent(out) :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return

                    ! this is the place to set any procedure pointers you want to change
                    ! e.g., other_wind, other_mixing, other_energy  (see star_data.inc)


                    ! the extras functions in this file will not be called
                    ! unless you set their function pointers as done below.
                    ! otherwise we use a null_ version which does nothing (except warn).

                    s% extras_startup => extras_startup
                    s% extras_start_step => extras_start_step
                    s% extras_check_model => extras_check_model
                    s% extras_finish_step => extras_finish_step
                    s% extras_after_evolve => extras_after_evolve
                    s% how_many_extra_history_columns => how_many_extra_history_columns
                    s% data_for_extra_history_columns => data_for_extra_history_columns
                    s% how_many_extra_profile_columns => how_many_extra_profile_columns
                    s% data_for_extra_profile_columns => data_for_extra_profile_columns

                    s% how_many_extra_history_header_items => how_many_extra_history_header_items
                    s% data_for_extra_history_header_items => data_for_extra_history_header_items
                    s% how_many_extra_profile_header_items => how_many_extra_profile_header_items
                    s% data_for_extra_profile_header_items => data_for_extra_profile_header_items

                end subroutine extras_controls


                subroutine extras_startup(id, restart, ierr)
                    integer, intent(in) :: id
                    logical, intent(in) :: restart
                    integer, intent(out) :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return
                end subroutine extras_startup


                integer function extras_start_step(id)
                    integer, intent(in) :: id
                    integer :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return
                    extras_start_step = 0
                end function extras_start_step


                ! returns either keep_going, retry, or terminate.
                integer function extras_check_model(id)
                    integer, intent(in) :: id
                    integer :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return
                    extras_check_model = keep_going
                    if (.false. .and. s% star_mass_h1 < 0.35d0) then
                        ! stop when star hydrogen mass drops to specified level
                        extras_check_model = terminate
                        write(*, *) 'have reached desired hydrogen mass'
                        return
                    end if


                    ! if you want to check multiple conditions, it can be useful
                    ! to set a different termination code depending on which
                    ! condition was triggered.  MESA provides 9 customizable
                    ! termination codes, named t_xtra1 .. t_xtra9.  You can
                    ! customize the messages that will be printed upon exit by
                    ! setting the corresponding termination_code_str value.
                    ! termination_code_str(t_xtra1) = 'my termination condition'

                    ! by default, indicate where (in the code) MESA terminated
                    if (extras_check_model == terminate) s% termination_code = t_extras_check_model
                end function extras_check_model


                integer function how_many_extra_history_columns(id)
                    integer, intent(in) :: id
                    integer :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return
                    how_many_extra_history_columns = 0
                end function how_many_extra_history_columns


                subroutine data_for_extra_history_columns(id, n, names, vals, ierr)
                    integer, intent(in) :: id, n
                    character (len=maxlen_history_column_name) :: names(n)
                    real(dp) :: vals(n)
                    integer, intent(out) :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return

                    ! note: do NOT add the extras names to history_columns.list
                    ! the history_columns.list is only for the built-in history column options.
                    ! it must not include the new column names you are adding here.


                end subroutine data_for_extra_history_columns


                integer function how_many_extra_profile_columns(id)
                    integer, intent(in) :: id
                    integer :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return
                    how_many_extra_profile_columns = 0
                end function how_many_extra_profile_columns


                subroutine data_for_extra_profile_columns(id, n, nz, names, vals, ierr)
                    integer, intent(in) :: id, n, nz
                    character (len=maxlen_profile_column_name) :: names(n)
                    real(dp) :: vals(nz,n)
                    integer, intent(out) :: ierr
                    type (star_info), pointer :: s
                    integer :: k
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return

                    ! note: do NOT add the extra names to profile_columns.list
                    ! the profile_columns.list is only for the built-in profile column options.
                    ! it must not include the new column names you are adding here.

                    ! here is an example for adding a profile column
                    !if (n /= 1) stop 'data_for_extra_profile_columns'
                    !names(1) = 'beta'
                    !do k = 1, nz
                    !   vals(k,1) = s% Pgas(k)/s% P(k)
                    !end do

                end subroutine data_for_extra_profile_columns


                integer function how_many_extra_history_header_items(id)
                    integer, intent(in) :: id
                    integer :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return
                    how_many_extra_history_header_items = 0
                end function how_many_extra_history_header_items


                subroutine data_for_extra_history_header_items(id, n, names, vals, ierr)
                    integer, intent(in) :: id, n
                    character (len=maxlen_history_column_name) :: names(n)
                    real(dp) :: vals(n)
                    type(star_info), pointer :: s
                    integer, intent(out) :: ierr
                    ierr = 0
                    call star_ptr(id,s,ierr)
                    if(ierr/=0) return

                    ! here is an example for adding an extra history header item
                    ! also set how_many_extra_history_header_items
                    ! names(1) = 'mixing_length_alpha'
                    ! vals(1) = s% mixing_length_alpha

                end subroutine data_for_extra_history_header_items


                integer function how_many_extra_profile_header_items(id)
                    integer, intent(in) :: id
                    integer :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return
                    how_many_extra_profile_header_items = 0
                end function how_many_extra_profile_header_items


                subroutine data_for_extra_profile_header_items(id, n, names, vals, ierr)
                    integer, intent(in) :: id, n
                    character (len=maxlen_profile_column_name) :: names(n)
                    real(dp) :: vals(n)
                    type(star_info), pointer :: s
                    integer, intent(out) :: ierr
                    ierr = 0
                    call star_ptr(id,s,ierr)
                    if(ierr/=0) return

                    ! here is an example for adding an extra profile header item
                    ! also set how_many_extra_profile_header_items
                    ! names(1) = 'mixing_length_alpha'
                    ! vals(1) = s% mixing_length_alpha

                end subroutine data_for_extra_profile_header_items


                ! returns either keep_going or terminate.
                ! note: cannot request retry; extras_check_model can do that.
                integer function extras_finish_step(id)
                    integer, intent(in) :: id
                    integer :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return
                    extras_finish_step = keep_going

                    ! to save a profile,
                        ! s% need_to_save_profiles_now = .true.
                    ! to update the star log,
                        ! s% need_to_update_history_now = .true.

                    ! see extras_check_model for information about custom termination codes
                    ! by default, indicate where (in the code) MESA terminated
                    if (extras_finish_step == terminate) s% termination_code = t_extras_finish_step
                end function extras_finish_step


                subroutine extras_after_evolve(id, ierr)
                    integer, intent(in) :: id
                    integer, intent(out) :: ierr
                    type (star_info), pointer :: s
                    ierr = 0
                    call star_ptr(id, s, ierr)
                    if (ierr /= 0) return
                end subroutine extras_after_evolve


            end module run_star_extras

|

.. caution::

    Every time you edit `run_star_extras`, you need to **recompile**. Otherwise MESA won't know 
    the code you edited. 


.. admonition:: Task

    Recompile by running ``./mk``. 


3. MESA Flowchart
==================

When MESA runs, it executes a flowchart like the following. 

.. raw:: html

   <object data="_static/flowchart.pdf" type="application/pdf" width="100%" height="600px">
       <p>Your browser does not support PDFs. 
       <a href="_static/flowchart.pdf">Download the PDF</a> instead.</p>
   </object>

There are many places where the subroutines and functions of `run_star_extras` get called. 
For example, at the end of each time step, MESA calls ``extras_finish_step``. 


4. MESA star data
=================

When MESA evolves a star, it saves many quantities of the stellar structure, both global and local. 
For example, it saves the effective temperature of the star (global), as well as the temperature 
structure of the star (local). 
These are all saved within the ``star_data`` structure. 

.. admonition:: Task

    The quantities accessible to `star_data` live in ``$MESA_DIR/star_data/public/``. 
    
    Using a text editor, open ``$MESA_DIR/star_data/public/star_data_step_input.inc`` and 
    ``$MESA_DIR/star_data/public/star_data_step_work.inc``, to see what can be accessed. 

.. dropdown:: What do you see? (Click to expand)

    In ``star_data_step_work.inc``, you can see things like 

    .. code-block:: Fortran

        real(dp) :: mstar_dot ! (gm/second)

    This is the rate of change of the star's mass, in grams per second. 
    
    Unless otherwise specified, 
    all quantities in `star_data` are in CGS units. 

    You will also see 

    .. code-block:: Fortran

        real(dp), pointer :: m(:) ! baryonic mass coord
         ! m(k) is enclosed baryonic mass at outer edge of cell k
         ! m(k) = s% M_center + s% q(k)*s% xmstar

    This is the mass enclosed at the outer edge of each cell. You'll notice that it has ``(:)``, 
    because it is an array. The ``:`` means that its length is not fixed -- 
    it is equal to the number of cells in the star, which changes from timestep to timestep. 

|

Accessing star data quantities in run_star_extras
_________________________________________________

Here we give an example for how to access star data quantities in `run_star_extras`. 

.. admonition:: Task

    Let's edit the ``extras_finish_step`` function in ``run_star_extras``, 
    following the instructions below. 

In ``extras_finish_step``, you'll see 

.. code-block:: Fortran

    type (star_info), pointer :: s

    ...

    call star_ptr(id, s, ierr)

The first line declares the variable ``s`` as the MESA variable type ``star_info``. As a reminder, 
all variables in Fortran need to be declared their types. 

The second line calls the ``star_ptr`` subroutine, and essentially points all `star_data` quantities 
to the ``s`` variable. With this, all `star_data` quantities are accessible through ``s``. 

To access the `star_data` quantities, you use the ``%`` operator:

.. admonition:: Task

    Add the following line to ``extras_finish_step``:

    .. code-block:: Fortran

        write(*,*) s% mstar, s% m(1), 1.1d0*Msun

    anywhere between ``extras_finish_step = keep_going`` and ``end function extras_finish_step``. 

    Then recompile, and run MESA. 

    Watch the terminal to see what comes out. You should see some addition 
    terminal messages at each step, after the relaxation steps are done. 

.. dropdown:: What do you see? (Click to expand)

    You should see

    .. code-block:: bash

        2.1872508577678557E+033   2.1872508577678557E+033   2.1872508577678557E+033

    This should give the star's total mass in grams (hence the line ``1.1d0*Msun``). 

|

.. note::

    The ``%`` operator in Fortran works very similarly to the ``.`` operator in python. 
    For example, in python you get the value of pi from the `numpy` module using ``np.pi``. 
    Here we access the value of ``mstar`` from ``s`` using ``s% mstar``. 

In the example above, we showed two equivalent ways of obtaining the star's total mass. 
We can access it readily from ``s% mstar``. We can also use the enclosed mass at each shell 
k, ``s% m(k)``. Zone 1 gives the surface, and zone ``s% nz`` gives the cell at the center. 
This means ``s% m(1)`` should give the mass enclosed at the surface zone, which is exactly the 
total mass of the star. 

.. note:: 

    Fortran uses 1-indexing and parenthesis for arrays. 
    This means the first element of some array ``A`` is given by ``A(1)``, 
    second by ``A(2)``, and so on. 
    
    Python uses 0-indexing and square brackets for arrays. 
    This means the first element of some array ``B`` is given by ``B[0]``, 
    second by ``B[1]``, and so on. 

|

Now, some more practice:

.. admonition:: Task

    Have ``extras_finish_step`` print out the central temperature, and log10 of the 
    central temperature

    Remember, every time you edit `run_star_extras`, recompile!

.. tip:: 

    The math functions accessible in MESA are given in ``$MESA_DIR/math/public/math_lib_crmath.f90``. 
    
    Use a text editor to see what is available. 

    For example, ``exp10(x)`` is equivalent to :math:`10^{x}`. Note that it is different than ``exp(x)``, 
    which is in base :math:`e`. 

.. dropdown:: Solutions (Click to expand)

    Add the following:

    .. code-block:: fortran

        write(*,*) s% T(s% nz), safe_log10(s% T(s% nz))

    Compile, and run. 

5. extra_history_columns
========================

Here we will use `run_star_extras` to implement our own history output. 

.. admonition:: Task

    First, look up the ``how_many_extra_history_columns`` function in ``run_star_extras``. 

    Set ``how_many_extra_history_columns = 2`` within this function. 

This tells MESA we 
want to have two extra history columns. Whenever you want an additional history column, you 
need to change this function. 

Example 1
_________

Next, 

.. admonition:: Task

    Navigate to the ``data_for_extra_history_columns`` subroutine. 

    Add the following line right before the subroutine ends:

    .. code-block:: Fortran

        names(1) = 'my_total_mass'

This tells MESA that our first extra history column should be named ``'my_total_mass'``. 

|

Now we're ready to feed MESA the value for the total mass, 
for which we show yet another way to calculate. 

In MESA, the star is broken up into many individual zones. The mass of zone ``k`` is given by 
``s% dm(k)`` (in grams). So if we sum up the `dm` of all the zones, we should recover the 
total mass of the star. This is done by the following `do` loop:

.. code-block:: Fortran

    m_total = 0d0 ! initialize the variable to 0

    ! loop from surface to center
    do k = 1, s% nz, 1
        m_total = m_total + s% dm(k)
    end do

    ! print out the value for sanity checks
    write(*,*) 'my_total_mass is:',  m_total

    ! Save the value to vals(1)
    ! vals(:) gives the values used by MESA for extra history columns
    vals(1) = m_total

The `do` loop in Fortran is essentially the `for` loop in python. In this example, 
we start from `k=1`, add one each time, until it reaches `k=s% nz` (inclusive). 

|

.. admonition:: Task

    Add the above code to your ``data_for_extra_history_columns``. 

    In addition, declare the variable types in the subroutine:

    .. code-block:: Fortran

        real(dp) :: m_total
        integer :: k

.. dropdown:: Solutions (Click to expand)

    Your ``data_for_extra_history_columns`` should now look like:

    .. code-block:: Fortran

        subroutine data_for_extra_history_columns(id, n, names, vals, ierr)
            integer, intent(in) :: id, n
            character (len=maxlen_history_column_name) :: names(n)
            real(dp) :: vals(n)
            integer, intent(out) :: ierr
            type (star_info), pointer :: s
            ! declare new variables
            real(dp) :: m_total
            integer :: k

            ierr = 0
            call star_ptr(id, s, ierr)
            if (ierr /= 0) return

            ! note: do NOT add the extras names to history_columns.list
            ! the history_columns.list is only for the built-in history column options.
            ! it must not include the new column names you are adding here.

            names(1) = 'my_total_mass'

            m_total = 0d0 ! initialize the variable to 0

            ! loop from surface to center
            do k = 1, s% nz, 1
                m_total = m_total + s% dm(k)
            end do

            ! print out the value for sanity checks
            write(*,*) 'my_total_mass is:',  m_total

            ! Save the value to vals(1)
            ! vals(:) gives the values used by MESA for extra history columns
            vals(1) = m_total


        end subroutine data_for_extra_history_columns        


Example 2
_________

The example above shows how you can implement an extra history column, and how to do a `do` loop. 
Now you're ready for something more complicated. 

In the following, we want to calculate the following quantity:

.. math::

    t_{\rm th} = \frac{ \int^{M}_{0} c_{\rm p} T dm }{L}

|

Now let's break this down:

- :math:`c_{\rm p}` is the specific heat capacity of each cell (in this case, specific means per unit mass). 
- :math:`c_{\rm p} T` gives the thermal content per unit mass of each cell. 
- If you multiply that by :math:`dm` of each cell, you get the thermal content of the cell. 
- If you add up the thermal content of all the cells (hence the integral), you get the total thermal content of the star. 
- Divide by the surface luminosity :math:`L`, you get the star's `thermal timescale`, how quickly the star adjusts its thermal content by radiating its energy away. 

|

We are now ready to implement this. 

.. admonition:: Task

    Following the `do` loop example above, implement a variable called ``E_th``, which is 
    given by :math:`\int^{M}_{0} c_{\rm p} T dm`. 
    
    In practice, calculate 
    :math:`c_{\rm{p},k} \cdot T_{k} \cdot dm_{k}` of each cell :math:`k`, then sum up all the cells 
    using a `do` loop. 

    Divide ``E_th`` by the surface luminosity of the star, and call it ``t_th``. 

    Finally, assign the new history column the value of ``t_th``, and give the new history column a name ``"t_th"``. Compile and run. 

    Make sure to also declare any new variables. 

.. dropdown:: Partial Hint: Pseudocode to get you started (Click to expand)

    .. code-block:: Fortran

        ! name your new history column quantity here
        ...

        ! initialize value to 0
        E_th = 0d0

        ! do loop to calculate Eth
        do ...

            E_th = E_th + s% ...  ! add the cp*T*dm of cell k

        end do

        ! divide by surface luminosity to get thermal time
        t_th = E_th / ... 

        ! assign value to your new history column
        ... 

        

.. dropdown:: Partial Hint: Where to look up star data quantities? (Click to expand)

    Go to ``$MESA_DIR/star_data/public``, and look up your quantity in either 
    ``star_data_step_work.inc`` or ``star_data_step_input.inc``. 

    The ``grep`` command may be useful on the terminal (see :doc:`commands`). 

    Quantities you need: `cp`, `T`, `dm`, of each cell, and the surface luminosity (luminosity of surface cell). 


.. dropdown:: Partial Hint: What is the surface luminosity of the star? (Click to expand)

    You can access the surface luminosity through two ways:

    - ``s% L(:)`` is an array containing the luminosity at outer edge of each cell. If we want the surface luminosity, we can access it by ``s% L(1)``. 
    - Alternatively, we can also use ``s% L_phot``, which gives the photospehre luminosity in Lsun units. Because we want the luminosity in cgs units, we actually want ``s% L_phot * Lsun``. 

.. Tip:: 

    Printing your values to the terminal is a helpful way to check whether you did this correctly (just helpful in general). 
    You should get a value that is about 1e14 - 1e15 seconds (1e7 years), to within a factor of a few. 

|

This was a lot of work, so great job getting here! 
The thermal timescale will be useful for future runs, once we get to the binary runs. 












