Data Formats
============

The transitionMatrix package supports a variety of input data formats for empirical (observation) data.
Two key ones are described here in more detail. More detailed documentation about data formats provided at
the Transition Matrix category at the `Open Risk Manual <https://www.openriskmanual.org/wiki/Category:Transition_Matrix>`_

Long Data Format
-------------------------------------------

The Long Data Format consists of Tuples (ID, Time, From State, To State) indicating the time T at which an entity ID
migrated From -> To state.

Canonical Form
~~~~~~~~~~~~~~~~

The canonical form that is used as input to duration based estimators uses normalize timestamps (from 0 to T_max)
and looks as follows:

    +----+------+----+----+
    | ID | Time | Fr | To |
    +----+------+----+----+
    |  1 | 1.1  | 0  | 1  |
    +----+------+----+----+
    |  1 | 2.0  | 1  | 2  |
    +----+------+----+----+
    |  1 | 3.4  | 2  | 3  |
    +----+------+----+----+
    |  1 | 4.0  | 3  | 2  |
    +----+------+----+----+
    |  2 | 1.2  | 0  | 1  |
    +----+------+----+----+
    |  2 | 2.4  | 1  | 2  |
    +----+------+----+----+
    |  2 | 3.5  | 2  | 3  |
    +----+------+----+----+

String Date Form
~~~~~~~~~~~~~~~~

It is frequent that the transition data have timestamps in the form of a datatime string. For example:

    +----+-------------+----+----+
    | ID | Date String | Fr | To |
    +----+-------------+----+----+
    |  1 | 10-10-2010  | 0  | 1  |
    +----+-------------+----+----+
    |  1 | 10-11-2010  | 1  | 2  |
    +----+-------------+----+----+

In this case the Datetime_to_float function of _`transitionMatrix.utils subpackage` the can be used to convert data into the canonical form

Compact Long Format
-------------------------------------------

Triples (ID, Time, State) indicating the time T at which an entity ID LEFT its previous state S (the state it migrates to
is encoded in the next observation of the same entity).

The compact format avoids the duplication of data but requires that the final state of all entities at the end
of the observation window (Time F) is included as the last record

    +----+-----+---+
    | ID | T   | S |
    +----+-----+---+
    |  1 | 1.1 | 0 |
    +----+-----+---+
    |  1 | 2.0 | 1 |
    +----+-----+---+
    |  1 | 3.4 | 2 |
    +----+-----+---+
    |  1 | 4.0 | 3 |
    +----+-----+---+
    |  1 | F   | 2 |
    +----+-----+---+
    |  2 | 1.2 | 0 |
    +----+-----+---+
    |  2 | 2.4 | 1 |
    +----+-----+---+
    |  2 | 3.5 | 2 |
    +----+-----+---+
    |  2 | F   | 3 |
    +----+-----+---+


Wide Data Format
-------------------------------------------

Conversion from wide to long can be handled using the `pandas wide_to_long method
<https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.wide_to_long.html>`_.
(This method will be more integrated in the future)


Other Formats
-------------------------------------------

Data ingestion is via a pandas dataframe so other formats can be handled with additional coding. Submit an issue
with your desired format.