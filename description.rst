The transitionMatrix Library
=============================

transitionMatrix is a Python powered library for the statistical analysis and visualization of state transition phenomena.
It can be used to analyze any dataset that captures timestamped transitions in a discrete state space.
Use cases include credit rating transitions, system state event logs and more.

* Author: `Open Risk <http://www.openriskmanagement.com>`_
* License: Apache 2.0
* Code Documentation: `Read The Docs <https://transitionmatrix.readthedocs.io/en/latest/>`_
* Mathematical Documentation: `Open Risk Manual <https://www.openriskmanual.org/wiki/Category:Transition_Matrix>`_
* Training: `Open Risk Academy <https://www.openriskacademy.com/login/index.php>`_
* Development Website: `Github <https://github.com/open-risk/transitionMatrix>`_
* Showcase: `Blog Posts <https://www.openriskmanagement.com/tags/transition-matrix/>`_

Functionality
-------------

You can use transitionMatrix to

- Estimate transition matrices from historical event data using a variety of estimators
- Visualize event data and transition matrices
- Characterise transition matrices
- Manipulate transition matrices (derive generators, perform comparisons, stress transition rates etc.)
- Access standardized datasets for testing
- Extract and work with default curves
- Map credit ratings using mapping tables

**NB: transitionMatrix is still in active development. If you encounter issues please raise them in our
github repository**

Architecture
------------

* transitinoMatrix supports file input/output in json and csv formats
* it has a powerful API for handling event data (based on pandas)
* provides intuitive objects for handling transition matrices individually and as sets (based on numpy)
* supports visualization using matplotlib

Links to other open source software
-----------------------------------

- Duration based estimators are similar to etm, an R package for estimating empirical transition matrices
- There is some overlap with lower dimensionality (survival) models like lifelines

Installation
=======================

You can install and use the transitionMatrix package in any system that supports the `Scipy ecosystem of tools <https://scipy.org/install.html>`_

Dependencies
-----------------

- TransitionMatrix requires Python 3 (currently 3.7)
- It depends on numerical and data processing Python libraries (Numpy, Scipy, Pandas).
- The Visualization API depends on Matplotlib.
- The precise dependencies are listed in the requirements.txt file.
- TransitionMatrix may work with earlier versions of python / these packages but it is not tested.

From PyPI
-------------

.. Todo:: PyPI might not have the latest and best release

.. code:: bash

    pip3 install pandas
    pip3 install matplotlib, plotly
    pip3 install transitionMatrix

From sources
-------------

Download the sources in your preferred directory:

.. code:: bash

    git clone https://github.com/open-risk/transitionMatrix


Using virtualenv
----------------

It is advisable to install the package in a virtualenv so as not to interfere with your system's python distribution

.. code:: bash

    virtualenv -p python3 tm_test
    source tm_test/bin/activate

If you do not have pandas already installed make sure you install it first (this will also install numpy and other required dependencies).

.. code:: bash

    pip3 install pandas
    pip3 install matplotlib
    pip3 install -r requirements.txt

Finally issue the install command and you are ready to go!

.. code:: bash

    python3 setup.py install

File structure
-----------------
The distribution has the following structure:

::

    | transitionMatrix/     Directory with the library source code
    | -- model.py           File with main data structures
    | -- estimators/        Directory with the estimator methods
    | -- utils/             Directory with helper classes and methods
    | -- examples/          Directory with usage examples
    | ---- python/          Examples as standalone python scripts
    | ---- notebooks/       Examples as jupyter notebooks
    | ---- academy/         Example scripts from the Open Risk Academy course PYT26038
    | -- datasets/          Directory with a variety of datasets useful for getting started
    | -- tests/             Directory with the testing suite

Testing
----------------------

It is a good idea to run the test-suite. Before you get started:
- Adjust the source directory path in transitionMatrix/__init__ and then issue the following in at the root of the distribution
- Unzip the data files in the datasets directory

.. code:: bash

    python3 test.py

Getting Started
===============

- Check the **Usage** pages in this documentation.
- Look at the **Examples** directory for a variety of typical workflows.
- For a more in depth study, the Open Risk Academy has courses elaborating on the use of the library:
    - `Analysis of Credit Migration using Python TransitionMatrix <https://www.openriskacademy.com/course/view.php?id=38>`_

