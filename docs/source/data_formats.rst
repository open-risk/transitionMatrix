Data Formats
============

The transitionMatrix package supports a variety of input data formats for empirical (observation) data.
Two key ones are described here in more detail

Compact Format
-------------------------------------------

Triples (ID, Time, State) indicating the time T at which an entity ID LEFT its previous state S (the state it migrates to
is encoded in the next observation of the same entity).

The compact format avoids the duplication of data but requires that the final state of all entities at the end
observation window (Time F) is included as the last record

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


Full Long Format
-------------------------------------------

Tuples (ID, Time, From State, To State) indicating the time T at which an entity ID migrated From -> To state

    +----+-----+----+----+
    | ID | Tim | Fr | To |
    +----+-----+----+----+
    |  1 | 1.1 | 0  | 1  |
    +----+-----+----+----+
    |  1 | 2.0 | 1  | 2  |
    +----+-----+----+----+
    |  1 | 3.4 | 2  | 3  |
    +----+-----+----+----+
    |  1 | 4.0 | 3  | 2  |
    +----+-----+----+----+
    |  2 | 1.2 | 0  | 1  |
    +----+-----+----+----+
    |  2 | 2.4 | 1  | 2  |
    +----+-----+----+----+
    |  2 | 3.5 | 2  | 3  |
    +----+-----+----+----+


Other Formats
-------------------------------------------

Data ingestion is via a pandas dataframe so other formats can be handled easily with some addition coding (e.g
using the wide_to_long method)