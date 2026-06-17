****************
Fortran Basics
****************

Here we go through a few basic Fortran syntaxes. 

.. note:: 

    Fortran does not care about capitalization. For instance, ``Msun`` and ``msun`` are the 
    same in Fortran. They are not the same in Python. 

1. Comment
============

Fortran comment starts with a ``!`` (as opposed to Python which uses ``#``). 

2. Declaring and Assigning Variables
====================================

In Fortran, all variables need to be declared their types. This is done near the top 
of each program, subroutine, or function. For instance, 

.. code-block:: fortran

    ! declaring variables
    integer :: ierr
    real(dp) :: Rsun
    logical :: need_to_save_profiles_now
    real(dp), dimension(10) :: T

    ! assigning values
    ierr = 0
    Rsun = 6.957d10 ! solar radius in cm
    need_to_save_profiles_now = .true. ! or .false. 
    T(1) = 1d29
    T(2:10) = 1d28

``real`` is a floating-point number. ``dp`` is technically a MESA definition. 
It stands for double precision (8-bytes), as opposed to single precision. 

You can use scientific notation for ``real`` variables. 
``1e10`` gives :math:`10^{10}` in single precision, whereas ``1d10`` gives the same 
quantity but in double precision. In MESA, always use double precision. 

In this example, ``T`` is an array of length 10 for double-precision float-point numbers. 

.. note:: 

    The first element of a Fortran array is given by 1, i.e. ``T(1)`` is the first element 
    of the ``T`` array. Python instead starts with 0. 

3. If-Then-Else
===============

.. code-block:: fortran

    if (mass >= 100d0) then
        write(*,*) "mass greater than 100"
    else if ((mass < 100d0) .and. (mass > 10d0)) then
        write(*,*) "mass between 10 and 100"
    else
        write(*,*) "mass less than 10"
    end if

4. Miscellaneous
================

You can print values out on the terminal like this:

.. code-block:: fortran

    write(*,*) "hello world"

    
5. Quick Fortran program example
====================================

In this example, we'll write a short Fortran program just as an . 
Using a text editor, create a file called ``example.f90`` and add the following:

.. code-block:: fortran

    program example

        implicit none

        Rsun = 7d10
        write(*,*) Rsun

    end program example

Now on your terminal, do the following:

.. code-block:: bash

    gfortran example.f90 -o example

This uses the ``gfortran`` compilter, to compile the ``example.f90`` 
from the human-readable Fortran language into a machine-readable 
program, and creates an executable called ``example``. 

You should see an error message like the following:

.. code-block:: bash

    example.f90:7:8:

        7 |     Rsun = 7d10
        |        1
    Error: Symbol 'rsun' at (1) has no IMPLICIT type

It is telling you that you have not assigned the variable type to ``Rsun`` yet. 
You will likely run into errors like this when running MESA, so it's good to get a 
sense of how to fix this. 

In this case, we simply have to declare the variable type of ``Rsun``:


.. code-block:: fortran

    program example

        implicit none

        integer, parameter :: dp = selected_real_kind(p=15)  ! real64
        real(dp) :: Rsun

        Rsun = 7d10
        write(*,*) Rsun

    end program example

where ``dp`` is defined within MESA and we copied it here for consistency. 
Now we're ready to compile again:

.. code-block:: bash

    gfortran example.f90 -o example

    ./example


