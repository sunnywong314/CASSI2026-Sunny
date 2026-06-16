****************
Fortran Basics
****************

Here we go through a few basic Fortran syntaxes. 

.. note:: 

    Fortran does not care about capitalization. For instance, ``Msun`` and ``msun`` are the 
    same. 

1. Comment
============

Fortran comment starts with a ``!``. 

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



    
    
