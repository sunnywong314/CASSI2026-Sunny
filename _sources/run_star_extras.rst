****************
run_star_extras
****************

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





