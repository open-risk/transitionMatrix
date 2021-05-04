Cohorts
===================
Organizing data in `cohorts <https://www.openriskmanual.org/wiki/Cohort>`_ can be an important step in understating transition data or towards applying a :ref:`cohort estimator`. Cohorts in this context are understood as the grouping of entities within a temporal interval. For example in a credit rating analysis context cohorts could be groups of annual observations. The implication of cohorting data is that the more granular information embedded in a more precise timestamp is not relevant. It is also possible that input data are only available in cohort form (when the precise timestamp information is not recorded at the source)


.. note:: Cohorting can bias the estimation in various subtle ways, so it is important that any procedure is well documented.



Cohorting Utilities
--------------------

Cohorting utilities are part of :ref:`preprocessing`. Presently the core algorithm is implemented in :func:`transitionMatrix.utils.preprocessing.bin_timestamps`.





Intermediate Cohort Data Formats
-------------------------------------------

The cohort data format is a tabular representation of time series data that records the states (measurements) of multiple entities. Its defining characteristic is that each table row contains data pertaining to one entity at one point in time.




The *canonical form* used as input to duration based estimators uses normalized timestamps (from 0 to T_max, where T_max is the last timepoint) and looks as follows:

    +----+------+------+----+
    | ID | Time | From | To |
    +----+------+------+----+
    |  1 | 1.1  |   0  | 1  |
    +----+------+------+----+
    |  1 | 2.0  |   1  | 2  |
    +----+------+------+----+
    |  1 | 3.4  |   2  | 3  |
    +----+------+------+----+
    |  1 | 4.0  |   3  | 2  |
    +----+------+------+----+
    |  2 | 1.2  |   0  | 1  |
    +----+------+------+----+
    |  2 | 2.4  |   1  | 2  |
    +----+------+------+----+
    |  2 | 3.5  |   2  | 3  |
    +----+------+------+----+

Cohorting Examples
---------------------


Cohorting Example 1
^^^^^^^^^^^^^^^^^^^^^^^^^^

An example with limited data (dataset contains only one entity). It is illustrated in script examples/python./matrix_from_duration_data.py with example flag set to 1. Input data set is synthetic_data1.csv

The state space is as follows (for brevity we work directly with the integer representation)

.. code::

    [('0', "A"), ('1', "B"), ('2', "C"), ('3', "D")]

The cohorting algorithm that assigns the last state to the cohort results in the following table. We notice that there is alot of movement inside each cohort (high count) and that only two of the states are represented at the cohort level (0 and 1).

.. code::

       ID  Cohort State       Time  Count
    0   0       0     0   2.061015   21.0
    1   0       1     1   4.400105   14.0
    2   0       2     0   6.665899   28.0
    3   0       3     0   8.842277   14.0
    4   0       4     0  11.111733   21.0
    5   0       5     0  11.182184    2.0

