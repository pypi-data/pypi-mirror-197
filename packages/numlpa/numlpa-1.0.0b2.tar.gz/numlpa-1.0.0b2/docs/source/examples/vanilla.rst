Vanilla example
===============

NumLPA contains a default configuration of almost all parameters.
You will see later how to use your own configuration file to replace the default values.
For now, and thanks to all the preconfigured parameters, you will be able to run a usage cycle with a minimum of effort.

Go to a blank working directory and run the following commands:

.. code-block:: bash

   # generate dislocation samples
   numlpa draw samples.tar

   # compute Fourier transforms
   numlpa diffract samples.tar transforms.tar

   # merge Fourier transforms
   numlpa merge transforms.tar transform.tar

   # fit a model
   numlpa fit transform.tar adjustments.tar

   # generate figures
   numlpa export samples.tar fig-samples
   numlpa export transforms.tar fig-transforms
   numlpa export transform.tar fig-transform
   numlpa export adjustments.tar fig-adjustments
