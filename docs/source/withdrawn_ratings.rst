Withdrawn Ratings
========================

Withdrawn ratings are a common issue that needs to be handled in the context of estimating transition matrices. See `right censoring issues <https://www.openriskmanual.org/wiki/Withdrawn_Ratings>`_

Adjust NR (Not Rated) States
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Adjusting for NR states can be done via the :meth:`transitionMatrix.model.TransitionMatrix.remove` method.


Single Period Matrix
""""""""""""""""""""""""""""
Example of using transitionMatrix to adjust the (not-rated) NR state. Input data are the Standard and Poor's historical data (1981 - 2016) for corporate credit rating migrations. Example of handling

* Script: examples/python/adjust_nr_states.py


Multi-period Matrix
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* Script: examples/python/fix_multiperiod_matrix.py

Example of using transitionMatrix to detect and solve various pathologies that might be affecting transition matrix data




