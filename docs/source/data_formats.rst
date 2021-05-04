Input Data Formats
===================

The transitionMatrix package supports a variety of input data formats for empirical (observation) data. Two key ones are described here in more detail. More background about data formats is available at the `Open Risk Manual Risk Data Category <https://www.openriskmanual.org/wiki/Category:Risk_Data>`_


Long Data Format
-------------------------------------------

Long Data Format is a tabular representation of time series data that records the states (measurements) of multiple entities. Its defining characteristic is that each table row contains data pertaining to one entity at one point in time.

Canonical Form of Long Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Long Data Format (also Narrow or Stacked) consists of Tuples, e.g. (Entity ID, Time, From State, To State) indicating the time T at which an entity with ID migrated from the (From State) -> to the (To State).

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

The canonical form has the advantage of being unambiguous about the context where the transition occurs. The meaning of each row of data stands on its own and does not rely on the order (or even the presence) of other records. This facilitates, for example, the algorithmic processing of the data. On the flipside,  the format is less efficient in terms of storage (the state information occurs twice) compared to the compact format (See below).

The canonical format requires that the final state of all entities at the end of the observation window (Time F) is included (otherwise we have no indication about when the measurements stopped). Alternatively such information is provided as separate metadata (or implicitly, for example if measurements are understood to span a number of full annual periods).

.. note::

    Synthetic_data(7, 8, 9) in the :ref:`Datasets` collection are examples of data in long format and canonical form

String Dates
~~~~~~~~~~~~~~~~

It is frequent that transition data (e.g. from financial applications) have timestamps in the form of a *date string*. For example:

    +----+-------------+------+----+
    | ID | Date String | From | To |
    +----+-------------+------+----+
    |  1 | 10-10-2010  | 0    | 1  |
    +----+-------------+------+----+
    |  1 | 10-11-2010  | 1    | 2  |
    +----+-------------+------+----+

String dates must be converted to a numerical representation before we can work with the transition data. transitionMatrix offers the :func:`transitionMatrix.utils.converters.datetime_to_float` function of :mod:`transitionMatrix.utils` subpackage can be used to convert data into the canonical form.

.. note::

    Synthetic_data9 and rating_data in the :ref:`Datasets` collection have observation times in string data form.


Compact Form of Long Format
-------------------------------------------

The format uses triples (ID, Time, State), indicating the time T at which an entity ID **Left** its previous state S (the state it migrates to is encoded in the next observation of the same entity). The convention can obviously be reversed to indicate the time of entering a new state (in which case we need some information to bound the start of the observation window).

The compact long format avoids the duplication of data of the canonical approach but requires the presence of other records to infer the realised sequence of events.

The format also requires that the final state of all entities at the end of the observation window (Time F) is included as the last record (otherwise we have no indication about when the measurements stopped). Alternatively such information is provided separately (or implicitly, e.g. if measurements are understood to span a number of full annual periods).




    +----+--------+-------+
    | ID | Time   | State |
    +----+--------+-------+
    |  1 |    1.1 |     0 |
    +----+--------+-------+
    |  1 |    2.0 |     1 |
    +----+--------+-------+
    |  1 |    3.4 |     2 |
    +----+--------+-------+
    |  1 |    4.0 |     3 |
    +----+--------+-------+
    |  1 |    F   |     2 |
    +----+--------+-------+
    |  2 |    1.2 |     0 |
    +----+--------+-------+
    |  2 |    2.4 |     1 |
    +----+--------+-------+
    |  2 |    3.5 |     2 |
    +----+--------+-------+
    |  2 |    F   | 3     |
    +----+--------+-------+

Wide Data Format
------------------

Wide Data Format is an alternative tabular representation of time series data that records the states (measurements) of multiple entities. Its defining characteristic is that each table row contains *all the data* pertaining to any one entity. The measurement times are not arbitrary but encoded in the column labels:

    +----+--------+-------+-------+
    | ID |   2011 |  2012 |  2013 |
    +----+--------+-------+-------+
    | A1 |      1 |    0  |    1  |
    +----+--------+-------+-------+
    | A2 |      2 |    1  |    3  |
    +----+--------+-------+-------+
    | A3 |      0 |    1  |    2  |
    +----+--------+-------+-------+

Conversion from wide to long formats can be handled using the `pandas wide_to_long method
<https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.wide_to_long.html>`_.


(This method will be more integrated in the future)


Other Formats
-------------------------------------------

As mentioned, a design choice is that data ingestion of transitionMatrix is via a pandas dataframe so other formats can be handled with additional code by the user. If there is a format that you repeatedly encounter submit an issue with your desired format / transformation `suggestion <https://github.com/open-risk/transitionMatrix/issues>`_.