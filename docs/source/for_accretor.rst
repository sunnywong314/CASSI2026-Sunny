********************
Day 8 : For accretor
********************

Now we will make our first attempt at evolving the accretor!

Usually we would set ``evolve_both_stars = .true.`` in MESA binary. 
But we will actually do this in MESA single star. The idea is that we would read in the 
mass accretion rate from the history file from the binary run, then we would create a text file. 
When we run the accretor in single star, we would ask MESA to read in this text file, and change 
the accretion rate accordingly. 

The reason why we do this separation is to avoid having to grapple with MESA runtime troubles 
for `both` stars at the same time. That is, we deal with them separately, which makes things easier. 
Moreover, what happens to the accretor doesn't affect the donor itself, nor the mass transfer rate, 
except for the fact that its mass is increasing (which MESA binary does anyways). In other words, 
we don't need to know the detailed structure of the accretor to know what's gonna happen to the binary. 
This is the key for why we can do this separation. 


Create data file
________________

First we will create a data file that takes the donor history file and writes out the mass accretion history for the accretor. 
This will be done in python. 

.. admonition:: Task

    First read in the history file with MESA reader. 

    We will then create a boolean array for the donor surface h1 :math:`X <= 0.1`.

    Then using this boolean array, we will create the following arrays that satisfy :math:`X <= 0.1`. Most of these quantities will have the same units as the history file, but a few may require a little bit of conversion. 

    - star age in yrs. Then subtract the entire star age array by its first element. Your new star age array should have 0 as its first element.
    - orbital period in minutes (Note: you will need a unit conversion from days to minutes)
    - binary separation in Rsun
    - donor mass in Msun
    - donor radius in Rsun
    - log10 of donor mass loss rate in Msun/yr (Note: we want the log10)
    - log10 of donor surface H1 (Note: we want the log10)


We will then try to write our data to a text file. 

.. admonition:: Task

    Write out the above data to a text file called ``for_accretor.data``. 

    The rows should be in the format:

    .. code-block:: python

        <length of column>

        age[0] period[0] separation[0] mass[0] radius[0] logMdot[0] logH1[0]

        age[1] period[1] separation[1] mass[1] radius[1] logMdot[1] logH1[1]

        ...

    The first row should be the length of the array. And each column should be separated by white space. 


Below is a hint for how you can write things out into a text file in python:

.. dropdown:: Hint: how to write things out to a file in python? (Click to expand)
    
    .. code-block:: python

        f = open('myfile.txt', 'w') # 'w' for write

        f.write('blah \n') # \n for new line

        f.close() # always remember to close it

    To get the numbers printed out in a nice format, try ``'%15.8g'%(number)``. 
    The 15 means we want to give it 15 character slots, and ``.8g`` means you let 
    python choose the cleanest way to express the number with 8 significant numbers. 

.. dropdown:: Hint: for loops (Click to expand)

    Let's say we have two arrays:

    .. code-block:: python

        a=[0.1, 0.2, 0.3]
        b=[0, 5, 8]

    If we want to print out the elements of ``a`` and ``b`` together, we do:

    .. code-block:: python

        for i in range(len(a)):

            print( i, a[i], b[i] )

    which should give you 

    .. code-block:: python

        0 0.1 0
        1 0.2 5
        2 0.3 8

    We do this to get the indices of all the ``a`` or ``b`` lists, and then 
    use the index to access the element of the list. 



