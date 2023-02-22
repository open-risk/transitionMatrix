Cohort Estimator
========================
A cohort estimator (more accurately discrete time estimator) is class of estimators of multi-state transitions that is a simpler alternative to Duration type estimators



Estimate a Transition Matrix from Cohort Data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Example workflows using transitionMatrix to estimate a transition matrix from data that are already grouped in cohorts

* Script: examples/python/matrix_from_cohort_data.py
* Example ID: 3


.. code::

    data = pd.read_csv(dataset_path + 'synthetic_data6.csv', dtype={'State': str})
    sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
    myState = tm.StateSpace()
    myState.generic(2)
    print(myState.validate_dataset(dataset=sorted_data))
    myEstimator = es.CohortEstimator(states=myState, ci={'method': 'goodman', 'alpha': 0.05})
    result = myEstimator.fit(sorted_data)
    myMatrixSet = tm.TransitionMatrixSet(values=result, temporal_type='Incremental')

    myEstimator.print(select='Counts', period=0)
    myEstimator.print(select='Frequencies', period=18)