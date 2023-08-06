Use virtual environments
========================

This step **is not necessary** for the installation of the package.
You can skip it, **but** you may lose the opportunity to keep the Python packages you install on your computer tidy.

Why?
----

If you are not already familiar with virtual environments, you should know that what is presented in this section allows you to install the package in a "virtual" location so that it does not affect the rest of the packages you have installed on your computer.
This offers several advantages:

* If you want to temporarily install the package, for example to test it, you can remove all traces of its installation simply by deleting the virtual environment.

* You can work on several projects (within different virtual environments) that require different versions of a package.

* If you want to edit the package, you can do it in a virtual environment while maintaining another virtual environment with an official version of NumLPA.

* When you create a virtual environment, only the pip and setuptools packages are preinstalled.
  By cleaning up your workspace in this way, you can identify precisely the libraries (and their version) that your program needs to work properly, because you will have to install them in your new virtual environment.
  You can then list the required packages and their version in a ``requirements.txt`` file.
  This way, for another person, or on another machine it will be possible to recreate the conditions of functioning of your program by initiating a virtual environment and executing the command ``pip install -r requirements.txt``.

If you want more information, everything is explained in the `Python documentation <https://docs.python.org/3/library/venv.html>`_.

How?
----

It is very simple.
There are only four steps and nothing to install.

Create your virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Choose a path for your virtual environment and execute the following command:

.. code-block:: bash

   python3 -m venv location-of-your-choice

Activate your virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Your virtual environment is now created.
But to "work in it" you have to run:

.. code-block:: bash

   source location-of-your-choice/bin/activate

Once this command is executed, your terminal "enters" your virtual environment.
The python packages that you install will now be placed in the virtual environment.
When used from within a virtual environment, common installation tools such as pip will install Python packages into a virtual environment without needing to be told to do so explicitly.

Deactivate your virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To leave your virtual environment, run:

.. code-block:: bash

   deactivate

Closing your terminal also does the trick.
Note that this does not delete the virtual environment.
You will be able to find everything you have installed by reactivating your virtual environment.

Delete your virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When you are done with a project, or you want to move your virtual environment, you can delete it with the command :

.. code-block:: bash

   rm -r location-of-your-choice

And now?
--------

It is advisable to execute the installation commands (presented in the following steps) from a virtual environment that you have created and activated as shown above.

